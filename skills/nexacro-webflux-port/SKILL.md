---
name: nexacro-webflux-port
description: Spring Boot / Spring MVC 기반 Nexacro 모듈(xapi / xeni / uiadapter)을 Spring WebFlux 로 포팅하는 전체 플레이북. 사용자가 "webflux 전환", "reactive 로 바꿔", "서블릿 제거", "nexacro webflux", "xapi 포팅", "xeni 포팅", "uiadapter 포팅", "HttpServletRequest 제거" 등을 언급할 때 반드시 이 skill 을 사용하세요. Servlet → WebFlux 포팅에서 자주 놓치는 9가지 함정(classpath 교체, multipart 타입 기반 파싱, paramOf 동치, WebFilter eager caching, ResultHandler 순서, stub shim LIMITATION, base-path, 정적 리소스 수동 매핑, BlockingBridge)을 단계별 체크리스트로 제공합니다.
---

# Nexacro WebFlux Port Skill

Spring Boot / Spring MVC 기반 Nexacro 스택(**xapi**, **xeni**, **uiadapter**, 샘플 앱) 을
Spring WebFlux 로 이식할 때 **반복되는 함정과 표준 해법**을 체크리스트로 제공하는 skill 입니다.

## 경로 규칙 (중요)

Claude Code 는 skill 실행 시 이 SKILL.md 앞에 Base Path 를 자동 주입합니다.

```
Base Path: C:\Users\<user>\.claude\skills\nexacro-webflux-port\
```

모든 참조 문서는 이 Base Path 기준 절대 경로를 사용합니다.

| 참조 | 절대 경로 |
|------|-----------|
| classpath 교체 | `{Base Path}references/classpath-shim.md` |
| ServletProvider shim | `{Base Path}references/servlet-provider-shim.md` |
| multipart import | `{Base Path}references/multipart-import-by-type.md` |
| getParameter 동치 | `{Base Path}references/getparameter-equivalence.md` |
| stub shim LIMITATION | `{Base Path}references/stub-shim-with-limitations.md` |
| WebFilter bypass | `{Base Path}references/webfilter-content-type-bypass.md` |
| ResultHandler 순서 | `{Base Path}references/result-handler-ordering.md` |
| base-path / 정적리소스 | `{Base Path}references/basepath-and-static-resources.md` |

---

## 언제 사용하는가

- **xapi-* / xeni-* / uiadapter-* 모듈을 WebFlux 버전으로 신규 생성** 하거나,
- 기존 Nexacro 기반 Spring Boot 프로젝트에서 **`spring-boot-starter-web` → `spring-boot-starter-webflux` 로 교체**하려고 할 때.

**사용하지 않는 경우**: 모듈 내부 POJO 만 수정하는 단순 변경, Nexacro 와 무관한 WebFlux 튜닝.

---

## 핵심 원칙 (반드시 유지)

1. **원본 POJO / POI 재사용** — `nexacroN-xapi-jakarta.jar`, `nexacroN-xeni-jakarta.jar` 의 POJO/POI 클래스는 **재포팅하지 않는다**. 대신 Servlet 결합 클래스만 classpath 우선순위로 교체한다.
2. **`jdeps ... | grep jakarta.servlet` 결과는 0 건** — CI 게이트. 교체 성공 여부를 이 명령 하나로 검증.
3. **패키지 변경 금지** — 교체 클래스는 원본과 동일 패키지(`com.nexacro.java.xapi.*` / `com.nexacro.java.xeni.*`)를 유지해야 내부 상호 호출이 동작.
4. **`spring-boot-starter-web` 금지** — WebFlux 와 공존 불가.

---

## Phase 별 체크리스트

### Phase A — 모듈 골격 + Maven 규칙

- [ ] **루트 aggregator `pom.xml`** 생성 (`<modules>` 에 xapi-webflux / uiadapter-webflux / xeni-webflux / webflux-example).
- [ ] **라이브러리 모듈** (xapi-webflux / xeni-webflux) 은 **bare deps** 사용:
  ```xml
  <!-- Boot 런타임을 소비자에 전파하지 않음 -->
  <dependency><groupId>org.springframework</groupId><artifactId>spring-webflux</artifactId></dependency>
  <dependency><groupId>io.projectreactor</groupId><artifactId>reactor-core</artifactId></dependency>
  ```
- [ ] **uiadapter 모듈 + 샘플 앱** 은 `spring-boot-starter-webflux` 사용.
- [ ] **원본 JAR** 은 `<scope>system</scope>` + `<systemPath>` + `<optional>true</optional>` (transitive 전파 차단).
- [ ] **Java 17**, Spring Boot 3.5.x (asis 와 동일 버전).

### Phase B — xapi-webflux (Servlet 경계 4개 클래스)

원본 JAR 의 Servlet 결합 클래스 4개 (`HttpPlatformRequest`, `HttpPlatformResponse`,
`HttpJavaTypePlatformResponse`, `HttpPartPlatformResponse`) 를 WebFlux 메서드 추가 버전으로 교체.

- [ ] 기존 `HttpServletRequest#getInputStream()` → `ServerHttpRequest` body `Flux<DataBuffer>` 로 대체.
- [ ] 기존 `HttpServletResponse#getOutputStream()` → `ServerHttpResponse#writeWith()` 로 대체.
- [ ] **패키지 유지**: `com.nexacro.java.xapi.tx.*` (원본 JAR 클래스들이 같은 패키지를 참조).
- [ ] `mvn -pl xapi-webflux compile` 성공 확인.

### Phase C — uiadapter-webflux-core

Interceptor → `WebFilter`, ViewResolver + HandlerMethodReturnValueHandler → `HandlerResultHandler`.

- [ ] **`NexacroWebFilter`**: body caching 하되 **multipart/* + application/x-www-form-urlencoded 는 bypass**. → `{Base Path}references/webfilter-content-type-bypass.md`
- [ ] **`NexacroResultHandler` supports() 상호배제**: `NexacroFileResult` 를 `NexacroFileResultHandler` 에만 위임. `ORDER=0` vs `ORDER=1`. → `{Base Path}references/result-handler-ordering.md`
- [ ] **ArgumentResolver**: `@ParamDataSet` 가 `Mono<DataSet>` 이 아닌 `DataSet` 을 반환하려면 WebFlux 의 `HandlerMethodArgumentResolver#resolveArgument` 가 `Mono` 를 리턴해도 프레임워크가 unwrap 함.
- [ ] **BlockingBridge 유틸** 도입: `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` 래핑.

### Phase D — xeni-webflux (11개 Servlet 결합 클래스 + 1개 orphan)

`maven-dependency-plugin unpack + excludes` 로 원본 JAR 클래스를 classpath 에서 제거하고
`src/main/java` 의 shim 이 우선 적용되도록 설정. **이 전략이 본 skill 의 핵심.**

**반드시 읽을 것**: `{Base Path}references/classpath-shim.md` + `{Base Path}references/servlet-provider-shim.md`

교체 대상 11개 (모두 `jakarta.servlet` import 0건 유지):

| # | 클래스 | 원본 의존성 | 대체 방식 |
|---|---|---|---|
| 1 | `ServletProvider` | `jakarta.servlet.http.*` | `ServerHttpRequest/Response` + upload 슬롯 |
| 2 | `GridExportImportServlet` | `HttpServlet` | stub (기능은 `GridExportImportHandler` 로 이동) |
| 3 | `GridExportImportAgent` | 간접 | 호출 경로 변경 |
| 4 | `XeniMultipartProcBase` | `Part`, `ServletFileUpload` | 사전 파싱 슬롯 활용 |
| 5 | `XeniMultipartProcDef` | `Part`, `ServletFileUpload` | 사전 파싱 슬롯 활용 |
| 6 | `XeniExcelDataStorageBase` | 간접 | 파일 경로 정규화 |
| 7 | `XeniExcelDataStorageDef` | 간접 | 파일 경로 정규화 |
| 8 | `GridPartExportExcel` | 간접 | 호출 경로 변경 |
| 9 | `GridPartExportCsv` | `HttpServletResponse` | **stub shim** + LIMITATION (→ `{Base Path}references/stub-shim-with-limitations.md`) |
| 10 | `ximport.GridImportContext` | `HttpServletResponse#getOutputStream()` | `ServletProvider#getOutputStream()` (캡처 BAOS) |
| 11 | `ximport.impl.GridImportExcelXSSFEvent` | `getHttpServletResponse() == null` 체크 | `getServletProvider() == null` 로 변경 |

**exclude-only 1개**: `export.api.GridExportExcel` (reverse 참조 0건 = orphan. 재구현 불필요).

- [ ] **POI / commons-io 직접 선언** (xeni-webflux 의 system-scope 때문에 transitive 가 안 됨) → uiadapter-webflux-excel 에서 직접 선언.
- [ ] **multipart import 경로**: FilePart/FormFieldPart **타입 기준 분기**. 이름 기준 분기는 취약. → `{Base Path}references/multipart-import-by-type.md`
- [ ] **`jdeps tobe/xeni-webflux/target/*.jar | grep jakarta.servlet` = 0 건** 확인.

### Phase E — 샘플 앱 (E2E 검증)

- [ ] **`paramOf()` 헬퍼** 도입 — `HttpServletRequest.getParameter()` 동치 (query + form merge). → `{Base Path}references/getparameter-equivalence.md`
- [ ] **컨트롤러 매핑**: `@PostMapping` → `@RequestMapping` (asis 와 동일하게 GET/POST 모두 허용).
- [ ] **정적 리소스 수동 매핑** — Tomcat 자동 서빙 없음. `ResourceHandlerRegistry` 로 export/import 경로 등록. → `{Base Path}references/basepath-and-static-resources.md`
- [ ] **base-path 반영** — `spring.webflux.base-path` 가 설정된 환경에서 다운로드 URL 생성 시 `request.exchange().getRequest().getPath().contextPath().value()` prepend.
- [ ] **Nexacro 3종 포맷 E2E 테스트** — XML / SSV / JSON 응답 검증 (nexacro-data-format skill 병용 권장).

---

## 최종 검증 게이트

```bash
# 1. 모든 교체 JAR 에 jakarta.servlet 참조 0건
jdeps tobe/*/target/*.jar | grep jakarta.servlet
# (출력 없어야 성공)

# 2. 통합 테스트
cd tobe && mvn -T 4 clean install

# 3. 샘플 앱 기동 + Nexacro 클라이언트 E2E
cd tobe/webflux-example && ../mvnw spring-boot:run
```

세 단계 모두 통과해야 포팅 완료.

---

## 자주 발생하는 회귀와 원인

| 증상 | 근본 원인 | 해결 위치 |
|---|---|---|
| `500 Server Error` on multipart POST | `NexacroWebFilter` 가 body eager caching | webfilter-content-type-bypass.md |
| `UnsupportedOperationException: ReadOnlyHttpHeaders.set` | `NexacroResultHandler` 가 `NexacroFileResult` 까지 `supports()` | result-handler-ordering.md |
| 다운로드 시 `filenamelist` 가 null | `getQueryParams()` 만 조회 (form body 누락) | getparameter-equivalence.md |
| `NoClassDefFoundError: org/apache/poi/...` | xeni-webflux system-scope → transitive 전파 안 됨 | classpath-shim.md + POI 직접 선언 |
| `NoClassDefFoundError: HttpServletResponse` (JVM 클래스 로드 시) | xeni 교체 클래스가 원본 JAR 클래스와 혼용 → 일부에만 shim 적용 | classpath-shim.md (excludes 누락 확인) |
| 다운로드 URL 이 404 (base-path 환경) | `contextPath` 미반영 | basepath-and-static-resources.md |
| 다운로드된 xlsx 가 `/excel` URL 로 404 | WebFlux 는 정적 리소스 자동 서빙 없음 | basepath-and-static-resources.md |

---

## 관련 skill

- `nexacro-build` — xfdl → xjs 빌드 (샘플 앱 프론트 검증 시 병용).
- `nexacro-data-format` — XML / SSV / JSON 통신 포맷 레퍼런스 (E2E 테스트 payload 작성 시 병용).
- `nexacro-xfdl-author` — 샘플 xfdl 작성 (E2E 검증용 신규 페이지 필요 시).
