# nexacroN-fullstack Repo Map

Layout of the monorepo that the skill clones. Shows which pieces each runner consumes.

> **🚧 진행 중인 변경 (2026-04-29):** 업스트림 `JasonMMo/nexacroN-fullstack` 를 **per-runner self-contained** 구조로 리팩터링 중입니다. 리팩터 완료 후 각 `samples/runners/<KEY>/` 디렉터리는 parent BOM / shared-business 모듈에 의존하지 않고 단독으로 `mvn package` 가 가능합니다. 본 문서는 리팩터 **이전** monorepo 의 모습을 기록하며, 리팩터 머지 후 sparse-checkout 절차도 단순화됩니다 (`nxui` + `samples/runners/<KEY>` 만 받음). plan: `C:\\Users\\mo\\.claude\\plans\\github-nexacro-claude-skills-lovely-salamander.md` Part A.

## Top-level tree

```
nexacroN-fullstack/                            [github.com/JasonMMo/nexacroN-fullstack]
├── README.md
├── LICENSE                                    (MIT)
├── .gitignore
├── pom.xml                                    (parent BOM — dependencyManagement)
├── api-contract/                              ★ always included
│   ├── openapi.yaml                           (15 endpoints)
│   ├── data-formats.md                        (XML / SSV / JSON + _RowType_)
│   └── contract-tests/                        (RestAssured — Plan 3)
├── core/                                      ★ always included
│   ├── xapi-javax/  xapi-jakarta/
│   ├── xeni-javax/  xeni-jakarta/
│   └── uiadapter-javax/  uiadapter-jakarta/
├── nxui/                                      ★ always included
│   ├── packageN.xprj
│   ├── packageN.xadl                          (svcurl=http://localhost:8080/uiadapter/)
│   ├── typedefinition.xml
│   ├── appvariables.xml
│   ├── bootstrap.xml
│   ├── _resource_/
│   ├── frame/                                 (frameLogin, frameMDI, ...)
│   ├── Base/main.xfdl
│   ├── pattern/                               (pattern01-04.xfdl)
│   └── sample/                                (sample*.xfdl)
└── samples/
    ├── seed-data/                             ★ always included
    │   ├── schema.sql                         (HSQL DDL)
    │   ├── data.sql                           (seed data)
    │   └── README.md
    ├── shared-business/                       (plain Spring — selected per jdk)
    │   ├── jdk8-javax/
    │   └── jdk17-jakarta/
    ├── shared-business-egov4/                 (eGov 4.x)
    │   └── jdk8-javax/
    ├── shared-business-egov5/                 (eGov 5.x)
    │   └── jdk17-jakarta/
    ├── shared-business-reactive/              (WebFlux controllers only)
    │   └── jdk17-mybatis/
    └── runners/                               (thin entry-points)
        ├── boot-jdk17-jakarta/
        ├── boot-jdk8-javax/
        ├── mvc-jdk17-jakarta/
        ├── mvc-jdk8-javax/
        ├── egov5-boot-jdk17-jakarta/
        ├── egov4-boot-jdk8-javax/
        ├── egov4-mvc-jdk8-javax/
        └── webflux-jdk17-jakarta/
```

## What sparse-checkout pulls for each runner

For user choice `(jdk=17, framework=spring-boot)`:

```
git sparse-checkout set \
  api-contract core nxui pom.xml README.md LICENSE .gitignore \
  samples/seed-data \
  samples/shared-business/jdk17-jakarta \
  samples/runners/boot-jdk17-jakarta
```

For `(jdk=17, framework=webflux)`:

```
git sparse-checkout set \
  api-contract core nxui pom.xml README.md LICENSE .gitignore \
  samples/seed-data \
  samples/shared-business/jdk17-jakarta \                 # reactive controllers import this
  samples/shared-business-reactive/jdk17-mybatis \
  samples/runners/webflux-jdk17-jakarta
```

→ WebFlux is option A (§2.3 of design spec): reactive layer reuses plain jdk17-jakarta service/mapper.

## Runner → business tree map

```
boot-jdk17-jakarta      ──► shared-business/jdk17-jakarta
boot-jdk8-javax         ──► shared-business/jdk8-javax
mvc-jdk17-jakarta       ──► shared-business/jdk17-jakarta
mvc-jdk8-javax          ──► shared-business/jdk8-javax
egov5-boot-jdk17-jakarta ──► shared-business-egov5/jdk17-jakarta
egov4-boot-jdk8-javax   ──► shared-business-egov4/jdk8-javax
egov4-mvc-jdk8-javax    ──► shared-business-egov4/jdk8-javax
webflux-jdk17-jakarta   ──► shared-business-reactive/jdk17-mybatis
                              └─(imports)─► shared-business/jdk17-jakarta
```

## What's intentionally excluded

- **Spring Security** — login is stubbed (§1.3 of design spec)
- **R2DBC** — WebFlux uses MyBatis sync wrapping for now
- **Production configs** — no Docker/K8s/CI in skeleton
