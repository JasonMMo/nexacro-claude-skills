# Stub shim + LIMITATION 패턴

원본 JAR 에서 **Servlet 결합은 있지만 실제 호출 경로가 없거나 우회 가능한** 클래스는
완전 재구현 대신 **stub shim** 으로 교체한다. 호출되면 `UnsupportedOperationException`
을 던지고, Javadoc 에 LIMITATION 을 명시해 소비자가 대체 경로를 쓰도록 유도한다.

## 언제 쓰는가

| 판정 | 처리 |
|---|---|
| reverse 참조 0건 (orphan) | exclude-only, 재구현 생략 |
| reverse 참조 있음 + 호출 경로 우회 가능 | **stub shim + LIMITATION** |
| reverse 참조 있음 + 호출 경로 우회 불가 | 완전 재구현 (ServletProvider 기반) |

`GridPartExportCsv` 는 2번 케이스 — 내부 POI/streaming 경로에서 참조되지만,
WebFlux 환경에서는 `GridPartExportExcel` 만 사용하므로 CSV 분기는 실제로 실행되지 않는다.

## 표준 스텁 (GridPartExportCsv 예)

```java
package com.nexacro.java.xeni.export.impl;   // 원본 패키지 유지

import com.nexacro.java.xeni.provider.ServletProvider;

/**
 * Servlet 결합이 있던 원본 구현을 WebFlux 환경에서 대체하는 <b>stub shim</b>.
 *
 * <h2>LIMITATION</h2>
 * <ul>
 *   <li><b>CSV export 는 지원하지 않는다.</b> WebFlux 경로에서는
 *       {@link GridPartExportExcel} 만 사용되며, CSV 분기로 진입하는 호출은
 *       런타임에 {@link UnsupportedOperationException} 을 던진다.</li>
 *   <li>원본 JAR 의 다른 클래스가 {@code instanceof GridPartExportCsv} 검사를
 *       수행하는 경로가 있으므로 <b>클래스는 반드시 존재해야 한다</b>
 *       (단순 exclude-only 로는 NoClassDefFoundError).</li>
 *   <li>추후 CSV 지원이 필요하면 {@code ServletProvider#getOutputStream()}
 *       (캡처 BAOS) 기반으로 재구현할 것. 절대 {@code HttpServletResponse} 를
 *       import 하지 말 것 (jdeps 게이트 0건 유지).</li>
 * </ul>
 */
public class GridPartExportCsv {

    public GridPartExportCsv() {
        // 생성은 허용 (instanceof 검사 통과용)
    }

    /**
     * @throws UnsupportedOperationException 항상. WebFlux 환경에서는 CSV export 미지원.
     */
    public void sendExportPartResponse(ServletProvider provider, Object... args) {
        throw new UnsupportedOperationException(
                "GridPartExportCsv is a stub in WebFlux port — CSV export is not supported. "
              + "Use GridPartExportExcel instead. See Javadoc LIMITATION section.");
    }

    // 원본이 public 으로 노출하던 다른 메서드 역시 동일 예외 throw.
}
```

## 설계 원칙

1. **패키지/클래스명 유지** — `com.nexacro.java.xeni.export.impl.GridPartExportCsv`.
   원본 JAR 내부에서 같은 FQCN 으로 참조하므로 패키지를 바꾸면 `NoClassDefFoundError`.

2. **생성자는 성공** — 일부 호출 경로가 `new GridPartExportCsv()` 후
   `instanceof` 검사만 하는 경우가 있다. 생성을 막으면 예상치 못한 지점에서 실패.

3. **메서드는 예외** — 실제 I/O 메서드만 `UnsupportedOperationException`.
   메시지에 **대체 경로와 Javadoc 참조** 를 포함해 디버깅을 돕는다.

4. **Javadoc 에 LIMITATION 섹션 명시** — 향후 유지보수자가
   "왜 stub 인가 / 언제 재구현해야 하는가 / 재구현 시 주의점" 을 바로 파악 가능.

5. **`jdeps` 0건 유지** — stub 이라도 `jakarta.servlet.*` import 금지.
   이 지침을 어기면 전체 포팅의 CI 게이트가 깨진다.

## 검증

```bash
# stub 클래스에도 jakarta.servlet 참조 0건
jdeps -v target/xeni-webflux-*.jar 2>&1 \
    | grep -E "(GridPartExportCsv|GridExportImportServlet).*jakarta.servlet"
# (출력 없어야 성공)

# 원본 JAR 의 소비자가 shim 을 찾는지 확인 (reverse ref 재검증)
javap -c target/classes/com/nexacro/java/xeni/**/*.class 2>&1 \
    | grep GridPartExportCsv
# (shim 참조 경로가 나와야 하고, 원본 JAR 잔재가 남아있으면 안 됨)
```

## 안티패턴 — 하지 말 것

```java
// ❌ 빈 구현으로 조용히 성공 — 호출자가 "동작했다" 고 오해
public void sendExportPartResponse(...) {
    // do nothing
}

// ❌ HttpServletResponse 를 import 해서 일부 메서드만 막음 — jdeps 오염
import jakarta.servlet.http.HttpServletResponse;
public void sendExportPartResponse(HttpServletResponse resp, ...) {
    throw new UnsupportedOperationException();
}

// ❌ 클래스 자체를 exclude-only 로 처리 — 소비자가 instanceof 할 때 NoClassDefFoundError
// (export.api.GridExportExcel 처럼 reverse ref 0건 확인된 경우에만 가능)
```

## 결정 플로우

```
원본 JAR 에 jakarta.servlet 결합 클래스 X 발견
        │
        ▼
    reverse ref 검사 (javap grep)
    ┌────────┴─────────┐
    │                  │
  0건              1건 이상
    │                  │
    ▼                  ▼
exclude-only    실행 경로 분석
                ┌───────┴────────┐
                │                │
           WebFlux 에서         WebFlux 에서도
           진입 안 됨           실제 실행됨
                │                │
                ▼                ▼
           stub shim        완전 재구현
           + LIMITATION     (ServletProvider 기반)
```
