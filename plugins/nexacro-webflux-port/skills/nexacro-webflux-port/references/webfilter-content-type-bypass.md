# NexacroWebFilter — Content-Type 기반 bypass

Nexacro 의 asis Interceptor 는 요청 본문을 eager 하게 읽어 캐시한 뒤
후속 파싱에서 재사용한다. WebFlux 포팅 시 `WebFilter` 에서 동일 전략을
쓰면 **multipart/form-data 및 application/x-www-form-urlencoded 요청이 깨진다**.

## 회귀 증상

```
500 Server Error
Caused by: java.lang.IllegalStateException: Only one connection receive subscriber allowed.
```

또는

```
org.springframework.core.io.buffer.DataBufferLimitException:
    Exceeded limit on max bytes to buffer
```

## 원인

1. `WebFilter` 가 `exchange.getRequest().getBody()` 를 subscribe 해서 바이트 조립.
2. 바이트를 `ServerHttpRequestDecorator` 로 재주입 (wrap body).
3. Spring WebFlux 의 multipart 파서 (`DefaultPartHttpMessageReader`) 나
   `FormHttpMessageReader` 가 **원본 body publisher** 를 다시 subscribe 시도.
4. Reactor Netty 의 body 는 **1회만 subscribe 가능** → 두 번째 subscribe 실패.

## 표준 패턴 — Content-Type bypass

multipart/form-data 와 application/x-www-form-urlencoded 는 **캐시 대상에서 제외**.
해당 요청은 Spring 내장 파서에 맡기고, `getMultipartData()` / `getFormData()` 로 읽는다.

```java
@Component
public class NexacroWebFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        MediaType contentType = exchange.getRequest().getHeaders().getContentType();

        // ── bypass 대상: Spring 이 직접 파싱해야 하는 포맷 ──
        if (contentType != null) {
            if (MediaType.MULTIPART_FORM_DATA.isCompatibleWith(contentType)
             || MediaType.APPLICATION_FORM_URLENCODED.isCompatibleWith(contentType)) {
                // body 를 건드리지 말 것. 그대로 downstream 으로 전달.
                return chain.filter(exchange);
            }
        }

        // ── 캐시 대상: Nexacro SSV/XML/JSON (application/octet-stream 등) ──
        return DataBufferUtils.join(exchange.getRequest().getBody())
                .defaultIfEmpty(exchange.getResponse().bufferFactory().wrap(new byte[0]))
                .flatMap(buffer -> {
                    byte[] bytes = new byte[buffer.readableByteCount()];
                    buffer.read(bytes);
                    DataBufferUtils.release(buffer);

                    // 캐시된 바이트로 body 교체 (재subscribe 가능)
                    ServerHttpRequestDecorator decorated =
                            new ServerHttpRequestDecorator(exchange.getRequest()) {
                                @Override
                                public Flux<DataBuffer> getBody() {
                                    return Flux.defer(() -> Flux.just(
                                            exchange.getResponse().bufferFactory().wrap(bytes)));
                                }
                            };

                    // ServletProvider 슬롯에 byte[] 저장해 downstream 핸들러가 사용
                    exchange.getAttributes().put(CACHED_BODY_ATTR, bytes);

                    return chain.filter(exchange.mutate().request(decorated).build());
                });
    }
}
```

## 왜 form-urlencoded 도 bypass?

`paramOf()` 헬퍼가 `exchange.getFormData()` 로 폼 바디에 접근한다
(→ `getparameter-equivalence.md`). `getFormData()` 는 내부적으로
원본 body publisher 를 subscribe 하므로, WebFilter 에서 이미 subscribe 하면
**같은 증상 (second subscribe 실패)** 발생.

## 왜 multipart 는 bypass?

`exchange.getMultipartData()` 가 body 스트림을 파싱해야 `FilePart` / `FormFieldPart`
를 반환할 수 있다. WebFilter 에서 body 를 byte[] 로 join 해버리면
multipart boundary 파싱 정보가 손실되어 `getMultipartData()` 가 빈 Map 반환.

## bypass 하지 말아야 하는 케이스

- `application/octet-stream` (Nexacro SSV binary)
- `application/xml`, `text/xml` (Nexacro XML)
- `application/json` (Nexacro JSON)
- `text/plain`

이 포맷들은 Nexacro 의 `HttpPlatformRequest` 가 직접 파싱하므로,
**WebFilter 가 바이트를 캐시해 `ServletProvider#getInputStream()` 으로 재주입**해야 한다.

## 검증 체크리스트

- [ ] multipart POST (`/excel/import.do`) → 500 에러 없이 FilePart 파싱 성공.
- [ ] hidden form POST (`/multiDownloadFiles.do`) → `paramOf()` 가 form body 값 반환.
- [ ] Nexacro SSV POST (`/dept/selectList.do`) → `HttpPlatformRequest` 가
      `ServletProvider#getInputStream()` 으로 SSV 파싱 성공.
- [ ] 대용량 파일 업로드 → `DataBufferLimitException` 없이 완료.

## 디버그 로그 추가 권장

```java
if (logger.isDebugEnabled()) {
    logger.debug("NexacroWebFilter path={} contentType={} action={}",
            exchange.getRequest().getPath().value(),
            contentType,
            bypassed ? "BYPASS" : "CACHE");
}
```

환경별 content-type 변주 (예: `multipart/form-data; boundary=...`,
`application/x-www-form-urlencoded; charset=UTF-8`) 를 한눈에 확인.

## 요약

| Content-Type | 처리 | 이유 |
|---|---|---|
| `multipart/form-data` | bypass | Spring 내장 multipart 파서가 body 재subscribe |
| `application/x-www-form-urlencoded` | bypass | `getFormData()` 가 body 재subscribe |
| `application/octet-stream` | cache | Nexacro SSV 가 `getInputStream()` 사용 |
| `application/xml`, `application/json` | cache | Nexacro XML/JSON 파서가 `getInputStream()` 사용 |
| Content-Type 없음 | cache | GET 요청 등. body 없으면 join 이 즉시 완료. |
