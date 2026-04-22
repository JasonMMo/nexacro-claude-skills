# ServletProvider shim 패턴

원본 `com.nexacro.java.xeni.provider.ServletProvider` 는 `HttpServletRequest` / `HttpServletResponse`
를 직접 보관하고 `getInputStream()` / `getOutputStream()` 등을 위임한다.
WebFlux 에서는 이 클래스를 **요청별 컨텍스트 객체**로 재정의하여 원본 POJO 들이 그대로 호출 가능하게 한다.

## 최소 시그니처 (원본과 동일 유지)

```java
package com.nexacro.java.xeni.provider;   // 패키지 변경 금지

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

public class ServletProvider {

    // ── 1. HTTP 기본 속성 (원본 HttpServletRequest 위임 대체) ──────────────
    private String requestUrl;          // exchange.getRequest().getURI().toString()
    private String queryString;         // exchange.getRequest().getURI().getRawQuery()
    private String contextPath;         // exchange.getRequest().getPath().contextPath().value()
    private String characterEncoding;   // "UTF-8" 기본
    private String contentType;
    private int    contentLength;

    // ── 2. Body 입력 스트림 (원본 HttpServletRequest#getInputStream() 대체) ─
    /** 핸들러가 `Flux<DataBuffer>` 를 byte[] 로 조립한 뒤 ByteArrayInputStream 으로 주입. */
    private InputStream bodyInputStream;

    // ── 3. 업로드 슬롯 (WebFlux 신설 — 사전 파싱 FilePart 주입용) ──────────
    private InputStream uploadFileStream;
    private String      uploadFileName;

    // ── 4. Output 캡처 (원본 HttpServletResponse#getOutputStream() 대체) ───
    /** 모든 write 가 이 BAOS 로 캡처된 뒤 핸들러에서 응답 본문으로 flush. */
    private final ByteArrayOutputStream capturedOutput = new ByteArrayOutputStream();

    // ── getter / setter / helper ─────────────────────────────────────────
    public InputStream  getInputStream()           { return bodyInputStream; }
    public OutputStream getOutputStream()          { return capturedOutput; }
    public byte[]       getCapturedBytes()         { return capturedOutput.toByteArray(); }
    public void         setBodyInputStream(InputStream is) { this.bodyInputStream = is; }

    public void setUploadFileStream(InputStream is) { this.uploadFileStream = is; }
    public InputStream getUploadFileStream()        { return uploadFileStream; }
    public void setUploadFileName(String name)      { this.uploadFileName = name; }
    public String getUploadFileName()               { return uploadFileName; }

    // ... 나머지 HTTP 속성 getter/setter (원본 ServletProvider 시그니처 그대로)
}
```

## 요청별 생성 흐름 (핸들러 레벨)

```java
public Mono<ServerResponse> handleExport(ServerRequest request) {
    return request.bodyToMono(byte[].class)
            .defaultIfEmpty(new byte[0])
            .flatMap(bodyBytes -> {
                ServletProvider provider = new ServletProvider();
                provider.setRequestUrl(request.uri().toString());
                provider.setQueryString(request.uri().getRawQuery());
                provider.setContextPath(request.exchange().getRequest()
                        .getPath().contextPath().value());
                provider.setCharacterEncoding("UTF-8");
                provider.setBodyInputStream(new ByteArrayInputStream(bodyBytes));

                return Mono.fromCallable(() -> {
                    // 원본 xeni POJO 들이 ServletProvider 기반으로 동작
                    GridExportImportAgent agent = new GridExportImportAgent();
                    agent.gridExport(provider, configuration);
                    return provider.getCapturedBytes();
                }).subscribeOn(Schedulers.boundedElastic())
                  .flatMap(bytes -> ServerResponse.ok()
                          .contentType(MediaType.APPLICATION_OCTET_STREAM)
                          .bodyValue(bytes));
            });
}
```

## 원칙

1. **상태는 요청 스코프** — `ServletProvider` 인스턴스는 반드시 요청마다 새로 생성. 스프링 빈 금지.
2. **출력 캡처** — 쓰기는 `capturedOutput` BAOS 로만 받고 핸들러에서 flush. 도중에 `ServerHttpResponse` 에 직접 쓰지 않음 (ordering 문제).
3. **업로드 슬롯은 사전 파싱 값** — multipart/* 요청은 핸들러가 `FilePart` 를 미리 바이트로 조립한 뒤 `setUploadFileStream` / `setUploadFileName` 호출. 원본 `ServletFileUpload` 경로는 사용 안 함.
4. **jakarta.servlet import 금지** — 이 파일은 `jdeps` 게이트에서 0 건 유지 대상.

## 소비자 측 계약

원본 JAR 의 다음 클래스들이 `ServletProvider` 를 통해 I/O 한다:

| 소비자 | 호출 메서드 | WebFlux 대응 |
|---|---|---|
| `XeniMultipartProcDef#getImportData()` | `getUploadFileStream()` / `getUploadFileName()` | 슬롯 read |
| `GridImportContext#getResponseWriter()` | `getOutputStream()` | 캡처 BAOS write |
| `GridPartExportExcel#sendExportPartResponse()` | `getOutputStream()` | 캡처 BAOS write |
| `PlatformRequest` | `getInputStream()` | body BAOS read |

이 계약만 맞으면 원본 JAR 의 수백 개 POJO 는 **아무 수정 없이** WebFlux 환경에서 동작한다.
