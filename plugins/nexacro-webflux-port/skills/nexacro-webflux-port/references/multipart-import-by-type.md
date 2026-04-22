# Multipart import — part 타입 기준 분기 (이름 기준 금지)

Nexacro 의 Excel import 경로는 multipart/form-data 로 **platform SSV 본문 + 업로드 파일** 두 part 를 보낸다.
WebFlux 에서 part 를 파싱할 때 **이름 기반 매칭을 하면 환경마다 실패**한다.

## 안티패턴 (이름 기준 분기) — 하지 말 것

```java
// ❌ 클라이언트가 보내는 part 이름은 환경마다 다를 수 있음
exchange.getMultipartData().flatMap(multipartData -> {
    List<Part> formFields = multipartData.get("PlatformData");   // 환경마다 다른 이름
    List<Part> fileParts  = multipartData.get("file");            // 환경마다 다른 이름
    // ...
});
```

**실패 사례**:
- 구버전 Nexacro: `PlatformData` / `file`
- 특정 버전: `platform` / `upload`
- 어떤 패치 후: 빈 문자열 이름 / UUID 이름

→ `multipartData.get("PlatformData")` 가 `null` 이면 import 가 조용히 실패.

## 표준 패턴 (타입 기준 분기) — 반드시 이 방식

asis 의 `XeniMultipartProcDef#getImportData()` 와 동일 전략: **`FilePart` vs `FormFieldPart` 인터페이스로 분기**.

```java
exchange.getMultipartData().flatMap(multipartData -> {
    FormFieldPart platformField = null;
    FilePart      filePart      = null;

    // 이름 무시, 타입으로만 첫 번째 발견한 part 를 채택
    for (List<Part> parts : multipartData.values()) {
        for (Part p : parts) {
            if (p instanceof FilePart && filePart == null) {
                filePart = (FilePart) p;
            } else if (p instanceof FormFieldPart && platformField == null) {
                platformField = (FormFieldPart) p;
            }
        }
    }

    // 디버그 로그 (환경별 part 이름 문제 파악용)
    if (logger.isDebugEnabled()) {
        logger.debug("multipart parts platformField={} filePart={}",
                platformField != null ? platformField.name() : "<none>",
                filePart != null ? filePart.name() + "(" + filePart.filename() + ")" : "<none>");
    }

    // FormFieldPart 는 value() 로 즉시 읽음 (스트리밍 불필요)
    final FormFieldPart pField = platformField;
    Mono<byte[]> platformBytesMono = pField != null
            ? Mono.fromCallable(() -> pField.value().getBytes(StandardCharsets.UTF_8))
            : Mono.just(new byte[0]);

    // FilePart 는 DataBuffer 스트림 → 바이트 조립
    final FilePart fPart = filePart;
    Mono<byte[]> fileBytesMono = fPart != null
            ? DataBufferUtils.join(fPart.content())
                .map(buf -> {
                    byte[] b = new byte[buf.readableByteCount()];
                    buf.read(b);
                    DataBufferUtils.release(buf);
                    return b;
                })
                .defaultIfEmpty(new byte[0])
            : Mono.just(new byte[0]);

    // 파일명 정규화 (Windows IE 구식 경로 대응)
    String rawName = fPart != null ? fPart.filename() : null;
    String fileName;
    if (rawName != null && !rawName.isEmpty()) {
        String norm = rawName.replace('\\', '/');
        int slash = norm.lastIndexOf('/');
        fileName = slash >= 0 ? norm.substring(slash + 1) : norm;
    } else {
        fileName = "upload.xlsx";
    }

    return Mono.zip(platformBytesMono, fileBytesMono)
            .flatMap(tuple -> processImport(tuple.getT1(), tuple.getT2(), fileName));
});
```

## ServletProvider 슬롯 주입 + agent.gridImport 경로

바이트를 직접 `XeniMultipartReqData` 로 조립하지 말 것. **ServletProvider 슬롯에 주입하고 agent.gridImport 에 위임**
— 원본 경로와 동일한 `saveImportStream` → import 처리가 일관되게 동작.

```java
private Mono<byte[]> processImport(byte[] platformBytes, byte[] fileBytes, String fileName) {
    return Mono.fromCallable(() -> {
        ServletProvider provider = new ServletProvider();
        provider.setCharacterEncoding("UTF-8");

        // 플랫폼 파트 → bodyInputStream (XeniMultipartProcDef 가 PlatformRequest 로 파싱)
        provider.setBodyInputStream(new ByteArrayInputStream(platformBytes));

        // 업로드 파일 파트 → uploadFile 슬롯 (XeniMultipartProcDef 가 reqData 에 주입)
        if (fileBytes.length > 0) {
            provider.setUploadFileStream(new ByteArrayInputStream(fileBytes));
            provider.setUploadFileName(fileName);
        }

        GridExportImportAgent agent = new GridExportImportAgent();
        agent.setMinMessage(configuration.isMinMessage());

        // agent.gridImport 가 내부적으로
        //   XeniMultipartProcDef.getImportData(provider) → reqData 구성
        //   → saveImportStream → import 처리
        // 까지 모두 처리.
        int result = agent.gridImport(provider, configuration);
        if (result < 0) {
            return buildErrorBytes(result, agent.getErrorMessage());
        }
        return provider.getCapturedBytes();
    }).subscribeOn(Schedulers.boundedElastic());
}
```

## 요약

| 원칙 | 이유 |
|---|---|
| **part 타입으로 분기** | 이름은 환경/버전마다 다름 |
| **ServletProvider 슬롯 경유** | agent.gridImport 내부가 ServletProvider 계약 기반 |
| **`XeniMultipartReqData` 직접 구성 금지** | saveImportStream 등 내부 단계 누락 → silent failure |
| **파일명 경로 정규화** | Windows IE 구버전이 `C:\path\file.xlsx` 를 그대로 보냄 |
