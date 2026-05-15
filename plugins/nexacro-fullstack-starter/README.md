# nexacro-fullstack-starter

> **하나의 nxui 화면, 7개의 검증된 백엔드 스택.**
> 동일한 Nexacro N v24 packageN UI (55 xfdl 화면) 가 7가지 서로 다른 Spring 서버 조합 위에서 동일하게 동작합니다. `/nexacro-fullstack-starter` 한 번 실행으로 원하는 조합을 골라 즉시 빌드 가능한 프로젝트를 받습니다.

---

## 🏆 검증된 7개 Tech Spec

| # | Runner Key | JDK | Servlet | Framework | Spring | Boot | eGov | Packaging |
|---|---|---|---|---|---|---|---|---|
| 1 | `boot-jdk17-jakarta` ⭐ | 17 | jakarta | Spring Boot | 6 | 3 | — | jar |
| 2 | `boot-jdk8-javax` | 8 | javax | Spring Boot | 5 | 2 | — | jar |
| 3 | `mvc-jdk17-jakarta` | 17 | jakarta | Spring MVC | 6 | — | — | war (Tomcat 10) |
| 4 | `mvc-jdk8-javax` | 8 | javax | Spring MVC | 5 | — | — | war (Tomcat 9) |
| 5 | `egov5-boot-jdk17-jakarta` | 17 | jakarta | eGov Boot | 6 | 3 | 5 | jar |
| 6 | `egov4-boot-jdk8-javax` | 8 | javax | eGov Boot | 5 | 2 | 4 | jar |
| 7 | `egov4-mvc-jdk8-javax` | 8 | javax | eGov MVC | 5 | — | 4 | war (Tomcat 9) |

⭐ = 기본 추천 (모던 JDK 17 / Spring Boot 3 / jakarta lane)

> `webflux-jdk17-jakarta` 는 1개 placeholder 로 남아 있으며 차기 버전에서 unblock 됩니다.

---

## ⚡ 3-Step Quick Start

### 1. 플러그인 설치 (최초 1회)
```bash
/plugin marketplace add JasonMMo/nexacro-claude-skills
/plugin install nexacro-fullstack-starter@nexacro-claude-skills
```

### 2. 스캐폴드 실행
```
/nexacro-fullstack-starter
```
프롬프트가 3개 질문을 묻습니다:
1. **JDK** — 8 또는 17
2. **Framework** — spring-boot / spring-mvc / egov-boot / egov-mvc
3. **Project name** — 영숫자 + 대시 (예: `my-app`)

→ 자동으로 (JDK, Framework) 조합에 맞는 runner 가 선택되고, 평탄화된 디렉터리가 만들어집니다.

### 3. 빌드 & 실행

**JAR runner (Boot 계열, 4종)**
```bash
cd my-app
mvn -o clean package
mvn spring-boot:run
# → http://localhost:8080/uiadapter/packageN/index.html
```

**WAR runner (MVC 계열, 3종)**
```bash
cd my-app
mvn -o clean package
# target/uiadapter.war 를 Tomcat 9 (javax) 또는 Tomcat 10 (jakarta) webapps/ 에 배포
```

---

## 🎯 어떤 조합을 골라야 할까?

| 상황 | 추천 |
|---|---|
| 신규 프로젝트, 제약 없음 | **`boot-jdk17-jakarta`** (1번) |
| 레거시 JDK 8 환경, 가벼운 Boot | `boot-jdk8-javax` (2번) |
| WAR 배포 강제 (외부 Tomcat) | `mvc-jdk17-jakarta` (3번) 또는 `mvc-jdk8-javax` (4번) |
| 공공기관/eGov 표준 (jdk17) | `egov5-boot-jdk17-jakarta` (5번) |
| 공공기관/eGov 표준 (jdk8) | `egov4-boot-jdk8-javax` (6번) |
| eGov + WAR 배포 (외부 WAS) | `egov4-mvc-jdk8-javax` (7번) |

자세한 의사결정 트리는 `skills/nexacro-fullstack-starter/references/runner-selection-guide.md` 참조.

---

## 🧱 동일한 nxui, 다른 백엔드

모든 7개 runner 는 **같은 nxui 폴더** (Nexacro N v24 packageN, 55 xfdl 화면) 를 그대로 사용합니다. 화면을 한 번 만들면 백엔드 스택을 교체해도 클라이언트는 재작성이 필요 없습니다.

각 runner 가 공통으로 제공하는 것:
- ✅ Canonical uiadapter 패턴 — `com.nexacro.uiadapter.{config, controller, domain, mapper, service, service.impl}`
- ✅ Nexacro 1st-party 모듈 사용 — uiadapter-core / xapi / xeni (envelope 자체 구현 X)
- ✅ HSQLDB in-memory + `schema.sql` / `data.sql` 자동 로드
- ✅ MyBatis mapper (`classpath:mybatis/mappers/*-mapper.xml`)
- ✅ 11개 controller — Board / Dept / File / Large / User / Video / Wide / TestData / ExcelExport / Relay / Stream
- ✅ FileController 6개 endpoint — advancedUploadFiles, advancedDownloadFile, multiDownloadFiles, advancedDownloadFiles, advancedDownloadList, advancedDeleteFiles
- ✅ Self-contained pom (parent BOM 의존성 없음)

---

## 🚦 자동 검증

스캐폴드 직후 다음 항목들이 자동 체크됩니다 (Step 3-3, 3-4):

1. **평탄화 검증** — `api-contract/`, `core/`, `samples/` 가 root 에 남아 있지 않음
2. **필수 트리** — `nxui/`, `src/`, `pom.xml` 존재
3. **4.2 layout** — 레거시 패키지 (`com.nexacro.{fullstack, runner}`) 부재 + canonical `com.nexacro.uiadapter.{config, controller, domain, mapper, service, service/impl}` 존재
4. **Packaging-aware** — JAR runner 는 `Application.java` 필수, WAR runner 는 Tomcat 이 부트스트랩 (검증 생략)

검증 실패 시 명확한 에러 메시지와 함께 PR 머지 상태 확인 지침을 안내합니다.

---

## 📂 산출 디렉터리 구조

```
my-app/
├── nxui/                                # Nexacro N v24 packageN (55 xfdl, 동일)
│   ├── packageN.xadl
│   ├── typedefinition.xml
│   └── ...
├── src/main/
│   ├── java/com/nexacro/uiadapter/      # canonical 4.2 layout
│   │   ├── Application.java             # JAR runner 만
│   │   ├── config/
│   │   ├── controller/                  # 11 controller
│   │   ├── domain/                      # 8 domain
│   │   ├── mapper/                      # 7 mapper
│   │   └── service/{,impl}/
│   ├── resources/
│   │   ├── application.yml              # context-path: /uiadapter
│   │   ├── schema.sql                   # HSQLDB, ^^ separator
│   │   ├── data.sql
│   │   ├── mybatis/
│   │   └── logback.xml (또는 log4j2.xml)
│   └── webapp/WEB-INF/                  # WAR runner 만
│       ├── web.xml
│       └── spring/*.xml
├── pom.xml                              # self-contained
└── README.md
```

---

## 🛠️ 거부되는 조합

다음은 자동 거부되고 대안이 제시됩니다:

| 조합 | 이유 | 대안 |
|---|---|---|
| `egov-mvc` + `jdk17` | eGov 4 MVC + jakarta lane 미지원 | `egov5-boot-jdk17-jakarta` |
| `webflux` + `jdk8` | WebFlux 는 jakarta 만 지원 | `boot-jdk8-javax` |
| `webflux` + `jdk17` (현재) | placeholder (차기 버전) | `boot-jdk17-jakarta` |

---

## 📚 참조 문서

- `skills/nexacro-fullstack-starter/SKILL.md` — 전체 스캐폴드 흐름
- `skills/nexacro-fullstack-starter/references/compatibility-matrix.md` — 호환성 매트릭스 상세
- `skills/nexacro-fullstack-starter/references/repo-map.md` — 업스트림 monorepo 구조 + runner 구현 현황
- `skills/nexacro-fullstack-starter/references/runner-selection-guide.md` — 의사결정 트리
- `skills/nexacro-fullstack-starter/references/troubleshooting.md` — 빌드/런타임 흔한 오류

업스트림 소스: [`JasonMMo/nexacroN-fullstack`](https://github.com/JasonMMo/nexacroN-fullstack)

---

## 🔖 Version

현재 버전: **0.8.2** — 7개 runner 구현 완료 + WAR-aware 4.2 layout 검증

업데이트:
```bash
/plugin update nexacro-fullstack-starter@nexacro-claude-skills
```
