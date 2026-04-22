# HandlerResultHandler 순서 — ORDER + supports() 상호배제

Nexacro uiadapter 는 컨트롤러가 반환하는 두 가지 타입을 구분해 응답을 만든다:

- `NexacroResult` → XML/SSV/JSON 직렬화 후 body 로 write
- `NexacroFileResult` / `NexacroMultiFileResult` → 파일 스트림을 응답으로 pipe

WebFlux 에서는 **두 종류의 `HandlerResultHandler` 를 등록하고, `supports()` 와
`@Order` 조합으로 위임 경로를 결정**한다. 한 쪽이 다른 쪽의 타입까지 처리하면
`UnsupportedOperationException: ReadOnlyHttpHeaders.set` 같은 혼합 실행 버그가 발생.

## 회귀 증상

```
java.lang.UnsupportedOperationException: This HttpHeaders instance is read-only
    at org.springframework.http.ReadOnlyHttpHeaders.set
    at com.nexacro.uiadapter.webflux.core.NexacroResultHandler.handleResult
```

**원인**: `NexacroResultHandler` 가 `supports()` 에서 `true` 를 반환해서
`NexacroFileResult` 까지 받았는데, 내부적으로 `response.getHeaders().set(...)`
을 시도. 단, Spring WebFlux 는 이미 `writeWith()` 가 호출된 뒤에 headers 를
`ReadOnlyHttpHeaders` 로 잠근다. `NexacroFileResultHandler` 는
writeWith 전에 headers 를 설정하지만, `NexacroResultHandler` 에 먼저 걸리면
순서가 꼬인다.

## 표준 패턴 — `supports()` 로 타입을 완전 분리

```java
// ── 일반 응답 (XML/SSV/JSON) ──
@Component
@Order(0)
public class NexacroResultHandler implements HandlerResultHandler {

    @Override
    public boolean supports(HandlerResult result) {
        Object value = result.getReturnValue();
        // FileResult 계열은 받지 않음 — 다른 핸들러가 처리
        if (value instanceof NexacroFileResult) return false;
        if (value instanceof NexacroMultiFileResult) return false;
        return value instanceof NexacroResult;
    }

    @Override
    public Mono<Void> handleResult(ServerWebExchange exchange, HandlerResult result) {
        NexacroResult r = (NexacroResult) result.getReturnValue();
        byte[] body = serialize(r, exchange);   // XML / SSV / JSON
        exchange.getResponse().getHeaders().setContentType(resolveContentType(exchange));
        return exchange.getResponse().writeWith(
                Mono.just(exchange.getResponse().bufferFactory().wrap(body)));
    }
}

// ── 파일 다운로드 응답 ──
@Component
@Order(1)
public class NexacroFileResultHandler implements HandlerResultHandler {

    @Override
    public boolean supports(HandlerResult result) {
        Object value = result.getReturnValue();
        return value instanceof NexacroFileResult
            || value instanceof NexacroMultiFileResult;
    }

    @Override
    public Mono<Void> handleResult(ServerWebExchange exchange, HandlerResult result) {
        Object value = result.getReturnValue();

        // 1. Content-Disposition / Content-Type 헤더는 writeWith 전에 설정
        applyDownloadHeaders(exchange.getResponse(), value);

        // 2. 파일 스트림을 Flux<DataBuffer> 로 변환
        Flux<DataBuffer> body = toDataBufferFlux(value, exchange);

        // 3. writeWith 로 응답. 이 시점 이후 headers 는 ReadOnly.
        return exchange.getResponse().writeWith(body);
    }
}
```

## 핵심 규칙

1. **`supports()` 는 상호배제** — 같은 타입이 두 핸들러에 걸리면 안 됨.
   `NexacroResultHandler#supports()` 는 `NexacroFileResult` 계열을 **명시적으로 제외**.

2. **`@Order` 는 tie-breaker** — `supports()` 가 제대로 분리돼 있으면 순서가 중요하지 않지만,
   방어적으로 `NexacroResultHandler=0`, `NexacroFileResultHandler=1` 로 둬서
   혹시 겹치는 타입이 생겨도 일반 응답이 먼저 시도되게.

3. **headers 는 `writeWith` 전에** — Spring WebFlux 는 body write 가 시작되면
   headers 를 `ReadOnlyHttpHeaders` 로 잠근다. 특히 `NexacroFileResultHandler` 에서
   Content-Disposition 을 뒤늦게 설정하는 버그 조심.

4. **하나의 응답엔 한 번의 writeWith** — `writeWith` 를 두 번 호출하면 즉시 에러.
   여러 파일 다운로드 (`NexacroMultiFileResult`) 는 zip 스트림으로 **미리 조립**해서
   단일 `Flux<DataBuffer>` 로 넘긴다.

## `HandlerResultHandler` 등록

WebFlux 는 application context 에 등록된 `HandlerResultHandler` 빈을 자동 수집하지만,
순서 보장을 위해 `WebFluxConfigurer#configureHttpMessageCodecs` 와는 별개로
`@Order` 를 반드시 명시.

```java
@Configuration
public class NexacroResultHandlerConfig {

    @Bean
    public NexacroResultHandler nexacroResultHandler(...) {
        return new NexacroResultHandler(...);
    }

    @Bean
    public NexacroFileResultHandler nexacroFileResultHandler(...) {
        return new NexacroFileResultHandler(...);
    }
}
```

## 디버그 팁

핸들러가 어떤 타입을 받고 있는지 확인:

```java
@Override
public boolean supports(HandlerResult result) {
    Object value = result.getReturnValue();
    boolean ok = /* 판정 로직 */;
    if (logger.isDebugEnabled()) {
        logger.debug("{}#supports returnType={} returnValueClass={} result={}",
                getClass().getSimpleName(),
                result.getReturnType(),
                value != null ? value.getClass().getName() : "null",
                ok);
    }
    return ok;
}
```

로그에서 두 핸들러가 **같은 요청에 대해 모두 `supports=true`** 를 찍으면
상호배제가 깨진 것. `NexacroResult` 인터페이스를 `NexacroFileResult` 가
implement 하고 있는 경우가 대표적 — `supports()` 에서 FileResult 를 먼저 걸러야 한다.

## 상속 관계 주의

```java
// asis 의 타입 계층 예시
public interface NexacroResult { ... }
public class NexacroFileResult implements NexacroResult { ... }   // ⚠️
```

`NexacroFileResult` 가 `NexacroResult` 를 구현하면 naive `instanceof NexacroResult`
는 FileResult 도 true 로 받는다. **반드시 `NexacroFileResult` 를 먼저 검사**해서
exclude.

```java
// ✅ 올바른 순서
if (value instanceof NexacroFileResult) return false;   // 먼저 exclude
if (value instanceof NexacroMultiFileResult) return false;
return value instanceof NexacroResult;                   // 그 다음 include
```

## 요약 표

| 핸들러 | ORDER | `supports()` | 대응 리턴 타입 |
|---|---|---|---|
| `NexacroResultHandler` | 0 | FileResult 제외한 `NexacroResult` | XML/SSV/JSON |
| `NexacroFileResultHandler` | 1 | `NexacroFileResult` / `NexacroMultiFileResult` | 파일 다운로드 |
