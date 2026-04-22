# HttpServletRequest#getParameter() 동치 — `paramOf()` 헬퍼

Servlet API 의 `HttpServletRequest#getParameter(name)` 은 **쿼리스트링과 폼 바디를 하나의 parameter map 으로 머지**해서 반환한다.
WebFlux 는 `getQueryParams()` (쿼리스트링) 와 `getFormData()` (폼 바디) 를 **완전히 분리**해서 노출하므로,
쿼리만 조회하면 폼 바디에 있는 값이 `null` 로 읽혀 회귀가 발생한다.

## 회귀 시나리오

Nexacro 의 `FileDownloadTransaction` 은 클라이언트에서 **hidden HTML form POST** 로
`filenamelist` / `file` / `subFolder` 등 파라미터를 전송한다.

```java
// ❌ 쿼리스트링만 조회 → filenamelist 가 form body 에 있어서 null
String filenamelist = exchange.getRequest().getQueryParams().getFirst("filenamelist");
if (filenamelist == null) throw new NexacroException("No input fileName specified.");
```

증상:
- 단일 파일 다운로드는 동작 (query string 에 포함) 하지만,
- 다중 파일 다운로드에서 `filenamelist` 를 찾지 못해 500 에러.

## 표준 헬퍼 — `paramOf()`

쿼리스트링 우선 조회 → 없고 Content-Type 이 form-urlencoded 인 경우에만 폼 바디로 fallback.

```java
/**
 * Servlet {@code HttpServletRequest#getParameter(name)} 동치.
 *
 * <p>Servlet API 는 query string 과 form body 를 하나의 parameter map 으로 머지해서 반환하지만,
 * WebFlux 는 {@code getQueryParams()}(쿼리 only) 와 {@code getFormData()}(폼 바디 only) 를
 * 분리해서 노출한다. Nexacro FileDownloadTransaction 이 hidden HTML form POST 로
 * 파라미터를 전송하므로 query string 만 읽으면 값이 null 이다.
 *
 * <p>동작:
 * <ol>
 *   <li>query string 에 있으면 즉시 반환.</li>
 *   <li>Content-Type 이 application/x-www-form-urlencoded 이면 getFormData() 로 fallback.</li>
 *   <li>그 외에는 empty Mono.</li>
 * </ol>
 */
private static Mono<String> paramOf(ServerWebExchange exchange, String name) {
    String fromQuery = exchange.getRequest().getQueryParams().getFirst(name);
    if (fromQuery != null) return Mono.just(fromQuery);

    MediaType ct = exchange.getRequest().getHeaders().getContentType();
    if (ct != null && MediaType.APPLICATION_FORM_URLENCODED.isCompatibleWith(ct)) {
        return exchange.getFormData().mapNotNull(form -> form.getFirst(name));
    }
    return Mono.empty();
}
```

## 사용 패턴 — `Mono.zip` + `switchIfEmpty`

여러 파라미터를 동시에 읽을 때는 `Mono.zip` + `switchIfEmpty` 패턴으로 필수/선택 구분.

```java
@RequestMapping("/multiDownloadFiles.do")
public Mono<NexacroMultiFileResult> multiDownloadFiles(ServerWebExchange exchange) {
    String charset = charsetOf(exchange);
    return Mono.zip(
                    paramOf(exchange, "filenamelist")
                            .switchIfEmpty(Mono.error(new NexacroException("No input fileName specified."))),
                    paramOf(exchange, "subFolder").defaultIfEmpty("")
            )
            .flatMap(t -> {
                String rawList = t.getT1();
                String filefolder = t.getT2();
                try {
                    String filenamelist = removedPathTraversal(URLDecoder.decode(rawList, charset));
                    // ... 다운로드 경로 조립
                    return Mono.just(new NexacroMultiFileResult(...));
                } catch (UnsupportedEncodingException e) {
                    return Mono.error(new NexacroException("URL decode failed", e));
                }
            });
}
```

## 중요 포인트

1. **form body 는 1회성 소비** — `exchange.getFormData()` 는 body 스트림을 소비하므로 한 요청에서 여러 번 호출해도 캐시되어 안전하지만, 이미 body 가 `NexacroWebFilter` 등에서 다른 용도로 소비됐다면 문제. WebFilter 레벨에서 form-urlencoded 는 bypass 필수 (→ `webfilter-content-type-bypass.md`).

2. **`switchIfEmpty` 로 필수 검증** — `defaultIfEmpty` 는 누락을 조용히 지나침. 반드시 있어야 하는 파라미터는 `switchIfEmpty(Mono.error(...))` 로 실패 전파.

3. **URL 디코딩은 fallback 이후** — `paramOf()` 는 raw 값만 반환. 디코딩은 호출자 `flatMap` 에서 `charset` 과 함께 처리.

4. **메서드 시그니처에 `throws Exception` 제거** — reactive 체인에서는 `Mono.error` 로 예외 전파. `URLDecoder.decode` 의 `UnsupportedEncodingException` 은 `try/catch` → `Mono.error` 로 변환.
