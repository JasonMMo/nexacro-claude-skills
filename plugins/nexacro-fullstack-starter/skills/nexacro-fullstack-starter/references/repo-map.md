# nexacroN-fullstack Repo Map

업스트림 모노레포에서 skill 이 어떤 부분을 가져오는지 정리한 문서입니다.

> **2026-04-29 업데이트:** 업스트림 `JasonMMo/nexacroN-fullstack` 가 **per-runner self-contained** 구조로 리팩터되었습니다 ([PR #1](https://github.com/JasonMMo/nexacroN-fullstack/pull/1)). 각 `samples/runners/<KEY>/` 디렉터리는 parent BOM / shared-business 모듈 의존 없이 단독 `mvn package` 가 가능합니다. 이에 맞춰 skill 의 sparse-checkout 도 **`nxui` + `samples/runners/<KEY>` 두 경로만** 받도록 단순화되었습니다.

> **2026-05-07 업데이트:** `boot-jdk17-jakarta` 가 GitLab 캐노니컬 패턴 (`nexacron/spring-boot/jakarta/uiadapter-jakarta`) 으로 재작성되었습니다 ([PR #2](https://github.com/JasonMMo/nexacroN-fullstack/pull/2)). 자체 구현 envelope/codec 을 걷어내고 1st-party `uiadapter-jakarta-core` 모듈의 `@ParamDataSet` / `@ParamVariable` argument resolver + `NexacroResult` return-value handler 로 대체. 컨트롤러는 `@Controller @RequestMapping("/foo.do")` (NO `/uiadapter/` prefix — `application.yml` 의 `context-path: /uiadapter` 가 prefix 담당). 패키지 레이아웃은 `com.nexacro.uiadapter.{config, controller, service, service.impl, mapper, domain}` 평면 구조.

> **2026-05-07 업데이트 (javax lane):** `boot-jdk8-javax` 도 동일한 캐노니컬 패턴으로 재작성되었습니다 ([PR #3](https://github.com/JasonMMo/nexacroN-fullstack/pull/3)). javax lane 에서는 `uiadapter-spring-{core,dataaccess,excel}` 모듈을 사용하고 import 경로는 `com.nexacro.uiadapter.spring.*` (jakarta lane 의 `com.nexacro.uiadapter.jakarta.*` 와 대응). JDK 8 호환을 위해 `List.of`/`Map.of`/`isBlank` 는 `Collections.emptyList()`/`Collections.singletonList()`/`Arrays.asList()`/`.trim().isEmpty()` 로 치환. mybatis plugin 은 `com.nexacro.uiadapter.spring.dao.mybatis.{NexacroMybatisMetaDataProvider,NexacroMybatisResultSetHandler}` 를 사용.

> **2026-05-07 업데이트 (canonical WebMvcConfig + 런타임 dep 갭 해소):** [PR #5](https://github.com/JasonMMo/nexacroN-fullstack/pull/5) 가 머지되어 양 레인의 `UiadapterWebMvcConfig` 가 GitLab 캐노니컬 샘플 (`nexacron/spring-boot/jakarta/uiadapter-jakarta`) 과 1:1 정렬되었습니다 — `ApplicationContextProvider`, `MultipartFilter`, `GridExportImportServlet` (`/XExportImport.do`), `NexacroHandlerMethodReturnValueHandler` + `NexacroView`/`NexacroFileView`/`NexacroStreamView`, `NexacroMappingExceptionResolver`, `xeniExcelInitializer`, `dbmsProvider` (HSQL) 가 모두 등록됩니다. xeni 1st-party 의 `commons-fileupload2-jakarta:2.0.0-M1` (jakarta) / `commons-fileupload:1.5` (javax) 런타임 의존성도 함께 추가되었습니다 (xeni pom 은 transitive 0개). 또한 `NexacroN_server_license.xml` 가 `.gitignore` 에 등록되어 있고, 각 runner README 에 `src/main/resources/NexacroN_server_license.xml` 드롭 위치가 문서화되어 있습니다 — xapi 라이선스 로더는 클래스패스 루트에서 해당 정확한 파일명을 찾습니다. 라이선스 미배치 시 첫 `*.do` 호출에서 `InvalidLicenseException` 으로 500 발생.

## 구현 현황 (2026-05-07 기준)

| Runner KEY | 상태 | 비고 |
|---|---|---|
| `boot-jdk17-jakarta` | ✅ canonical | self-contained pom + GitLab 캐노니컬 uiadapter 패턴 |
| `boot-jdk8-javax` | ✅ canonical | javax lane 캐노니컬 패턴 포팅 완료 (PR #3) |
| `mvc-jdk17-jakarta` | ⏳ placeholder | 업스트림 Plan 2 대기 (README-only 스텁) |
| `mvc-jdk8-javax` | ⏳ placeholder | 업스트림 Plan 2 대기 |
| `egov5-boot-jdk17-jakarta` | ⏳ placeholder | 업스트림 Plan 2 대기 |
| `egov4-boot-jdk8-javax` | ⏳ placeholder | 업스트림 Plan 2 대기 |
| `egov4-mvc-jdk8-javax` | ⏳ placeholder | 업스트림 Plan 2 대기 |
| `webflux-jdk17-jakarta` | ⏳ placeholder | 업스트림 Plan 2 대기 |

placeholder 상태인 runner 는 skill 의 `rejectedCombinations` 가 scaffold 단계에서 차단합니다.

## 업스트림 Top-level tree (현행)

```
nexacroN-fullstack/                    [github.com/JasonMMo/nexacroN-fullstack]
├── README.md
├── LICENSE                            (MIT)
├── .gitignore
├── api-contract/                      (참고자료, scaffold 시 미사용)
│   ├── openapi.yaml
│   └── data-formats.md
├── core/                              (참고자료, scaffold 시 미사용)
│   ├── xapi-javax/  xapi-jakarta/
│   ├── xeni-javax/  xeni-jakarta/
│   └── uiadapter-javax/  uiadapter-jakarta/
├── nxui/                              ★ scaffold 가 가져옴
│   ├── packageN.xprj
│   ├── packageN.xadl                  (svcurl=http://localhost:8080/uiadapter/)
│   ├── typedefinition.xml
│   ├── appvariables.xml
│   ├── bootstrap.xml
│   ├── _resource_/
│   ├── frame/                         (frameLogin, frameMDI, ...)
│   ├── Base/main.xfdl
│   ├── pattern/                       (pattern01-04.xfdl)
│   └── sample/                        (sample*.xfdl)
└── samples/runners/                   (각 디렉터리가 독립적으로 빌드 가능)
    ├── boot-jdk17-jakarta/            ✅ src/, pom.xml, src/main/resources/{schema,data}.sql
    ├── boot-jdk8-javax/               ✅ src/, pom.xml, src/main/resources/{schema,data}.sql
    ├── mvc-jdk17-jakarta/             ⏳ README only
    ├── mvc-jdk8-javax/                ⏳ README only
    ├── egov5-boot-jdk17-jakarta/      ⏳ README only
    ├── egov4-boot-jdk8-javax/         ⏳ README only
    ├── egov4-mvc-jdk8-javax/          ⏳ README only
    └── webflux-jdk17-jakarta/         ⏳ README only
```

> Part A 리팩터 결과로 root `pom.xml` (parent BOM), `samples/shared-business*`, `samples/seed-data/` 는 더 이상 존재하지 않거나 사용되지 않습니다. 각 self-contained runner 가 자신의 의존성·seed-data 를 자체 보유합니다.

## skill 의 sparse-checkout (현행)

`(jdk=17, framework=spring-boot)` 선택 시:

```bash
git clone --filter=blob:none --no-checkout https://github.com/JasonMMo/nexacroN-fullstack.git
cd nexacroN-fullstack
git sparse-checkout init --no-cone
git sparse-checkout set \
  nxui \
  samples/runners/boot-jdk17-jakarta
git checkout
```

> `--no-cone` 모드: cone 모드는 디렉터리 단위만 허용하고 파일 단위 패턴을 거부하므로 일관되게 `--no-cone` 사용. `api-contract/`, `core/`, root `pom.xml`/`README.md`/`LICENSE`/`.gitignore` 는 모두 체크아웃 대상에서 제외됩니다.

## 평탄화 복사

체크아웃 후 skill 은 두 디렉터리만 타겟 프로젝트 루트로 평탄화 복사합니다:

```bash
cp -r "$TMP_DIR/nexacroN-fullstack/nxui" "${TARGET_DIR}/"
cp -r "$TMP_DIR/nexacroN-fullstack/samples/runners/${RUNNER_KEY}/." "${TARGET_DIR}/"
```

결과:

```
{{PROJECT_NAME}}/
├── nxui/                              (Nexacro studio project)
├── src/main/java/...                  (runner + 인라인된 business 소스)
├── src/main/resources/                (mybatis xml, application.yml, schema.sql, data.sql)
├── pom.xml                            (self-contained — parent X)
└── README.md
```

`api-contract/`, `core/`, `samples/` 디렉터리는 결과물에 **포함되지 않습니다**. skill Step 3-3 가드가 이를 강제 검증합니다.

## skill Step 3-3 / 3-4 가드 (4.2 layout)

scaffold 직후 SKILL.md Step 3-3 (평탄화 검증) 다음에 Step 3-4 가 자동 실행되어 다음 4 가지를 강제 검증합니다:

1. **legacy 패키지 부재** — `src/main/java/com/nexacro/fullstack`, `src/main/java/com/nexacro/runner` 가 존재하면 실패. OLD self-implemented 패턴 (Part D 이전) 이 업스트림 main 에 머물러 있는 경우를 감지.
2. **canonical 패키지 존재** — `src/main/java/com/nexacro/uiadapter/Application.java` 가 반드시 존재.
3. **6 개 필수 서브패키지** — `config`, `controller`, `domain`, `mapper`, `service`, `service/impl` 모두 존재.
4. **service / service/impl 분리 sanity** — `service/` 루트에 `*Impl.java` 가 있으면 경고 (구현체는 `service/impl/` 에 있어야 함).

검증 실패 시 사용자에게 다음 안내:
- jakarta lane (jdk17) → upstream `JasonMMo/nexacroN-fullstack` PR #2 머지 상태 확인
- javax lane (jdk8) → upstream Phase 2 PR (canonical-uiadapter-pattern-javax) 머지 상태 확인

이 가드는 skill plugin v0.4.0 (2026-05-07) 부터 적용됩니다.

## 의도적으로 제외된 항목

- **Spring Security** — login 은 stub 처리 (§1.3 of design spec)
- **R2DBC** — WebFlux 는 MyBatis sync wrapping 사용 (placeholder 상태)
- **Production configs** — Docker/K8s/CI 는 skeleton 에 포함 X
- **api-contract/** — 참고자료 (OpenAPI 스펙·data-format 가이드)
- **core/** — nexacro 1st-party JAR 의 참조 소스 (실제 의존성은 tobesoft Nexus 에서 받아옴)
