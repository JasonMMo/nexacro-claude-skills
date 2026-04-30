# nexacroN-fullstack Repo Map

업스트림 모노레포에서 skill 이 어떤 부분을 가져오는지 정리한 문서입니다.

> **2026-04-29 업데이트:** 업스트림 `JasonMMo/nexacroN-fullstack` 가 **per-runner self-contained** 구조로 리팩터되었습니다 ([PR #1](https://github.com/JasonMMo/nexacroN-fullstack/pull/1)). 각 `samples/runners/<KEY>/` 디렉터리는 parent BOM / shared-business 모듈 의존 없이 단독 `mvn package` 가 가능합니다. 이에 맞춰 skill 의 sparse-checkout 도 **`nxui` + `samples/runners/<KEY>` 두 경로만** 받도록 단순화되었습니다.

## 구현 현황 (2026-04-29 기준)

| Runner KEY | 상태 | 비고 |
|---|---|---|
| `boot-jdk17-jakarta` | ✅ implemented | self-contained pom, mvn package 검증됨 |
| `boot-jdk8-javax` | ✅ implemented | self-contained pom, mvn package 검증됨 |
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

## 의도적으로 제외된 항목

- **Spring Security** — login 은 stub 처리 (§1.3 of design spec)
- **R2DBC** — WebFlux 는 MyBatis sync wrapping 사용 (placeholder 상태)
- **Production configs** — Docker/K8s/CI 는 skeleton 에 포함 X
- **api-contract/** — 참고자료 (OpenAPI 스펙·data-format 가이드)
- **core/** — nexacro 1st-party JAR 의 참조 소스 (실제 의존성은 tobesoft Nexus 에서 받아옴)
