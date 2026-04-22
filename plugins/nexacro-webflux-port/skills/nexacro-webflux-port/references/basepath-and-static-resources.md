# base-path 반영 + 정적 리소스 수동 매핑

WebFlux 는 Spring MVC / Tomcat 과 달리 **정적 리소스 자동 서빙이 없다**.
또한 `spring.webflux.base-path` 가 설정된 환경에서는 애플리케이션이 **수동으로
context path 를 URL 앞에 붙여** 주지 않으면 클라이언트가 404 를 맞는다.

Nexacro 의 Excel export/import 경로는 이 두 이슈를 동시에 만난다.

---

## Issue 1 — `spring.webflux.base-path` 반영

### 증상

`application.yml`:
```yaml
spring:
  webflux:
    base-path: /myapp
```

애플리케이션 내부에서 생성한 다운로드 URL:
```java
// ❌ context path 누락
String downloadUrl = "/excel/" + filename + ".xlsx";
```

클라이언트가 받는 URL: `/excel/report_xxx.xlsx`
실제 서버 매핑: `/myapp/excel/report_xxx.xlsx`
→ **404**

### 해결 — `RequestPath.contextPath()` prepend

```java
public String buildDownloadUrl(ServerWebExchange exchange, String filename) {
    String contextPath = exchange.getRequest()
            .getPath()
            .contextPath()
            .value();   // "/myapp" 또는 "" (base-path 미설정 시)

    return contextPath + "/excel/" + filename;
}
```

`RequestPath.contextPath().value()` 는:
- base-path 설정 시 → `"/myapp"` (leading slash 있음, trailing slash 없음)
- base-path 미설정 시 → `""` (빈 문자열)

양쪽 모두 **그대로 prepend** 해도 정상 URL 이 된다.

### ServletProvider 로 전달

핸들러에서 `ServletProvider` 에 미리 주입하면 downstream POJO 가 사용 가능:

```java
ServletProvider provider = new ServletProvider();
provider.setContextPath(exchange.getRequest().getPath().contextPath().value());
provider.setRequestUrl(exchange.getRequest().getURI().toString());
// ...
```

원본 JAR 의 `GridExportImportAgent` 가 `ServletProvider#getContextPath()` 를 호출해
응답에 포함되는 다운로드 링크를 조립한다.

---

## Issue 2 — 정적 리소스 자동 서빙 없음

### 증상

Excel export 결과물이 `webflux-example/target/classes/static/excel/report_xxx.xlsx`
로 저장되고, 응답 body 에 다운로드 URL `/myapp/excel/report_xxx.xlsx` 가 포함되지만
클라이언트가 해당 URL 로 요청하면 404.

**이유**: Spring MVC 는 Tomcat 이 `classpath:/static/**` 을 자동 서빙하지만,
**WebFlux 는 기본적으로 `/webjars/**` 만 등록**한다. 나머지는 개발자가 명시 등록.

### 해결 — `WebFluxConfigurer#addResourceHandlers`

```java
@Configuration
public class StaticFileConfig implements WebFluxConfigurer {

    private final NexacroExcelProperties excelProperties;

    public StaticFileConfig(NexacroExcelProperties excelProperties) {
        this.excelProperties = excelProperties;
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // Nexacro Excel export 결과물
        registry.addResourceHandler("/excel/**")
                .addResourceLocations("classpath:/static/excel/",
                                     "file:" + excelProperties.getExportPath() + "/")
                .setCacheControl(CacheControl.noCache());

        // Nexacro Excel import 업로드 스풀 (확인용)
        registry.addResourceHandler("/import/**")
                .addResourceLocations("file:" + excelProperties.getImportPath() + "/")
                .setCacheControl(CacheControl.noCache());

        // 일반 정적 리소스 (xfdl.js, xtheme, css, images)
        registry.addResourceHandler("/**")
                .addResourceLocations("classpath:/static/")
                .setCacheControl(CacheControl.maxAge(Duration.ofHours(1)));
    }
}
```

### 주의 — 경로 우선순위

`/**` 핸들러는 **맨 마지막** 에 등록. 먼저 등록한 `/excel/**`, `/import/**`,
`/webjars/**` 등이 우선 매칭되고, 매칭 실패 시 `/**` 로 fallback.

Spring 은 **등록 순서대로** `ResourceWebHandler` 체인을 구성하므로, 일반
fallback 을 먼저 등록하면 구체 경로가 그림자에 가려진다.

### 주의 — `file:` 스킴 과 trailing slash

```java
// ❌ trailing slash 누락 → "fileexportPath123" 처럼 경로 조립 오류
.addResourceLocations("file:" + excelProperties.getExportPath())

// ✅ trailing slash 필수
.addResourceLocations("file:" + excelProperties.getExportPath() + "/")
```

`ResourceHandlerRegistry` 는 location 을 prefix 로 쓰는데, trailing slash 가 없으면
`new PathResource(location + filename)` 이 `file:/tmp/exportreport.xlsx` 같은
잘못된 경로를 만든다.

### 주의 — base-path 와 handler pattern

`addResourceHandler("/excel/**")` 의 패턴은 **context path 를 제외한 경로**.
즉 base-path 가 `/myapp` 이어도 핸들러 pattern 은 `/excel/**` 그대로 두면
실제 매칭은 `/myapp/excel/xxx` 에서 자동 동작.

```java
// ✅ base-path 반영은 Spring 이 자동 처리
registry.addResourceHandler("/excel/**")   // "/myapp/excel/**" 이라고 쓰지 말 것
```

---

## 조합 체크리스트

Nexacro Excel 다운로드 E2E 가 동작하려면:

- [ ] 컨트롤러/핸들러에서 `exchange.getRequest().getPath().contextPath().value()`
      를 `ServletProvider#setContextPath()` 에 주입.
- [ ] `GridExportImportAgent` 가 생성하는 응답 body 에 이 contextPath 가 prepend 된
      URL 이 포함되는지 **로그로 확인**.
- [ ] `StaticFileConfig` 에 `/excel/**` → export path 매핑 등록.
- [ ] `application.yml` 의 `spring.webflux.base-path` 와
      `nexacro.excel.export-path` 가 실제 파일 시스템 경로와 일치.
- [ ] 다운로드 URL 을 브라우저로 직접 열었을 때 xlsx 가 내려오는지 검증.
- [ ] xfdl 클라이언트에서도 동일 URL 로 `ObjectFileDownload` 가 동작하는지 검증.

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 다운로드 URL 404 (base-path 환경) | contextPath 미반영 | `RequestPath.contextPath().value()` prepend |
| 다운로드 URL 404 (base-path 없는 환경) | 정적 리소스 핸들러 미등록 | `ResourceHandlerRegistry` 로 `/excel/**` 수동 매핑 |
| 다운로드 URL 에 `//excel/` (슬래시 2개) | contextPath 가 이미 slash 포함인데 URL 조립에서 중복 | `contextPath + "/excel/..."` 에서 contextPath 는 `""` 또는 `"/myapp"` 만 리턴 — 중복 slash 생성 경로 재확인 |
| 파일은 생성됐는데 서빙 404 | `file:` location trailing slash 누락 | `file:" + path + "/"` 로 수정 |
| 모든 /excel 이 404 인데 /webjars 는 동작 | `/**` 핸들러가 먼저 등록돼 `/excel/**` 을 가림 | 핸들러 등록 순서 변경 (구체 → 일반) |

## 참고

Spring MVC 의 `WebMvcConfigurer#addResourceHandlers` 와 시그니처 동일.
asis 코드에 이미 있는 설정을 WebFlux 의 `WebFluxConfigurer` 로 **인터페이스만 바꿔서** 포팅 가능.
단, `EncodedResourceResolver` 등 MVC 전용 resolver 는 WebFlux 에서 작동하지 않으므로 제거.
