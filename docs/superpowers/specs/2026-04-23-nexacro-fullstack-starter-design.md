# nexacro-fullstack-starter — Design Spec

- **Date**: 2026-04-23
- **Status**: Draft (pending user review)
- **Author**: Claude (Opus orchestration)
- **Target plugin**: `plugins/nexacro-fullstack-starter/`
- **Target monorepo**: `github.com/JasonMMo/nexacroN-fullstack` (new)

---

## 1. Overview & Goals

### 1.1 Problem

사용자는 GitLab에 **8개의 nexacroN 샘플 프로젝트**를 버전·프레임워크 조합별로 따로 관리하고 있다. 각 repo마다 `nxui`(프론트 소스)와 Spring 샘플 자바 코드를 **중복 유지**하고 있어, 기능 1개 추가 시 최대 8곳을 수정해야 한다.

### 1.2 Goals

1. **Consumer UX**: 개발자가 Claude Code 한 줄로 (nexacro 버전, JDK, 프레임워크) 조건을 고르면 해당 조합의 풀스택 프로젝트가 즉시 세팅된다.
2. **Provider UX**: 유지보수 대상 코드베이스를 **8개 → 5개 자바 트리 + 1개 nxui** 로 축소.
3. **Contract Stability**: 모든 runner가 **동일한 API 계약**(15 endpoints: 14 common + 1 webflux-only)을 노출 → 같은 `packageN` nxui가 어느 runner와도 동작.

### 1.3 Non-Goals (Out of Scope — 이번 작업)

- nexacro17, nexacro14 버전 (향후 `nexacro17-fullstack`, `nexacro14-fullstack` repo)
- Spring Security 통합 (로그인은 스텁)
- R2DBC 기반 WebFlux (현재 MyBatis 동기 래핑만)
- eGov4 MVC + jdk17/jakarta 조합 (미요청)
- Production-ready 배포 설정 (Docker, K8s 등)

---

## 2. Design Decisions

### 2.1 Matrix (nexacroN 전용, 8 runner)

| # | runner | JDK | servlet-api | 프레임워크 | eGov | 비즈니스 트리 |
|---|---|---|---|---|---|---|
| 1 | `boot-jdk17-jakarta` | 17 | jakarta | Spring Boot 3 | — | `shared-business/jdk17-jakarta` |
| 2 | `boot-jdk8-javax` | 8 | javax | Spring Boot 2 | — | `shared-business/jdk8-javax` |
| 3 | `mvc-jdk17-jakarta` | 17 | jakarta | Spring 6 (war) | — | `shared-business/jdk17-jakarta` |
| 4 | `mvc-jdk8-javax` | 8 | javax | Spring 5 (war) | — | `shared-business/jdk8-javax` |
| 5 | `egov5-boot-jdk17-jakarta` | 17 | jakarta | eGov 5 / Boot 3 | 5.x | `shared-business-egov5/jdk17-jakarta` |
| 6 | `egov4-boot-jdk8-javax` | 8 | javax | eGov 4 / Boot 2 | 4.x | `shared-business-egov4/jdk8-javax` |
| 7 | `egov4-mvc-jdk8-javax` | 8 | javax | eGov 4 / Spring 5 (war) | 4.x | `shared-business-egov4/jdk8-javax` |
| 8 | `webflux-jdk17-jakarta` | 17 | jakarta | Spring Boot 3 + WebFlux | — | `shared-business-reactive/jdk17-mybatis` |

### 2.2 Derivation Rules

```
servletApi   = (jdk >= 17) ? "jakarta" : "javax"
springMajor  = (servletApi == "jakarta") ? 6 : 5
bootMajor    = (servletApi == "jakarta") ? 3 : 2
egovVersion  = (servletApi == "jakarta") ? "5.x" : "4.x"
```

→ 사용자는 `nexacroVersion / jdk / framework / useEgov` 4개만 선택, 나머지는 자동 유도.

### 2.3 Architecture — C'''''' (API contract-driven, MVC/Boot 통합)

핵심 원칙:
1. **API 계약**(`api-contract/openapi.yaml`)이 유일한 진실 원천. 모든 runner가 이를 준수.
2. **비즈니스 코드는 JDK/servlet-api 기준으로만 분리** (MVC ↔ Boot 는 같은 소스 공유).
3. **runner는 얇은 부트스트랩** (POM + `Application.java` 또는 `web.xml`만).
4. **WebFlux 옵션 A**: controller만 분리, service/mapper는 `shared-business/jdk17-jakarta` 재사용.

### 2.4 Repo 2원 구조

- **Repo 1**: `github.com/JasonMMo/nexacro-claude-skills` (기존) — 플러그인 정의.
- **Repo 2**: `github.com/JasonMMo/nexacroN-fullstack` (신규) — 실제 코드 모노레포.
- 향후: `nexacro17-fullstack`, `nexacro14-fullstack` — 동일 패턴.

---

## 3. Plugin Structure (Repo 1)

```
plugins/nexacro-fullstack-starter/
├── .claude-plugin/
│   └── plugin.json                           (name/version/keywords)
├── skills/
│   └── nexacro-fullstack-starter/
│       ├── SKILL.md                          (메인 플로우)
│       ├── assets/
│       │   ├── matrix.json                   (8 runner × clone URL)
│       │   └── prompts/
│       │       ├── collect-params.md
│       │       └── post-install.md
│       └── references/
│           ├── compatibility-matrix.md       (derivation 규칙 상세)
│           ├── repo-map.md                   (nexacroN-fullstack 트리 설명)
│           ├── runner-selection-guide.md     (언제 어느 runner를 고를지)
│           └── troubleshooting.md            (port/JDK/war 배포 이슈)
```

### 3.1 plugin.json

```json
{
  "name": "nexacro-fullstack-starter",
  "version": "0.1.0",
  "description": "Scaffolds a full-stack Nexacro project (nxui + Spring server) from a nexacro version × JDK × framework matrix.",
  "author": { "name": "JasonMMo", "url": "https://github.com/JasonMMo" },
  "homepage": "https://github.com/JasonMMo/nexacro-claude-skills",
  "license": "MIT",
  "keywords": ["nexacro", "fullstack", "scaffold", "spring-boot", "spring-mvc", "webflux", "egovframework"]
}
```

### 3.2 matrix.json (요약)

```json
{
  "nexacroN": {
    "repo": "https://github.com/JasonMMo/nexacroN-fullstack.git",
    "branch": "main",
    "runners": {
      "boot-jdk17-jakarta": {
        "businessTree": "shared-business/jdk17-jakarta",
        "runnerPath": "samples/runners/boot-jdk17-jakarta",
        "jdk": 17, "servletApi": "jakarta", "framework": "spring-boot", "bootMajor": 3, "egov": null
      },
      "boot-jdk8-javax":     { "businessTree": "shared-business/jdk8-javax",           "runnerPath": "samples/runners/boot-jdk8-javax",     "jdk": 8,  "servletApi": "javax",   "framework": "spring-boot",       "bootMajor": 2 },
      "mvc-jdk17-jakarta":   { "businessTree": "shared-business/jdk17-jakarta",        "runnerPath": "samples/runners/mvc-jdk17-jakarta",   "jdk": 17, "servletApi": "jakarta", "framework": "spring-mvc",        "springMajor": 6 },
      "mvc-jdk8-javax":      { "businessTree": "shared-business/jdk8-javax",           "runnerPath": "samples/runners/mvc-jdk8-javax",      "jdk": 8,  "servletApi": "javax",   "framework": "spring-mvc",        "springMajor": 5 },
      "egov5-boot-jdk17-jakarta": { "businessTree": "shared-business-egov5/jdk17-jakarta",  "runnerPath": "samples/runners/egov5-boot-jdk17-jakarta",  "jdk": 17, "servletApi": "jakarta", "framework": "egov-boot", "egovMajor": 5 },
      "egov4-boot-jdk8-javax":    { "businessTree": "shared-business-egov4/jdk8-javax",     "runnerPath": "samples/runners/egov4-boot-jdk8-javax",     "jdk": 8,  "servletApi": "javax",   "framework": "egov-boot", "egovMajor": 4 },
      "egov4-mvc-jdk8-javax":     { "businessTree": "shared-business-egov4/jdk8-javax",     "runnerPath": "samples/runners/egov4-mvc-jdk8-javax",      "jdk": 8,  "servletApi": "javax",   "framework": "egov-mvc",  "egovMajor": 4 },
      "webflux-jdk17-jakarta":    { "businessTree": "shared-business-reactive/jdk17-mybatis","runnerPath": "samples/runners/webflux-jdk17-jakarta",    "jdk": 17, "servletApi": "jakarta", "framework": "webflux" }
    },
    "alwaysInclude": ["api-contract", "core", "nxui", "samples/seed-data"]
  }
}
```

### 3.3 SKILL.md 플로우 (요약)

1. **Step 1**: 파라미터 수집 — `nexacroVersion` (default `nexacroN`), `jdk`, `framework`, `useEgov`, `projectName`, `targetDir`
2. **Step 2**: Matrix 조회 → runner key 결정 → derivation 규칙으로 파생 변수 계산
3. **Step 3**: 호환성 체크 — 불가능 조합(`framework=mvc + useEgov=true + jdk=17` 등)은 거부
4. **Step 4**: Clone 전략 — sparse clone 또는 full clone + prune
5. **Step 5**: 복사 & 토큰 치환 — `{{PROJECT_NAME}}`, `{{BACKEND_URL}}`, `{{CONTEXT_PATH}}`
6. **Step 6**: 후처리 — `README.md` 생성 (runner별 실행 명령), `.gitignore`, 초기 커밋
7. **Step 7**: 검증 출력 — 다음 명령 안내 (`mvn` 빌드, nexacro IDE 열기, DB 초기화)

---

## 4. Monorepo Structure (Repo 2: `nexacroN-fullstack`)

```
nexacroN-fullstack/
├── README.md
├── CONTRIBUTING.md
├── pom.xml                                   (parent BOM, dependencyManagement)
├── api-contract/
│   ├── openapi.yaml                          (15 endpoints: 14 common + 1 webflux-only)
│   ├── data-formats.md                       (XML/SSV/JSON, _RowType_)
│   └── contract-tests/                       (RestAssured or Spring Cloud Contract)
├── core/
│   ├── xapi-javax/                           (Spring 5)
│   ├── xapi-jakarta/                         (Spring 6)
│   ├── xeni-javax/
│   ├── xeni-jakarta/
│   ├── uiadapter-javax/
│   └── uiadapter-jakarta/
├── nxui/                                     (packageN 1벌)
│   ├── packageN.xprj
│   ├── packageN.xadl                         (svcurl=http://localhost:8080/uiadapter/)
│   ├── typedefinition.xml
│   ├── appvariables.xml
│   ├── bootstrap.xml
│   ├── _resource_/
│   ├── frame/                                (frameLogin.xfdl 등 8 파일)
│   ├── Base/main.xfdl
│   ├── pattern/                              (pattern01~pattern04.xfdl)
│   └── sample/                               (sampleDataType.xfdl 등)
└── samples/
    ├── seed-data/
    │   ├── schema.sql                        (HSQL DDL)
    │   ├── data.sql                          (초기 테스트 데이터)
    │   └── README.md
    ├── shared-business/
    │   ├── jdk8-javax/                       (Maven module)
    │   │   ├── pom.xml
    │   │   └── src/main/java/com/example/sample/
    │   │       ├── controller/               (*.do 매핑)
    │   │       ├── service/
    │   │       ├── mapper/                   (MyBatis 인터페이스 + XML)
    │   │       ├── dto/
    │   │       └── config/                   (DataSource, MyBatis, HSQL)
    │   └── jdk17-jakarta/
    │       └── (동일 구조, jakarta import)
    ├── shared-business-egov4/
    │   └── jdk8-javax/                       (egov4 dependency, EgovAbstractServiceImpl 상속)
    ├── shared-business-egov5/
    │   └── jdk17-jakarta/                    (egov5 dependency)
    ├── shared-business-reactive/
    │   └── jdk17-mybatis/                    (controller만 — service/mapper는 shared-business/jdk17-jakarta 의존)
    │       ├── pom.xml                       (WebFlux + shared-business/jdk17-jakarta 의존)
    │       └── src/main/java/.../controller/ (Mono<> 반환)
    └── runners/                              (8개 — POM + 부트스트랩만)
        ├── boot-jdk17-jakarta/
        │   ├── pom.xml                       (spring-boot-starter-web 3.x)
        │   ├── src/main/java/.../Application.java
        │   └── src/main/resources/application.yml
        ├── boot-jdk8-javax/
        ├── mvc-jdk17-jakarta/
        │   ├── pom.xml                       (war packaging)
        │   └── src/main/webapp/WEB-INF/web.xml
        ├── mvc-jdk8-javax/
        ├── egov5-boot-jdk17-jakarta/
        ├── egov4-boot-jdk8-javax/
        ├── egov4-mvc-jdk8-javax/
        └── webflux-jdk17-jakarta/
```

### 4.1 Parent POM 전략

- 루트 `pom.xml`은 BOM 역할 — 버전 관리, 공통 플러그인 설정.
- 비즈니스 트리 5개는 각자 `<parent>`로 루트 참조, 고유 의존성 선언.
- runner 8개는 `<parent>`로 루트 참조, `<dependency>`로 해당 business tree 의존.

### 4.2 Contract Test

- `api-contract/contract-tests/` 에 **15개 endpoint (14 common + 1 webflux-only) 에 대한 RestAssured 기반 테스트** 1벌 작성 (WebFlux 전용 endpoint는 해당 runner에만 assert).
- 각 runner의 CI에서 동일 테스트를 자기 포트(8080)로 실행 → 모든 runner가 **같은 계약을 지키는지** 자동 검증.

---

## 5. API Contract (15 endpoints)

### 5.1 공통 endpoint (14개, 모든 runner)

| # | URL | Method | Request | Response | 비고 |
|---|---|---|---|---|---|
| 1 | `/uiadapter/login.do` | POST | `dsSearch{USER_ID, USER_PASSWORD}` | `dsList{LOGIN_RESULT="LOGIN_SUCCESS"}` | **스텁** (검증 없음) |
| 2 | `/uiadapter/select_data_single.do` | POST | `dsSearch` | `dsOutput` (1행) | pattern01 단건 |
| 3 | `/uiadapter/select_datalist.do` | POST | `dsSearch` | `dsList` (다행) | pattern01/02 공용 |
| 4 | `/uiadapter/update_datalist_map.do` | POST | `dsList` (I/U/D rows) | `dsResult` | pattern01 저장 |
| 5 | `/uiadapter/advancedUploadFiles.do?subFolder=` | POST multipart | files[] | `dsResult` | 파일 업로드 |
| 6 | `/uiadapter/advancedDownloadFile.do?subFolder=&...` | GET | query | 파일 바이너리 | 단일 다운로드 |
| 7 | `/uiadapter/multiDownloadFiles.do?subFolder=` | GET | query | zip 스트림 | 다중 다운로드 |
| 8 | `/uiadapter/advancedDownloadList.do?subFolder=` | POST | `dsSearch` | `dsList` | 파일 목록 |
| 9 | `/uiadapter/streamingVideo.do?fileName=&streamType=nio` | GET | query | video/* 스트리밍 | NIO 지원 |
| 10 | `/uiadapter/select_testDataTypeList.do` | POST | `dsSearch` | `dsList` | 타입별 조회 |
| 11 | `/uiadapter/check_testDataTypeList.do` | POST | `dsList` | `dsResult` | 타입 검증 |
| 12 | `/uiadapter/update_deptlist_map.do` | POST | `dsList` (I/U/D) | `dsResult` | I/U/D 저장 |
| 13 | `/uiadapter/sampleLargeData.do` | POST | `dsSearch` | `dsList` (수만 행) | 대용량 |
| 14 | `/uiadapter/search_manyColumn_data.do` | POST | `dsSearch` | `dsList` (광폭) | 대량 컬럼 |

### 5.2 WebFlux 전용 + 대체 구현 (1개)

| # | URL | WebFlux runner | 기타 runner (7개) |
|---|---|---|---|
| 15 | `/uiadapter/relay/exim_exchange.do` | `WebClient` + `Mono` (비동기) | `RestTemplate` 동기 호출 (동일 계약, 다른 구현) |

**구현 배포**:
- `shared-business/jdk{8-javax,17-jakarta}/` → `ExchangeRelayController` (RestTemplate 동기)
- `shared-business-egov{4,5}/` → 동일한 동기 구현 (eGov 특이사항 없음)
- `shared-business-reactive/jdk17-mybatis/` → `ReactiveExchangeRelayController` (WebClient)

### 5.3 Data Format

- 기본: **JSON** (`application/json`)
- nexacro-data-format 스킬 참조: `_RowType_`(`N/I/U/D/O`), `Parameters/Datasets/ColumnInfo/Rows` 구조 준수.
- Request `Content-Type`: `application/json` 또는 `multipart/form-data`(업로드만).

### 5.4 HSQL Schema (seed-data/schema.sql 초안)

```sql
-- 사용자
CREATE TABLE USERS (USER_ID VARCHAR(32) PRIMARY KEY, USER_NAME VARCHAR(64), USER_PASSWORD VARCHAR(64));
INSERT INTO USERS VALUES ('test1', '테스트유저', 'test1');

-- 샘플 (pattern01, pattern02, sampleDataType)
CREATE TABLE SAMPLE_BOARD (ID BIGINT IDENTITY, TITLE VARCHAR(200), CONTENT LONGVARCHAR, CREATED_AT TIMESTAMP);
CREATE TABLE DEPT (DEPT_NO INT PRIMARY KEY, DEPT_NAME VARCHAR(64), LOC VARCHAR(64));

-- 대용량/광폭 (pattern04, sampleBulkColumns)
CREATE TABLE LARGE_DATA (ID BIGINT IDENTITY, /* ... */);
CREATE TABLE WIDE_COLUMNS (ID BIGINT IDENTITY, /* 50+ 컬럼 */);

-- 파일 메타 (sampleFileUpDownload)
CREATE TABLE FILE_META (FILE_ID VARCHAR(64) PRIMARY KEY, SUB_FOLDER VARCHAR(128), FILE_NAME VARCHAR(256), SIZE_BYTES BIGINT, CREATED_AT TIMESTAMP);
```

(상세는 구현 시 기존 GitLab 8개 repo의 SQL을 비교해 **가장 풍부한 쪽을 베이스**로 통합.)

---

## 6. Skill Invocation Flow

```
사용자: /nexacro-fullstack-starter

┌─────────────────────────────────────────────────────────────┐
│ Step 1: 파라미터 수집                                        │
│   - nexacroVersion (현재는 "nexacroN"만)                     │
│   - jdk (8 | 17)                                             │
│   - framework (spring-boot | spring-mvc | egov-boot |        │
│                egov-mvc | webflux)                           │
│   - useEgov (derived from framework)                         │
│   - projectName                                              │
│   - targetDir                                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Matrix 조회 + 파생 변수 계산                         │
│   (jdk, framework) → runner key                              │
│   servletApi, springMajor, bootMajor, egovVersion 파생       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 호환성 체크                                          │
│   - mvc + jdk17 + egov → reject (eGov4 MVC jdk17 미지원)     │
│   - webflux + jdk8 → reject                                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Sparse clone                                         │
│   git clone --filter=blob:none --sparse                      │
│     https://github.com/JasonMMo/nexacroN-fullstack.git       │
│   cd nexacroN-fullstack                                      │
│   git sparse-checkout set                                    │
│     api-contract core nxui samples/seed-data                 │
│     samples/<businessTree> samples/<runnerPath>              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: 타겟 디렉터리로 이동 + 토큰 치환                     │
│   - {{PROJECT_NAME}} → "MyProject"                           │
│   - {{BACKEND_URL}}  → "http://localhost:8080/uiadapter/"    │
│   - {{CONTEXT_PATH}} → "/uiadapter"                          │
│   - pom.xml <artifactId> 갱신                                │
│   - nxui typedefinition.xml svcurl 토큰 치환                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: 후처리                                               │
│   - README.md 생성 (runner별 실행 가이드)                    │
│   - .gitignore                                               │
│   - git init && 초기 커밋 (옵션)                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 7: 사용자 안내                                          │
│   - DB 초기화: mvn exec:java -Dexec.mainClass=...            │
│   - 서버 실행: mvn spring-boot:run (or mvn jetty:run for mvc)│
│   - nexacro IDE: nxui/packageN.xprj 열기                     │
│   - 브라우저 접속: http://localhost:8080/...                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Orchestration Plan (implementation 단계)

> 상세 디스패치는 `writing-plans` 단계에서 확정. 여기는 계층 가이드만.

| 작업 유형 | 담당 | 근거 |
|---|---|---|
| 전체 조율 / 의사결정 / 에이전트 디스패치 / 결과 통합 | Opus (저) | 크로스 컨텍스트 추론 |
| `SKILL.md`, 4개 reference 문서 작성 | Sonnet subagent | 중간 복잡도 글쓰기 |
| `matrix.json` 정의 + 호환성 체크 로직 | Sonnet subagent | 구조적 데이터 |
| nexacroN-fullstack 초기 모노레포 레이아웃 생성 | Sonnet subagent | 파일 다수 + 로직 |
| 기존 GitLab 8 repo → 모노레포 병합 매핑 | Sonnet + Codex 병행 | 정확성 중요 |
| 8 runner POM, web.xml, Application.java 템플릿 | Haiku subagent | 반복 단순 |
| HSQL schema.sql 통합 (8 repo SQL 머지) | Haiku subagent | 기계적 병합 |
| Contract test (RestAssured) 1벌 작성 | Sonnet subagent | 로직 + API 이해 |
| 15 endpoint openapi.yaml 작성 | Sonnet subagent | 스펙 정밀도 |
| API 계약 일관성 / runner-tree 매핑 검증 | `codex:codex-rescue` | 독립 시각 |
| 빌드 검증 (`mvn verify` × 8 runner) | Haiku subagent | 실행 + 로그 분석 |
| 주요 마일스톤 코드 리뷰 | `superpowers:code-reviewer` | 스펙 대비 일치 |

---

## 8. Phased Rollout

### Phase 0 — 준비
- [ ] GitHub `JasonMMo/nexacroN-fullstack` repo 생성 (`gh repo create`)
- [ ] 디렉터리 골격 커밋 (빈 폴더 + README)

### Phase 1 — 플러그인 스캐폴드 (`nexacro-fullstack-starter`)
- [ ] `plugins/nexacro-fullstack-starter/.claude-plugin/plugin.json`
- [ ] `SKILL.md` + `assets/matrix.json` + 4 references
- [ ] `.claude-plugin/marketplace.json`에 신규 plugin 등록 (기존 2개 → 3개)
- [ ] README.md / README-ko.md 업데이트
- [ ] CHANGELOG.md `[1.8.0]` 엔트리

### Phase 2 — 모노레포 본체 구축
- [ ] api-contract/openapi.yaml (15 endpoints: 14 common + 1 webflux-only)
- [ ] core/* 6개 (기존 `nexacro-webflux` 프로젝트의 xapi/xeni/uiadapter 재사용)
- [ ] nxui/ (packageN 원본 복사 + svcurl 토큰화)
- [ ] shared-business/{jdk8-javax, jdk17-jakarta}/
- [ ] shared-business-egov4/jdk8-javax/
- [ ] shared-business-egov5/jdk17-jakarta/
- [ ] shared-business-reactive/jdk17-mybatis/
- [ ] 8 runner 껍데기
- [ ] seed-data (schema.sql, data.sql)
- [ ] contract-tests

### Phase 3 — 기존 GitLab 8 repo 정리
- [ ] 8 repo README에 "이관 공지" + 링크 추가
- [ ] 1~2 스프린트 지켜본 후 아카이브 처리

### Phase 4 — 검증 & 릴리스
- [ ] codex:codex-rescue 검증 (계약 일관성, 매핑 무결성)
- [ ] 8 runner 실빌드/실행 스모크 테스트
- [ ] 플러그인 설치 dry-run
- [ ] v1.8.0 태그 + CHANGELOG 확정

---

## 9. Risks & Mitigations

| Risk | 확률 | 영향 | 완화책 |
|---|---|---|---|
| 기존 GitLab 8 repo 코드가 실제론 서로 다름 (같은 endpoint인데 응답 스키마 다름) | 중 | 고 | Phase 2 시작 시 **8 repo diff** 선행, contract test로 강제 수렴 |
| eGov4 MVC와 eGov4 Boot 소스가 사용자가 인지한 것보다 더 다름 | 중 | 중 | eGov4 MVC runner는 **eGov4 Boot 기준**으로 재작성 (사용자 동의) |
| WebFlux controller에서 `shared-business/jdk17-jakarta` service 재사용 시 트랜잭션/블로킹 이슈 | 중 | 중 | `Mono.fromCallable(...).subscribeOn(boundedElastic())` 래핑, 향후 R2DBC 전환 flag |
| nexacro IDE와 `nxui/` 디렉터리 통합 개발 친화성 | 중 | 중 | `nxui/`는 nexacro IDE 네이티브 구조 유지, Java 코드는 IntelliJ/Eclipse 별도 | 
| 14개 endpoint 중 일부가 실제 GitLab 8 repo에 구현 안 되어 있음 | 저 | 저 | 미구현 endpoint는 **스텁** 제공 (TODO 주석 + 404 반환) |
| `nexacron-fullstack` vs `nexacroN-fullstack` 네이밍 혼선 | 저 | 저 | 모든 공식 참조는 `nexacroN-fullstack` (대문자 N) 사용 — 이 스펙이 진실 원천 |

---

## 10. Open Questions / TODOs

- [ ] `gh repo create` 시 `--public` 여부 확인 (현재 8 repo가 public이므로 동일하게 public 가정)
- [ ] HSQL 데이터 초기화 방식: Spring Boot `schema.sql` auto-load vs 별도 `@PostConstruct` 초기화 → 후자 권장 (MVC runner도 동일 메커니즘 사용 가능)
- [ ] MVC runner는 Tomcat `war` 배포 vs `embedded jetty` 실행 → 개발 UX 위해 `mvn jetty:run` 권장
- [ ] `nxui/packageN.xprj` 파일 안의 절대경로 참조가 있는지 선검증 필요 (있으면 상대경로 또는 토큰화)
- [ ] Contract test가 **동일한 JSON** 을 기대하므로, 8 runner 모두 Jackson 설정 통일 (e.g. `SNAKE_CASE`, date format)

---

## 11. Acceptance Criteria

다음이 모두 충족되면 v1.8.0 릴리스 가능:

1. `/plugin install nexacro-fullstack-starter@nexacro-claude-skills` 후 `/nexacro-fullstack-starter` 호출이 8가지 조건 조합을 모두 처리.
2. 각 조합 결과물에서 `mvn verify` 통과 (contract test 포함).
3. 각 조합 결과물 실행 후 `http://localhost:8080/uiadapter/` 로 nxui 접속 시 8개 샘플 메뉴가 모두 동작.
4. `nexacroN-fullstack` 모노레포 업데이트 1회로 8 runner가 자동 반영 (drift test 통과).
5. codex:codex-rescue 독립 검증 통과.

---

## 12. References

- 기존 플러그인: `plugins/nexacro-claude-skills/`, `plugins/nexacro-webflux-port/`
- 원본 packageN: `D:\AI\reference\Nexacro24\Sample\packageN`
- nexacro-data-format 규칙: `.claude/rules/nexacro-data-format.md`
- nexacro-webflux-port 레퍼런스 (multipart, ServletProvider 등): `plugins/nexacro-webflux-port/skills/nexacro-webflux-port/references/*`

---

## 13. Changelog of this spec

- 2026-04-23: Draft v1 — brainstorming 결과 반영 (C'''''' architecture, 5 business trees + 8 runners, 14 endpoints, nexacroN-fullstack repo, stub login, exchange-relay alt impl).
