# Plan 1 — nexacro-fullstack-starter Plugin + Monorepo Skeleton

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an installable `nexacro-fullstack-starter` plugin (v1.8.0) with a newly-created `nexacroN-fullstack` GitHub repo containing enough skeleton (api-contract, parent POM, placeholder trees) for the plugin's clone flow to succeed end-to-end.

**Architecture:** Two-repo design. Repo 1 (`nexacro-claude-skills`) hosts the plugin definition (SKILL.md + matrix.json + references). Repo 2 (`nexacroN-fullstack`, new) holds the real code; Plan 1 puts only the skeleton in place (empty trees + README per folder + api-contract/openapi.yaml stub). Subsequent plans fill the bodies.

**Tech Stack:** Claude Code plugin (skill YAML frontmatter + markdown), JSON (matrix + plugin manifests), bash (git, gh CLI), Maven (parent POM), OpenAPI 3 (api-contract).

**Spec:** `D:\AI\workspace\nexacro-claude-skills\docs\superpowers\specs\2026-04-23-nexacro-fullstack-starter-design.md`

**Orchestration model:**
- Opus (this session) = coordination + task dispatch
- Sonnet subagents (`general-purpose` with `model: sonnet`) = authoring SKILL.md, references, openapi.yaml
- Haiku subagents (`general-purpose` with `model: haiku`) = repetitive file creation, validation runs
- `codex:codex-rescue` = independent structural verification at key milestones

---

## File Structure

### Repo 1 — `D:\AI\workspace\nexacro-claude-skills` (existing)

**New files (Plan 1)**:
```
plugins/nexacro-fullstack-starter/
├── .claude-plugin/
│   └── plugin.json                                     [new]
└── skills/
    └── nexacro-fullstack-starter/
        ├── SKILL.md                                    [new]
        ├── assets/
        │   └── matrix.json                             [new]
        └── references/
            ├── compatibility-matrix.md                 [new]
            ├── repo-map.md                             [new]
            ├── runner-selection-guide.md               [new]
            └── troubleshooting.md                      [new]
```

**Modified files (Plan 1)**:
```
.claude-plugin/marketplace.json                         [modify: register new plugin]
README.md                                               [modify: add nexacro-fullstack-starter section]
README-ko.md                                            [modify: 동일]
CHANGELOG.md                                            [modify: v1.8.0 entry]
```

### Repo 2 — `D:\AI\workspace\nexacroN-fullstack` (NEW, local clone of new GitHub repo)

**New files (Plan 1 — skeleton only)**:
```
nexacroN-fullstack/
├── README.md
├── LICENSE                                             (MIT)
├── .gitignore
├── pom.xml                                             (parent BOM)
├── api-contract/
│   ├── openapi.yaml                                    (15 endpoints stub)
│   ├── data-formats.md
│   └── README.md
├── core/
│   └── README.md                                       (placeholder only — real content in Plan 2)
├── nxui/
│   └── README.md                                       (placeholder only — Plan 3)
└── samples/
    ├── README.md
    ├── seed-data/
    │   ├── schema.sql                                  (basic DDL)
    │   ├── data.sql                                    (basic seed)
    │   └── README.md
    ├── shared-business/README.md                       (placeholder — Plan 2)
    ├── shared-business-egov4/README.md                 (placeholder — Plan 2)
    ├── shared-business-egov5/README.md                 (placeholder — Plan 2)
    ├── shared-business-reactive/README.md              (placeholder — Plan 2)
    └── runners/README.md                               (placeholder — Plan 2)
```

---

## Phase 0 — GitHub Repo Provisioning

### Task 0.1: Verify prerequisites

**Files:** none

- [ ] **Step 1: Confirm `gh` CLI is installed and authenticated**

Run:
```bash
gh auth status
```
Expected: `✓ Logged in to github.com account JasonMMo`

If not authenticated, run `gh auth login` interactively before proceeding.

- [ ] **Step 2: Confirm no existing repo conflicts**

Run:
```bash
gh repo view JasonMMo/nexacroN-fullstack 2>&1 | head -1
```
Expected: `GraphQL: Could not resolve to a Repository with the name 'JasonMMo/nexacroN-fullstack'.` (error is good — means name is available)

If the repo already exists, stop and consult user before proceeding.

---

### Task 0.2: Create GitHub repo

**Files:** none (remote action)

- [ ] **Step 1: Create the public repo**

Run:
```bash
gh repo create JasonMMo/nexacroN-fullstack --public --description "nexacroN full-stack monorepo — nxui (packageN) + 8 Spring runners (MVC/Boot/eGov4/eGov5/WebFlux) sharing an API contract" --license MIT
```
Expected: `✓ Created repository JasonMMo/nexacroN-fullstack on GitHub`

- [ ] **Step 2: Clone locally**

Run:
```bash
cd D:\AI\workspace
git clone https://github.com/JasonMMo/nexacroN-fullstack.git
cd nexacroN-fullstack
```
Expected: directory `D:\AI\workspace\nexacroN-fullstack\` exists with `.git/` and `LICENSE` (from `--license MIT`).

---

### Task 0.3: Seed initial .gitignore + README

**Files:**
- Create: `D:\AI\workspace\nexacroN-fullstack\.gitignore`
- Create: `D:\AI\workspace\nexacroN-fullstack\README.md`

- [ ] **Step 1: Write `.gitignore`**

Content:
```gitignore
# Maven
target/
dependency-reduced-pom.xml
*.class

# IDEs
.idea/
.vscode/
*.iml
.project
.classpath
.settings/
bin/

# Nexacro IDE
*.bak
.swp

# OS
.DS_Store
Thumbs.db
desktop.ini

# HSQL embedded DB files
*.log
*.script
*.data
*.properties.db
*.tmp/

# Local overrides
*.local
.env
.env.local
```

- [ ] **Step 2: Write root `README.md`**

Content:
```markdown
# nexacroN-fullstack

End-to-end monorepo for Nexacro N v24 + Spring server stacks. Single `packageN` nxui front-end driving a matrix of 8 server runners that share an OpenAPI contract.

## Structure

| Folder | Purpose |
|---|---|
| `api-contract/` | OpenAPI spec + data-format reference (source of truth for 15 endpoints) |
| `core/` | Nexacro xapi / xeni / uiadapter in `javax` and `jakarta` variants |
| `nxui/` | `packageN` front-end project (xprj + xadl + xfdl forms) |
| `samples/seed-data/` | HSQL schema + seed data |
| `samples/shared-business/` | Plain Spring business code (jdk8-javax + jdk17-jakarta) |
| `samples/shared-business-egov4/` | eGov 4.x business code (jdk8-javax) |
| `samples/shared-business-egov5/` | eGov 5.x business code (jdk17-jakarta) |
| `samples/shared-business-reactive/` | WebFlux controller layer (reuses `shared-business/jdk17-jakarta` service/mapper) |
| `samples/runners/` | 8 thin entry-point modules (POM + Application/web.xml only) |

## Runner matrix

| Runner | JDK | servlet-api | Framework | eGov |
|---|---|---|---|---|
| `boot-jdk17-jakarta` | 17 | jakarta | Spring Boot 3 | — |
| `boot-jdk8-javax` | 8 | javax | Spring Boot 2 | — |
| `mvc-jdk17-jakarta` | 17 | jakarta | Spring 6 (war) | — |
| `mvc-jdk8-javax` | 8 | javax | Spring 5 (war) | — |
| `egov5-boot-jdk17-jakarta` | 17 | jakarta | Boot 3 | 5.x |
| `egov4-boot-jdk8-javax` | 8 | javax | Boot 2 | 4.x |
| `egov4-mvc-jdk8-javax` | 8 | javax | Spring 5 (war) | 4.x |
| `webflux-jdk17-jakarta` | 17 | jakarta | WebFlux (Boot 3) | — |

## Quick start (via Claude Code)

```
/plugin marketplace add JasonMMo/nexacro-claude-skills
/plugin install nexacro-fullstack-starter@nexacro-claude-skills
/nexacro-fullstack-starter
```

The skill will clone the runner(s) you select into your target directory.

## License

MIT — see `LICENSE`.
```

- [ ] **Step 3: Validate markdown renders**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
head -20 README.md
```
Expected: first heading `# nexacroN-fullstack` visible, no escaping issues.

- [ ] **Step 4: Commit + push**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
git add .gitignore
git commit -m "chore: add .gitignore"
git add README.md
git commit -m "docs: add root README with monorepo overview"
git push origin main
```
Expected: both commits show on GitHub at `https://github.com/JasonMMo/nexacroN-fullstack`.

---

## Phase 1 — Plugin scaffolding (`nexacro-fullstack-starter`)

### Task 1.1: Create plugin directory structure

**Files:**
- Create: `D:\AI\workspace\nexacro-claude-skills\plugins\nexacro-fullstack-starter\.claude-plugin\`
- Create: `D:\AI\workspace\nexacro-claude-skills\plugins\nexacro-fullstack-starter\skills\nexacro-fullstack-starter\assets\`
- Create: `D:\AI\workspace\nexacro-claude-skills\plugins\nexacro-fullstack-starter\skills\nexacro-fullstack-starter\references\`

- [ ] **Step 1: Create directories**

Run:
```bash
cd D:\AI\workspace\nexacro-claude-skills
mkdir -p plugins/nexacro-fullstack-starter/.claude-plugin
mkdir -p plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets
mkdir -p plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references
```
Expected: no output.

- [ ] **Step 2: Verify structure**

Run:
```bash
ls -la plugins/nexacro-fullstack-starter/
ls -la plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/
```
Expected: `.claude-plugin/` and `skills/` at first level; `assets/` and `references/` under skill folder.

---

### Task 1.2: Write `plugin.json`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/.claude-plugin/plugin.json`

- [ ] **Step 1: Write the file**

Content:
```json
{
  "name": "nexacro-fullstack-starter",
  "version": "0.1.0",
  "description": "Scaffolds a full-stack Nexacro N v24 project: packageN nxui + Spring server (Boot/MVC/eGov/WebFlux) picked from a jdk × framework matrix. Clones the nexacroN-fullstack monorepo and extracts the combination you select.",
  "author": {
    "name": "JasonMMo",
    "url": "https://github.com/JasonMMo"
  },
  "homepage": "https://github.com/JasonMMo/nexacro-claude-skills",
  "repository": "https://github.com/JasonMMo/nexacro-claude-skills",
  "license": "MIT",
  "keywords": [
    "nexacro",
    "nexacroN",
    "fullstack",
    "scaffold",
    "starter",
    "spring-boot",
    "spring-mvc",
    "spring-webflux",
    "egovframework",
    "mybatis",
    "hsql",
    "korean-support"
  ]
}
```

- [ ] **Step 2: Validate JSON parses**

Run:
```bash
python -c "import json; json.load(open('plugins/nexacro-fullstack-starter/.claude-plugin/plugin.json', encoding='utf-8')); print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/.claude-plugin/plugin.json
git commit -m "feat(nexacro-fullstack-starter): add plugin.json v0.1.0"
```

---

### Task 1.3: Write `matrix.json`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json`

- [ ] **Step 1: Write the file**

Content:
```json
{
  "version": "1",
  "repoDefaults": {
    "host": "github.com",
    "owner": "JasonMMo"
  },
  "nexacroVersions": {
    "nexacroN": {
      "repo": "https://github.com/JasonMMo/nexacroN-fullstack.git",
      "branch": "main",
      "alwaysInclude": [
        "api-contract",
        "core",
        "nxui",
        "pom.xml",
        "README.md",
        "LICENSE",
        ".gitignore",
        "samples/seed-data"
      ],
      "runners": {
        "boot-jdk17-jakarta": {
          "businessTree": "samples/shared-business/jdk17-jakarta",
          "runnerPath": "samples/runners/boot-jdk17-jakarta",
          "jdk": 17,
          "servletApi": "jakarta",
          "framework": "spring-boot",
          "springMajor": 6,
          "bootMajor": 3,
          "egovMajor": null,
          "packaging": "jar",
          "runCmd": "mvn spring-boot:run"
        },
        "boot-jdk8-javax": {
          "businessTree": "samples/shared-business/jdk8-javax",
          "runnerPath": "samples/runners/boot-jdk8-javax",
          "jdk": 8,
          "servletApi": "javax",
          "framework": "spring-boot",
          "springMajor": 5,
          "bootMajor": 2,
          "egovMajor": null,
          "packaging": "jar",
          "runCmd": "mvn spring-boot:run"
        },
        "mvc-jdk17-jakarta": {
          "businessTree": "samples/shared-business/jdk17-jakarta",
          "runnerPath": "samples/runners/mvc-jdk17-jakarta",
          "jdk": 17,
          "servletApi": "jakarta",
          "framework": "spring-mvc",
          "springMajor": 6,
          "bootMajor": null,
          "egovMajor": null,
          "packaging": "war",
          "runCmd": "mvn jetty:run"
        },
        "mvc-jdk8-javax": {
          "businessTree": "samples/shared-business/jdk8-javax",
          "runnerPath": "samples/runners/mvc-jdk8-javax",
          "jdk": 8,
          "servletApi": "javax",
          "framework": "spring-mvc",
          "springMajor": 5,
          "bootMajor": null,
          "egovMajor": null,
          "packaging": "war",
          "runCmd": "mvn jetty:run"
        },
        "egov5-boot-jdk17-jakarta": {
          "businessTree": "samples/shared-business-egov5/jdk17-jakarta",
          "runnerPath": "samples/runners/egov5-boot-jdk17-jakarta",
          "jdk": 17,
          "servletApi": "jakarta",
          "framework": "egov-boot",
          "springMajor": 6,
          "bootMajor": 3,
          "egovMajor": 5,
          "packaging": "jar",
          "runCmd": "mvn spring-boot:run"
        },
        "egov4-boot-jdk8-javax": {
          "businessTree": "samples/shared-business-egov4/jdk8-javax",
          "runnerPath": "samples/runners/egov4-boot-jdk8-javax",
          "jdk": 8,
          "servletApi": "javax",
          "framework": "egov-boot",
          "springMajor": 5,
          "bootMajor": 2,
          "egovMajor": 4,
          "packaging": "jar",
          "runCmd": "mvn spring-boot:run"
        },
        "egov4-mvc-jdk8-javax": {
          "businessTree": "samples/shared-business-egov4/jdk8-javax",
          "runnerPath": "samples/runners/egov4-mvc-jdk8-javax",
          "jdk": 8,
          "servletApi": "javax",
          "framework": "egov-mvc",
          "springMajor": 5,
          "bootMajor": null,
          "egovMajor": 4,
          "packaging": "war",
          "runCmd": "mvn jetty:run"
        },
        "webflux-jdk17-jakarta": {
          "businessTree": "samples/shared-business-reactive/jdk17-mybatis",
          "runnerPath": "samples/runners/webflux-jdk17-jakarta",
          "jdk": 17,
          "servletApi": "jakarta",
          "framework": "webflux",
          "springMajor": 6,
          "bootMajor": 3,
          "egovMajor": null,
          "packaging": "jar",
          "runCmd": "mvn spring-boot:run"
        }
      },
      "rejectedCombinations": [
        {
          "match": { "framework": "egov-mvc", "jdk": 17 },
          "reason": "eGov4 MVC on jdk17/jakarta is not supported — no corresponding sample project exists. Use egov5-boot-jdk17-jakarta instead."
        },
        {
          "match": { "framework": "webflux", "jdk": 8 },
          "reason": "WebFlux requires jdk17+ jakarta. Use boot-jdk8-javax for jdk8."
        }
      ],
      "derivationRules": {
        "servletApi": "jdk >= 17 ? 'jakarta' : 'javax'",
        "springMajor": "servletApi == 'jakarta' ? 6 : 5",
        "bootMajor": "framework in [spring-boot, egov-boot, webflux] ? (servletApi == 'jakarta' ? 3 : 2) : null",
        "egovMajor": "framework == 'egov-boot' ? (servletApi == 'jakarta' ? 5 : 4) : (framework == 'egov-mvc' ? 4 : null)"
      },
      "tokens": {
        "{{PROJECT_NAME}}": "user-supplied project name (alphanumeric + dash, no spaces)",
        "{{BACKEND_URL}}": "http://localhost:8080/uiadapter/",
        "{{CONTEXT_PATH}}": "/uiadapter",
        "{{SERVER_PORT}}": "8080"
      }
    }
  }
}
```

- [ ] **Step 2: Validate JSON + runner key naming consistency**

Run:
```bash
python -c "
import json
m = json.load(open('plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json', encoding='utf-8'))
runners = m['nexacroVersions']['nexacroN']['runners']
for key, cfg in runners.items():
    assert cfg['runnerPath'].endswith(key), f'Key {key} does not match runnerPath {cfg[\"runnerPath\"]}'
print(f'OK ({len(runners)} runners validated)')
"
```
Expected: `OK (8 runners validated)`

- [ ] **Step 3: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json
git commit -m "feat(nexacro-fullstack-starter): add matrix.json with 8 nexacroN runners"
```

---

### Task 1.4: Write `SKILL.md`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md`

> **Dispatch to Sonnet subagent** — this file is ~300 lines of Korean + English prose; Sonnet produces higher quality than Haiku for mixed-language documentation.

- [ ] **Step 1: Write the file**

Content:
```markdown
---
name: nexacro-fullstack-starter
description: Scaffolds a full-stack Nexacro N v24 project (packageN nxui + Spring server) picked from a jdk × framework × eGov matrix. Clones the nexacroN-fullstack monorepo and extracts the runner you select.
argument-hint: "[--jdk 8|17] [--framework spring-boot|spring-mvc|egov-boot|egov-mvc|webflux] [--name <project-name>] [--dir <target-dir>]"
---

# Nexacro Fullstack Starter

Scaffold a ready-to-run Nexacro N v24 project in one step. You pick (JDK, framework, eGov?) — the skill picks the runner, clones the monorepo, strips everything you don't need, substitutes tokens, and hands you a working project.

## 개요 / Overview

- **입력**: jdk 버전, 프레임워크, (eGov 사용 여부), 프로젝트 이름
- **출력**: nxui + Spring 서버가 들어있는 독립 프로젝트 디렉터리
- **소스**: `github.com/JasonMMo/nexacroN-fullstack` (clone 후 sparse-checkout)
- **매트릭스**: `assets/matrix.json` (현재 8개 runner 등록)

## Step 1 — 파라미터 수집 / Collect parameters

### 1-1. 필수 4개 입력

아래 순서로 한 번에 하나씩 질문합니다. CLI 아규먼트(`--jdk`, `--framework` 등)로 전달된 값은 이미 받은 것으로 간주하고 건너뜁니다.

```
[1/5] nexacro 버전 / nexacro version
      기본값: nexacroN
      선택지: nexacroN (현재는 nexacroN 만 지원)

[2/5] JDK 버전 / JDK version
      선택지: 8 | 17
      - 8  → Spring 5 / javax / Boot 2 / eGov4
      - 17 → Spring 6 / jakarta / Boot 3 / eGov5

[3/5] 프레임워크 / Framework
      선택지:
      - spring-boot  (Spring Boot 기본 - embedded Tomcat)
      - spring-mvc   (전통 MVC - war 배포)
      - egov-boot    (표준프레임워크 Boot)
      - egov-mvc     (표준프레임워크 MVC - jdk8만 지원)
      - webflux      (Spring WebFlux - jdk17만 지원)

[4/5] 프로젝트 이름 / Project name
      예: my-nexacro-app
      제약: 영숫자 + 하이픈만, 공백 불가

[5/5] 타겟 디렉터리 / Target directory
      기본값: ./{{PROJECT_NAME}}
      경고: 이미 존재하면 중단 (덮어쓰기 안 함)
```

### 1-2. 파생 변수 계산

`assets/matrix.json` 의 `derivationRules` 로 파생:

| 변수 | 규칙 |
|---|---|
| `servletApi` | `jdk >= 17 ? "jakarta" : "javax"` |
| `springMajor` | `servletApi == "jakarta" ? 6 : 5` |
| `bootMajor` | `framework ∈ {spring-boot, egov-boot, webflux} ? (jakarta ? 3 : 2) : null` |
| `egovMajor` | `framework == "egov-boot" ? (jakarta ? 5 : 4) : (framework == "egov-mvc" ? 4 : null)` |

### 1-3. runner key 결정

`(framework, jdk)` 조합으로 runner key 계산 — 상세는 `references/runner-selection-guide.md` 참고.

예:
- `(spring-boot, 17)` → `boot-jdk17-jakarta`
- `(egov-mvc, 8)` → `egov4-mvc-jdk8-javax`
- `(webflux, 17)` → `webflux-jdk17-jakarta`

## Step 2 — 호환성 체크 / Compatibility check

`assets/matrix.json` 의 `rejectedCombinations` 를 순회하며 요청 조합이 매치되면 **거부**하고 사유와 대안을 출력합니다.

현재 거부 조합:
1. `framework=egov-mvc + jdk=17` — eGov4 MVC jdk17 미지원 → `egov5-boot-jdk17-jakarta` 권장
2. `framework=webflux + jdk=8` — WebFlux는 jdk17+ 전용 → `boot-jdk8-javax` 권장

호환성 통과 시 확정된 runner key 및 파생 변수 전체를 사용자에게 **재확인**합니다:

```
🎯 확정 구성 / Confirmed configuration
────────────────────────────────────────
nexacro:    nexacroN
runner:     boot-jdk17-jakarta
jdk:        17
servletApi: jakarta
framework:  spring-boot
bootMajor:  3
springMajor: 6
egovMajor:  (none)
────────────────────────────────────────
이대로 진행할까요? / Proceed? (y/n)
```

## Step 3 — Sparse clone

### 3-1. 임시 디렉터리로 전체 clone (sparse)

```bash
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"
git clone --filter=blob:none --sparse https://github.com/JasonMMo/nexacroN-fullstack.git
cd nexacroN-fullstack
```

### 3-2. 선택된 경로만 체크아웃

matrix.json 의 `alwaysInclude` + 선택된 `businessTree` + `runnerPath` 를 조합:

```bash
git sparse-checkout set \
  api-contract core nxui pom.xml README.md LICENSE .gitignore \
  samples/seed-data \
  samples/shared-business/jdk17-jakarta \
  samples/runners/boot-jdk17-jakarta
```

### 3-3. 타겟 디렉터리로 복사

```bash
cp -r "$TMP_DIR/nexacroN-fullstack/." "${TARGET_DIR}/"
rm -rf "$TMP_DIR"
cd "${TARGET_DIR}"
rm -rf .git  # 신규 git init 을 위해 히스토리 제거
```

## Step 4 — 토큰 치환 / Token substitution

`matrix.json` 의 `tokens` 를 순회하며 타겟 디렉터리의 모든 텍스트 파일에서 `{{TOKEN}}` 을 실제 값으로 치환합니다.

| 토큰 | 치환 값 |
|---|---|
| `{{PROJECT_NAME}}` | 사용자 입력 프로젝트명 |
| `{{BACKEND_URL}}` | `http://localhost:8080/uiadapter/` |
| `{{CONTEXT_PATH}}` | `/uiadapter` |
| `{{SERVER_PORT}}` | `8080` |

추가로 Maven 아티팩트 ID 도 업데이트:

```bash
# pom.xml 들의 <artifactId>{{PROJECT_NAME}}</artifactId> 치환
find . -name "pom.xml" -exec sed -i "s|{{PROJECT_NAME}}|${PROJECT_NAME}|g" {} \;
```

> Windows 환경에서는 `sed -i` 대신 Python 스크립트 사용 (references/troubleshooting.md 참고).

## Step 5 — 후처리 / Post-processing

### 5-1. 프로젝트 전용 README 생성

타겟 디렉터리에 사용자 설정이 반영된 `README.md` 덮어쓰기:

```markdown
# {{PROJECT_NAME}}

Generated by `nexacro-fullstack-starter` plugin.

- **nexacro version**: nexacroN
- **runner**: {{RUNNER_KEY}}
- **jdk**: {{JDK}}
- **framework**: {{FRAMEWORK}}

## Run

1. 서버 실행: `cd samples/runners/{{RUNNER_KEY}} && {{RUN_CMD}}`
2. nexacro IDE 에서 `nxui/packageN.xprj` 열기
3. 브라우저: http://localhost:8080/uiadapter/

## Docs

- API contract: `api-contract/openapi.yaml`
- Seed data: `samples/seed-data/`
```

### 5-2. 초기 커밋 (옵션)

```bash
git init
git add .
git commit -m "chore: scaffolded from nexacro-fullstack-starter"
```

사용자에게 물어보고 진행 (기본값: yes).

## Step 6 — 사용자 안내 / Final guidance

실행 요약 출력:

```
✅ 프로젝트 생성 완료 / Scaffold complete
─────────────────────────────────────
경로:     ./{{PROJECT_NAME}}
runner:   {{RUNNER_KEY}}
─────────────────────────────────────

다음 단계 / Next steps:
  1. DB 초기화:   (seed-data 는 서버 첫 실행 시 자동 로드)
  2. 서버 실행:   cd samples/runners/{{RUNNER_KEY}}
                 {{RUN_CMD}}
  3. nexacro IDE: nxui/packageN.xprj 열기
  4. 브라우저:    http://localhost:8080/uiadapter/

문제 발생 시 references/troubleshooting.md 참고.
```

## 참고 / References

- `references/compatibility-matrix.md` — 매트릭스 전체 + 파생 규칙 상세
- `references/repo-map.md` — `nexacroN-fullstack` 모노레포 트리 설명
- `references/runner-selection-guide.md` — 어떤 runner 를 골라야 하는지 가이드
- `references/troubleshooting.md` — 자주 발생하는 이슈 (port 충돌, JDK mismatch, war 배포)
```

- [ ] **Step 2: Validate frontmatter parses**

Run:
```bash
python -c "
import re
content = open('plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md', encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
assert m, 'Frontmatter missing'
fm = m.group(1)
assert 'name: nexacro-fullstack-starter' in fm
assert 'description:' in fm
assert 'argument-hint:' in fm
print('OK frontmatter valid')
"
```
Expected: `OK frontmatter valid`

- [ ] **Step 3: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md
git commit -m "feat(nexacro-fullstack-starter): add SKILL.md with 6-step scaffolding flow"
```

---

### Task 1.5: Write `references/compatibility-matrix.md`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/compatibility-matrix.md`

- [ ] **Step 1: Write the file**

Content:
```markdown
# Compatibility Matrix Reference

Derivation rules and the current 8-runner matrix for `nexacroN-fullstack`.

## Derivation rules

User picks 4 values. Everything else is derived.

```
User picks:  nexacroVersion (= nexacroN), jdk, framework, projectName

Derived:
  servletApi   = (jdk >= 17) ? "jakarta" : "javax"
  springMajor  = (servletApi == "jakarta") ? 6 : 5
  bootMajor    = framework ∈ {spring-boot, egov-boot, webflux}
                   ? (servletApi == "jakarta" ? 3 : 2)
                   : null
  egovMajor    = (framework == "egov-boot")
                   ? (servletApi == "jakarta" ? 5 : 4)
                   : (framework == "egov-mvc") ? 4 : null
  packaging    = framework ∈ {spring-mvc, egov-mvc} ? "war" : "jar"
```

## 8-runner matrix (nexacroN)

| # | runner key | jdk | servletApi | framework | springMajor | bootMajor | egovMajor | packaging |
|---|---|---|---|---|---|---|---|---|
| 1 | `boot-jdk17-jakarta` | 17 | jakarta | spring-boot | 6 | 3 | — | jar |
| 2 | `boot-jdk8-javax` | 8 | javax | spring-boot | 5 | 2 | — | jar |
| 3 | `mvc-jdk17-jakarta` | 17 | jakarta | spring-mvc | 6 | — | — | war |
| 4 | `mvc-jdk8-javax` | 8 | javax | spring-mvc | 5 | — | — | war |
| 5 | `egov5-boot-jdk17-jakarta` | 17 | jakarta | egov-boot | 6 | 3 | 5 | jar |
| 6 | `egov4-boot-jdk8-javax` | 8 | javax | egov-boot | 5 | 2 | 4 | jar |
| 7 | `egov4-mvc-jdk8-javax` | 8 | javax | egov-mvc | 5 | — | 4 | war |
| 8 | `webflux-jdk17-jakarta` | 17 | jakarta | webflux | 6 | 3 | — | jar |

## Business tree sharing

Runners share JVM source where structure is identical.

| Business tree | Shared by runners |
|---|---|
| `samples/shared-business/jdk8-javax` | `boot-jdk8-javax`, `mvc-jdk8-javax` |
| `samples/shared-business/jdk17-jakarta` | `boot-jdk17-jakarta`, `mvc-jdk17-jakarta` |
| `samples/shared-business-egov4/jdk8-javax` | `egov4-boot-jdk8-javax`, `egov4-mvc-jdk8-javax` |
| `samples/shared-business-egov5/jdk17-jakarta` | `egov5-boot-jdk17-jakarta` |
| `samples/shared-business-reactive/jdk17-mybatis` | `webflux-jdk17-jakarta` |

→ 5 trees, 8 runners. Edit business logic once, all matching runners pick it up.

## Rejected combinations

Checked in Step 2 of SKILL.md.

| Input | Reason | Alternative |
|---|---|---|
| `framework=egov-mvc + jdk=17` | eGov4 MVC jdk17/jakarta sample does not exist | `egov5-boot-jdk17-jakarta` |
| `framework=webflux + jdk=8` | WebFlux requires jdk17+ jakarta | `boot-jdk8-javax` |
| `nexacroVersion ≠ nexacroN` | Only nexacroN is implemented in v0.1.0 | wait for `nexacro17-fullstack` / `nexacro14-fullstack` (future) |

## servletApi cross-reference

| jdk | servlet-api | javax → jakarta import changes |
|---|---|---|
| 8, 11 | `javax.servlet.*` | uses `javax.servlet.http.HttpServletRequest` |
| 17+ | `jakarta.servlet.*` | uses `jakarta.servlet.http.HttpServletRequest` |

This alone forces per-JDK business trees (cannot share source across `javax`/`jakarta`).
```

- [ ] **Step 2: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/compatibility-matrix.md
git commit -m "docs(nexacro-fullstack-starter): add compatibility-matrix.md"
```

---

### Task 1.6: Write `references/repo-map.md`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/repo-map.md`

- [ ] **Step 1: Write the file**

Content:
```markdown
# nexacroN-fullstack Repo Map

Layout of the monorepo that the skill clones. Shows which pieces each runner consumes.

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
```

- [ ] **Step 2: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/repo-map.md
git commit -m "docs(nexacro-fullstack-starter): add repo-map.md"
```

---

### Task 1.7: Write `references/runner-selection-guide.md`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/runner-selection-guide.md`

- [ ] **Step 1: Write the file**

Content:
```markdown
# Runner Selection Guide

어떤 runner를 골라야 할지 모를 때 보는 의사결정 가이드.

## Decision tree

```
Q1. JDK 버전이 17 이상인가?
├── Yes (17+) ──► servletApi = jakarta
│   │
│   Q2. WebFlux reactive 구현이 필요한가?
│   ├── Yes ──► webflux-jdk17-jakarta
│   └── No
│       │
│       Q3. eGov 표준프레임워크 사용?
│       ├── Yes ──► egov5-boot-jdk17-jakarta  (eGov 5.x)
│       └── No
│           │
│           Q4. war 패키징(전통 MVC) 필요?
│           ├── Yes ──► mvc-jdk17-jakarta
│           └── No  ──► boot-jdk17-jakarta   ★ 대부분 이것
│
└── No (8/11) ──► servletApi = javax
    │
    Q2'. eGov 표준프레임워크 사용?
    ├── Yes
    │   │
    │   Q3'. war 패키징?
    │   ├── Yes ──► egov4-mvc-jdk8-javax
    │   └── No  ──► egov4-boot-jdk8-javax
    │
    └── No
        │
        Q3'. war 패키징?
        ├── Yes ──► mvc-jdk8-javax
        └── No  ──► boot-jdk8-javax
```

## "어떤 걸 고를지 모르겠다" — 기본값 추천

| 상황 | 추천 runner | 이유 |
|---|---|---|
| 신규 프로젝트, 제약 없음 | `boot-jdk17-jakarta` | 최신 스택, 가장 간단한 실행 (`mvn spring-boot:run`) |
| 기존 jdk8 환경 유지 필요 | `boot-jdk8-javax` | javax 기반 레거시 호환 |
| 공공기관 프로젝트 | `egov5-boot-jdk17-jakarta` | 표준프레임워크 최신 |
| 공공기관 jdk8 필수 | `egov4-boot-jdk8-javax` | 표준프레임워크 4.x |
| 레거시 war 배포 서버 | `mvc-jdk{8|17}-{javax|jakarta}` | 전통 Tomcat war |
| 대용량 비동기 / 스트리밍 | `webflux-jdk17-jakarta` | Reactive, 단 학습 곡선 있음 |

## WebFlux 를 고르기 전 체크리스트

WebFlux는 개발 진입장벽이 있으니 아래를 확인하세요:

- [ ] 반드시 비동기/논블로킹 필요한가? (대부분의 CRUD 업무는 Boot로 충분)
- [ ] 팀이 `Mono<>`/`Flux<>` 패턴에 익숙한가?
- [ ] MyBatis 사용 고수? (WebFlux + MyBatis 는 동기 래핑 한계 존재)
- [ ] 예외 처리, 트랜잭션 재설계 시간이 있는가?

하나라도 "아니오" 면 `boot-jdk17-jakarta` 가 안전합니다.

## 호환성 미매치 사례

### "egov-mvc + jdk17" 를 시도한 경우

→ Step 2 에서 거부됨. 이유: eGov4 MVC + jdk17/jakarta 공식 샘플 미존재.
→ 대안 추천: `egov5-boot-jdk17-jakarta` (eGov 최신 + Boot 3)

### "webflux + jdk8" 를 시도한 경우

→ Step 2 에서 거부됨. 이유: WebFlux는 Spring 6/jakarta/jdk17+ 조합만 지원.
→ 대안 추천: `boot-jdk8-javax` (동기 Boot 2)

## 추후 지원 예정

- `nexacro17-fullstack` — nexacro17 버전 (별도 repo)
- `nexacro14-fullstack` — nexacro14 버전 (별도 repo)
- `egov4-mvc-jdk17-jakarta` — 요청 받으면 추가 검토
- R2DBC 기반 reactive — `webflux-jdk17-jakarta-r2dbc` 신규 runner로 추가
```

- [ ] **Step 2: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/runner-selection-guide.md
git commit -m "docs(nexacro-fullstack-starter): add runner-selection-guide.md"
```

---

### Task 1.8: Write `references/troubleshooting.md`

**Files:**
- Create: `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/troubleshooting.md`

- [ ] **Step 1: Write the file**

Content:
```markdown
# Troubleshooting

자주 발생하는 이슈와 해결법.

## 설치/호출 단계

### `gh` 미인증

증상: `git clone` 단계에서 `remote: Repository not found` 또는 HTTPS 자격 증명 실패.

해결:
```bash
gh auth login
# or for public clone only
git config --global credential.helper manager-core
```

### Windows 에서 `sed -i` 실패

증상: 토큰 치환 단계에서 `sed: -i may not be used with stdin`.

해결: `sed -i` 대신 Python 사용.
```bash
python -c "
import pathlib, sys
for p in pathlib.Path('.').rglob('*'):
    if not p.is_file() or p.suffix in {'.jar','.class','.zip','.png','.jpg'}: continue
    try: t = p.read_text(encoding='utf-8')
    except: continue
    if '{{PROJECT_NAME}}' in t:
        p.write_text(t.replace('{{PROJECT_NAME}}', '${PROJECT_NAME}'), encoding='utf-8')
"
```

### `.gitignore` 누락으로 `target/` 커밋됨

증상: 초기 커밋에 수만 파일.

해결: 템플릿의 `.gitignore` 가 복사되었는지 확인. 없으면 수동 추가 후:
```bash
git rm -rf --cached target/
git add .gitignore
git commit -m "chore: apply gitignore"
```

## 빌드 단계

### Maven `compile` — `package javax.servlet does not exist`

증상: jdk17 환경에서 javax 기반 runner 실행.

원인: 잘못된 runner 선택 (예: jdk17 환경에서 `boot-jdk8-javax`).

해결: 올바른 runner 재스캐폴드 또는 `JAVA_HOME` 을 jdk8 로 설정.

### Maven `test-compile` — `package jakarta.servlet does not exist`

증상: jdk8 환경에서 jakarta 기반 runner 실행.

원인: 반대 케이스. jdk17 설치 필요.

해결: `JAVA_HOME` jdk17 로 설정 또는 `boot-jdk8-javax` 재스캐폴드.

### `mvn spring-boot:run` — port 8080 already in use

증상: `Web server failed to start. Port 8080 was already in use.`

해결 1: 기존 프로세스 종료
```bash
# Windows
netstat -ano | findstr :8080
taskkill /F /PID <pid>
# macOS/Linux
lsof -ti :8080 | xargs kill -9
```

해결 2: 다른 포트 사용 (`application.yml` 의 `server.port` 수정) — 단, nxui `svcurl` 도 맞춰 수정 필요.

## 실행 단계

### nexacro IDE 에서 `packageN.xprj` 열기 실패

증상: "프로젝트 파일이 손상되었습니다".

원인: `{{PROJECT_NAME}}` 토큰 치환 누락.

해결: 타겟 디렉터리에서 `grep -r "{{" nxui/` 로 남은 토큰 확인 후 수동 치환.

### 브라우저 `http://localhost:8080/uiadapter/` 에서 404

증상: nxui 가 로드되지 않음.

원인 1: 서버가 실행 중이 아님. `mvn spring-boot:run` 출력 확인.

원인 2: `contextPath` 불일치. `application.yml` 의 `server.servlet.context-path` 가 `/uiadapter` 인지 확인.

원인 3: nexacro 빌드 산출물이 `static/uiadapter/` 에 배포 안 됨. 별도 플러그인 `nexacro-build` 로 생성 후 복사.

### `login.do` 가 항상 "LOGIN_SUCCESS" 반환

정상 동작입니다. Plan 1 은 Spring Security 미적용, 로그인은 스텁 구현 (§1.3 of design spec). Phase 2 이후 실제 인증 추가 예정.

### WebFlux runner — Mono chain 에서 `Cannot invoke "..." because "..." is null`

증상: 업로드/다운로드 endpoint 에서 NPE.

원인: multipart 부분 읽기가 blocking 코드와 혼재.

참고: `plugins/nexacro-webflux-port/skills/nexacro-webflux-port/references/multipart-import-by-type.md`
```

- [ ] **Step 2: Commit**

Run:
```bash
git add plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/troubleshooting.md
git commit -m "docs(nexacro-fullstack-starter): add troubleshooting.md"
```

---

## Phase 1b — Marketplace / README / CHANGELOG updates

### Task 1.9: Register plugin in `marketplace.json`

**Files:**
- Modify: `D:\AI\workspace\nexacro-claude-skills\.claude-plugin\marketplace.json`

- [ ] **Step 1: Read current marketplace.json**

Run:
```bash
cat .claude-plugin/marketplace.json
```
Note the current structure so you can insert a new `plugins[]` entry matching the existing style.

- [ ] **Step 2: Add new plugin entry**

Add a third object to `plugins[]` array (after the existing `nexacro-claude-skills` and `nexacro-webflux-port` entries). The exact JSON structure follows the existing entries — typically:

```json
{
  "name": "nexacro-fullstack-starter",
  "source": "./plugins/nexacro-fullstack-starter",
  "description": "Scaffolds a full-stack Nexacro N v24 project: packageN nxui + Spring server (Boot/MVC/eGov/WebFlux) picked from a jdk × framework matrix.",
  "keywords": ["nexacro", "nexacroN", "fullstack", "scaffold", "starter"]
}
```

If the existing entries use a different shape (e.g. `path` instead of `source`), match theirs exactly.

- [ ] **Step 3: Validate JSON**

Run:
```bash
python -c "
import json
m = json.load(open('.claude-plugin/marketplace.json', encoding='utf-8'))
names = [p['name'] for p in m['plugins']]
assert 'nexacro-fullstack-starter' in names
assert len(names) == 3
print(f'OK ({len(names)} plugins registered)')
"
```
Expected: `OK (3 plugins registered)`

- [ ] **Step 4: Commit**

Run:
```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(marketplace): register nexacro-fullstack-starter plugin"
```

---

### Task 1.10: Update root `README.md`

**Files:**
- Modify: `D:\AI\workspace\nexacro-claude-skills\README.md`

- [ ] **Step 1: Add plugin to "currently publishes" table**

Edit the existing intro table to list 3 plugins instead of 2. Find:
```markdown
It currently publishes **two plugins**:
```

Replace with:
```markdown
It currently publishes **three plugins**:
```

In the table below that sentence, add a third row:
```markdown
| `nexacro-fullstack-starter` | Scaffolds a full-stack Nexacro N v24 project (packageN nxui + Spring server) from a jdk × framework matrix |
```

- [ ] **Step 2: Add installation command**

Under `### 2. Install the plugin(s) you need`, append a third install command block:
```bash
# Full-stack starter (nxui + server scaffold from a jdk × framework matrix)
/plugin install nexacro-fullstack-starter@nexacro-claude-skills
```

- [ ] **Step 3: Add skill section**

Find the section header `### Plugin ② — \`nexacro-webflux-port\``. After the entire `nexacro-webflux-port` skill section, add a new section:

```markdown
### Plugin ③ — `nexacro-fullstack-starter`

#### nexacro-fullstack-starter
- **Description**: Scaffolds a Nexacro N v24 full-stack project by cloning the `nexacroN-fullstack` monorepo and extracting one of 8 runner combinations (Boot/MVC × jdk8/17, eGov4/5, WebFlux).
- **Triggers**: nexacro fullstack, nexacro 시작, nexacro scaffold, nexacro starter, spring-boot nexacro, webflux nexacro, egov nexacro
- **Features**:
  - 4-input UX (jdk, framework, useEgov, projectName) → 8-runner matrix
  - Auto-derives servletApi / springMajor / bootMajor / egovMajor
  - Rejects impossible combos (eGov MVC + jdk17, WebFlux + jdk8) with alternatives
  - Sparse-clones only the runner + business tree you need (no 8-way bloat)
  - Token substitution (`{{PROJECT_NAME}}`, `{{BACKEND_URL}}`, `{{CONTEXT_PATH}}`)
  - 4 reference docs: compatibility matrix, repo map, runner selection, troubleshooting
```

- [ ] **Step 4: Update "Project Structure" tree**

Find the existing tree listing and add a third plugin under `plugins/`:
```
│   └── nexacro-fullstack-starter/    # plugin ③: fullstack scaffold
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── nexacro-fullstack-starter/
│               ├── SKILL.md
│               ├── assets/matrix.json
│               └── references/       # 4 detailed reference docs
```

- [ ] **Step 5: Commit**

Run:
```bash
git add README.md
git commit -m "docs(readme): add nexacro-fullstack-starter plugin section"
```

---

### Task 1.11: Update root `README-ko.md`

**Files:**
- Modify: `D:\AI\workspace\nexacro-claude-skills\README-ko.md`

- [ ] **Step 1: Update intro**

Find `현재 **2개 플러그인** 을 게시합니다:` and change to `현재 **3개 플러그인** 을 게시합니다:`.

- [ ] **Step 2: Add table row**

Add a third row to the plugin table:
```markdown
| `nexacro-fullstack-starter` | Nexacro N 풀스택 프로젝트 스캐폴드 (packageN nxui + Spring 서버, jdk × 프레임워크 매트릭스) |
```

- [ ] **Step 3: Add install command**

Under `### 2. 필요한 플러그인 설치` block:
```bash
# 풀스택 스캐폴드 (nxui + 서버 매트릭스)
/plugin install nexacro-fullstack-starter@nexacro-claude-skills
```

- [ ] **Step 4: Add skill section**

After the `nexacro-webflux-port` Korean section, append:

```markdown
### 플러그인 ③ — `nexacro-fullstack-starter`

#### nexacro-fullstack-starter
- **설명**: `nexacroN-fullstack` 모노레포를 clone 해서 8가지 runner 조합(Boot/MVC × jdk8/17, eGov4/5, WebFlux) 중 하나를 추출하여 nexacro N v24 풀스택 프로젝트를 스캐폴드
- **트리거**: nexacro 풀스택, nexacro 시작, nexacro 스캐폴드, nexacro starter, spring-boot nexacro, webflux nexacro, egov nexacro
- **기능**:
  - 4개 입력(jdk / framework / useEgov / projectName) → 8-runner 매트릭스
  - servletApi / springMajor / bootMajor / egovMajor 자동 파생
  - 불가능 조합 거부 (eGov MVC + jdk17, WebFlux + jdk8) 및 대안 제시
  - Sparse clone 으로 필요한 runner + business tree 만 받음
  - 토큰 치환 (`{{PROJECT_NAME}}`, `{{BACKEND_URL}}`, `{{CONTEXT_PATH}}`)
  - 4개 레퍼런스 문서: 호환성 매트릭스 / repo 맵 / runner 선택 가이드 / troubleshooting
```

- [ ] **Step 5: Update 프로젝트 구조 tree**

Mirror Task 1.10 Step 4 (add `nexacro-fullstack-starter/` under `plugins/`).

- [ ] **Step 6: Commit**

Run:
```bash
git add README-ko.md
git commit -m "docs(readme-ko): nexacro-fullstack-starter plugin section 추가"
```

---

### Task 1.12: Add v1.8.0 entry to `CHANGELOG.md`

**Files:**
- Modify: `D:\AI\workspace\nexacro-claude-skills\CHANGELOG.md`

- [ ] **Step 1: Insert new entry**

Find `## [Unreleased]` and insert a new section right below it (before `## [1.7.0]`):

```markdown
## [1.8.0] - 2026-04-23

### Added
- **신규 플러그인** `nexacro-fullstack-starter` (v0.1.0)
  - SKILL.md — 6-step 스캐폴드 플로우 (파라미터 수집 → 호환성 체크 → sparse clone → 토큰 치환 → 후처리 → 사용자 안내)
  - `assets/matrix.json` — nexacroN 8-runner 매트릭스 + derivation 규칙 + rejected combinations
  - `references/compatibility-matrix.md` — 전체 매트릭스 + business tree 공유 구조
  - `references/repo-map.md` — `nexacroN-fullstack` 모노레포 트리 + sparse-checkout 가이드
  - `references/runner-selection-guide.md` — 의사결정 트리 + WebFlux 선택 체크리스트
  - `references/troubleshooting.md` — gh 인증 / Windows sed / port 충돌 / multipart NPE 등
- **신규 GitHub repo** `JasonMMo/nexacroN-fullstack`
  - Root README, LICENSE (MIT), .gitignore, 부모 pom.xml
  - `api-contract/openapi.yaml` (15 endpoints 스켈레톤) + `data-formats.md`
  - `core/`, `nxui/`, `samples/{shared-business*, runners, seed-data}/` placeholder
- `.claude-plugin/marketplace.json` — `nexacro-fullstack-starter` 등록 (2 → 3 플러그인)
- README.md / README-ko.md — 플러그인 ③ 섹션 추가

### Changed
- 마켓플레이스 인트로: "two plugins" → "three plugins" / "2개 플러그인" → "3개 플러그인"
- 프로젝트 구조 트리 업데이트 (3개 플러그인 반영)

### Notes
- 현재 Plan 1 스코프: 플러그인 + 모노레포 **skeleton** 까지. 실제 business code (5 shared-business 트리 + 8 runners 본체) 는 Plan 2 에서 구현 예정.
- Spring Security 는 미적용 — `login.do` 는 스텁 구현 (항상 `LOGIN_SUCCESS` 반환).
- `framework=egov-mvc + jdk=17` 과 `framework=webflux + jdk=8` 조합은 명시적으로 거부.
```

- [ ] **Step 2: Commit**

Run:
```bash
git add CHANGELOG.md
git commit -m "docs(changelog): add v1.8.0 entry for nexacro-fullstack-starter"
```

---

### Task 1.13: Bump plugin marketplace aggregate version (if applicable)

**Files:**
- Potentially modify: `D:\AI\workspace\nexacro-claude-skills\plugins\nexacro-claude-skills\.claude-plugin\plugin.json` (only if marketplace uses umbrella version)

- [ ] **Step 1: Check if umbrella version bump is needed**

Run:
```bash
cat plugins/nexacro-claude-skills/.claude-plugin/plugin.json | python -c "import json,sys; print(json.load(sys.stdin)['version'])"
```
Expected: `1.7.0`

Decision: The `nexacro-claude-skills` plugin stays at `1.7.0` (unchanged — it's a sibling plugin). The new plugin has its own version `0.1.0`. The CHANGELOG header `[1.8.0]` refers to the **marketplace-level release**, not any individual plugin version.

→ **No file change required in this task.** Skip to Task 1.14.

---

## Phase 1c — Plugin validation

### Task 1.14: Structural verification via codex

**Files:** none (verification only)

- [ ] **Step 1: Dispatch codex:codex-rescue for independent structural audit**

Dispatch agent with this prompt:

```
Audit the nexacro-fullstack-starter plugin just added at plugins/nexacro-fullstack-starter/.

Check:
1. plugin.json parses as JSON, has name/version/description/keywords
2. SKILL.md has valid YAML frontmatter with name, description, argument-hint
3. matrix.json has exactly 8 runners under nexacroVersions.nexacroN.runners
4. Every runner key in matrix.json matches its runnerPath basename (e.g. "boot-jdk17-jakarta" ↔ "samples/runners/boot-jdk17-jakarta")
5. Every businessTree in matrix.json is one of the 5 valid trees listed in references/compatibility-matrix.md
6. .claude-plugin/marketplace.json lists all 3 plugins
7. README.md, README-ko.md, CHANGELOG.md all mention nexacro-fullstack-starter

Report any drift as BLOCKER / WARNING / NIT. Under 300 words.
```

- [ ] **Step 2: Act on codex findings**

If BLOCKER: fix before proceeding to Task 1.15.
If WARNING/NIT: document in `docs/superpowers/specs/2026-04-23-nexacro-fullstack-starter-design.md` section 10 (Open Questions) for Plan 2 follow-up.

---

### Task 1.15: Local plugin install dry-run

**Files:** none (command-level verification)

- [ ] **Step 1: Verify plugin discoverable from marketplace.json**

Run:
```bash
cd D:\AI\workspace\nexacro-claude-skills
python -c "
import json
mp = json.load(open('.claude-plugin/marketplace.json', encoding='utf-8'))
names = [p['name'] for p in mp['plugins']]
assert 'nexacro-fullstack-starter' in names, f'plugin not found in marketplace.json, only: {names}'
print('OK — plugin listed in marketplace.json')
"
```
Expected: `OK — plugin listed in marketplace.json`

- [ ] **Step 2: Verify SKILL.md passes frontmatter parsing**

Run:
```bash
python -c "
import re
p = 'plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md'
content = open(p, encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
assert m, 'no frontmatter'
fm = m.group(1)
for key in ('name:', 'description:'):
    assert key in fm, f'missing {key}'
print('OK — SKILL.md frontmatter valid')
"
```
Expected: `OK — SKILL.md frontmatter valid`

- [ ] **Step 3: Verify all 4 references exist**

Run:
```bash
ls plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/references/
```
Expected: 4 files — `compatibility-matrix.md`, `repo-map.md`, `runner-selection-guide.md`, `troubleshooting.md`.

---

## Phase 2 — Monorepo skeleton (minimal)

### Task 2.1: Initialize parent POM

**Files:**
- Create: `D:\AI\workspace\nexacroN-fullstack\pom.xml`

- [ ] **Step 1: Write the parent POM**

Content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example.nexacro</groupId>
    <artifactId>nexacroN-fullstack-parent</artifactId>
    <version>0.1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>nexacroN-fullstack parent</name>
    <description>Parent BOM for nexacroN-fullstack monorepo. Manages versions for xapi/xeni/uiadapter, Spring, MyBatis, HSQL, eGovFramework variants.</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <!-- Version defaults (overridable per module) -->
        <spring.jakarta.version>6.1.5</spring.jakarta.version>
        <spring.javax.version>5.3.30</spring.javax.version>
        <boot.jakarta.version>3.2.4</boot.jakarta.version>
        <boot.javax.version>2.7.18</boot.javax.version>
        <mybatis.version>3.5.15</mybatis.version>
        <mybatis.spring.version>2.1.2</mybatis.spring.version>
        <hsqldb.version>2.7.2</hsqldb.version>
        <egov4.version>4.1.0</egov4.version>
        <egov5.version>5.0.0</egov5.version>
    </properties>

    <modules>
        <!-- Plan 2 will enable these one by one. Skeleton leaves the <modules> empty. -->
    </modules>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.hsqldb</groupId>
                <artifactId>hsqldb</artifactId>
                <version>${hsqldb.version}</version>
            </dependency>
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis</artifactId>
                <version>${mybatis.version}</version>
            </dependency>
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis-spring</artifactId>
                <version>${mybatis.spring.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.13.0</version>
                </plugin>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-surefire-plugin</artifactId>
                    <version>3.2.5</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

- [ ] **Step 2: Validate POM is well-formed XML**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
python -c "import xml.etree.ElementTree as ET; ET.parse('pom.xml'); print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

Run:
```bash
git add pom.xml
git commit -m "build: add parent pom.xml with dependency management skeleton"
```

---

### Task 2.2: Scaffold `api-contract/`

**Files:**
- Create: `D:\AI\workspace\nexacroN-fullstack\api-contract\openapi.yaml`
- Create: `D:\AI\workspace\nexacroN-fullstack\api-contract\data-formats.md`
- Create: `D:\AI\workspace\nexacroN-fullstack\api-contract\README.md`

- [ ] **Step 1: Write `api-contract/README.md`**

Content:
```markdown
# API Contract

Source of truth for the 15 endpoints every runner must expose.

## Files

- `openapi.yaml` — OpenAPI 3.1 spec for all endpoints
- `data-formats.md` — Nexacro XML / SSV / JSON envelope reference + `_RowType_` semantics
- `contract-tests/` — RestAssured-based contract tests (Plan 3)

## Endpoints

14 common (all runners) + 1 webflux-only = 15 total.

See `openapi.yaml` for the full spec.
```

- [ ] **Step 2: Write `api-contract/data-formats.md`**

Content:
```markdown
# Nexacro Data Formats

Reference for the JSON envelope Nexacro N v24 uses over the wire.

## Envelope

```json
{
  "version": "1.0",
  "Parameters": [
    { "id": "ErrorCode", "value": 0 },
    { "id": "ErrorMsg", "value": "" }
  ],
  "Datasets": [
    {
      "id": "dsOutput",
      "ColumnInfo": {
        "ConstColumn": [],
        "Column": [
          { "id": "ID", "type": "BIGINT" },
          { "id": "TITLE", "type": "STRING", "size": 200 }
        ]
      },
      "Rows": [
        { "_RowType_": "N", "ID": 1, "TITLE": "sample" }
      ]
    }
  ]
}
```

## `_RowType_` semantics

| Flag | Meaning | Server action |
|---|---|---|
| `N` | Normal (unchanged) | skip |
| `I` | Inserted client-side | INSERT |
| `U` | Updated client-side | UPDATE |
| `D` | Deleted client-side | DELETE |
| `O` | Original snapshot of a modified row | skip (diff reference only) |

## Content-Type

- Default: `application/json`
- File upload: `multipart/form-data`
- Download: `application/octet-stream` or specific MIME

## Cross-reference

See also:
- `.claude/rules/nexacro-data-format.md` (nexacro-webflux project)
- `plugins/nexacro-claude-skills/skills/nexacro-data-format/` (marketplace skill)
```

- [ ] **Step 3: Write `api-contract/openapi.yaml` (stub)**

Content (stub — Plan 3 fleshes out request/response schemas):
```yaml
openapi: 3.1.0
info:
  title: nexacroN-fullstack API contract
  version: 0.1.0
  description: |
    15 endpoints (14 common + 1 webflux-only) that every runner in
    nexacroN-fullstack exposes. Paths are relative to the runner's
    contextPath (default: /uiadapter).
  license:
    name: MIT

servers:
  - url: http://localhost:8080/uiadapter
    description: Local dev server

tags:
  - name: auth
  - name: pattern01
  - name: pattern02-excel
  - name: pattern04-largeData
  - name: sampleDataType
  - name: sampleBulkColumns
  - name: sampleFileUpDownload
  - name: sampleStreaming
  - name: sampleEximExchange
    description: WebFlux-only (other runners provide sync alternative via RestTemplate)

paths:
  /login.do:
    post:
      tags: [auth]
      summary: Stub login (always succeeds — Spring Security not applied in v0.1.0)
      responses:
        "200": { description: OK }

  /select_data_single.do:
    post:
      tags: [pattern01]
      summary: Fetch a single row
      responses: { "200": { description: OK } }

  /select_datalist.do:
    post:
      tags: [pattern01]
      summary: Fetch list (shared by pattern01 and pattern02-excel)
      responses: { "200": { description: OK } }

  /update_datalist_map.do:
    post:
      tags: [pattern01]
      summary: Bulk I/U/D for pattern01
      responses: { "200": { description: OK } }

  /advancedUploadFiles.do:
    post:
      tags: [sampleFileUpDownload]
      summary: Multipart upload
      parameters:
        - in: query
          name: subFolder
          schema: { type: string }
      responses: { "200": { description: OK } }

  /advancedDownloadFile.do:
    get:
      tags: [sampleFileUpDownload]
      summary: Single file download
      parameters:
        - in: query
          name: subFolder
          schema: { type: string }
      responses: { "200": { description: OK } }

  /multiDownloadFiles.do:
    get:
      tags: [sampleFileUpDownload]
      summary: Multi-file download (zip stream)
      parameters:
        - in: query
          name: subFolder
          schema: { type: string }
      responses: { "200": { description: OK } }

  /advancedDownloadList.do:
    post:
      tags: [sampleFileUpDownload]
      summary: List downloadable files
      responses: { "200": { description: OK } }

  /streamingVideo.do:
    get:
      tags: [sampleStreaming]
      summary: Video streaming (NIO)
      parameters:
        - in: query
          name: fileName
          schema: { type: string }
          required: true
        - in: query
          name: streamType
          schema: { type: string, enum: [nio] }
      responses: { "200": { description: OK, content: { "video/*": {} } } }

  /select_testDataTypeList.do:
    post:
      tags: [sampleDataType]
      responses: { "200": { description: OK } }

  /check_testDataTypeList.do:
    post:
      tags: [sampleDataType]
      responses: { "200": { description: OK } }

  /update_deptlist_map.do:
    post:
      tags: [sampleDataType]
      summary: Bulk I/U/D for dept list
      responses: { "200": { description: OK } }

  /sampleLargeData.do:
    post:
      tags: [pattern04-largeData]
      responses: { "200": { description: OK } }

  /search_manyColumn_data.do:
    post:
      tags: [sampleBulkColumns]
      responses: { "200": { description: OK } }

  /relay/exim_exchange.do:
    post:
      tags: [sampleEximExchange]
      summary: |
        WebFlux-native reactive relay. Other runners provide a synchronous
        RestTemplate-based implementation with the same contract.
      responses: { "200": { description: OK } }
```

- [ ] **Step 4: Validate YAML parses**

Run:
```bash
python -c "
import yaml
spec = yaml.safe_load(open('api-contract/openapi.yaml', encoding='utf-8'))
paths = spec['paths']
assert len(paths) == 15, f'expected 15 paths, got {len(paths)}'
print(f'OK ({len(paths)} endpoints)')
"
```
Expected: `OK (15 endpoints)`

> If `yaml` module unavailable, install with `pip install pyyaml`.

- [ ] **Step 5: Commit**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
git add api-contract/README.md
git commit -m "docs(api-contract): add README"
git add api-contract/data-formats.md
git commit -m "docs(api-contract): add data-formats.md with _RowType_ reference"
git add api-contract/openapi.yaml
git commit -m "feat(api-contract): add openapi.yaml stub with 15 endpoints"
```

---

### Task 2.3: Placeholder directories + READMEs

**Files:**
- Create: `core/README.md`, `nxui/README.md`, `samples/README.md`
- Create: `samples/shared-business/README.md`, `samples/shared-business-egov4/README.md`, `samples/shared-business-egov5/README.md`, `samples/shared-business-reactive/README.md`
- Create: `samples/runners/README.md`

- [ ] **Step 1: Create directory structure**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
mkdir -p core nxui samples/shared-business samples/shared-business-egov4 samples/shared-business-egov5 samples/shared-business-reactive samples/runners samples/seed-data
```

- [ ] **Step 2: Write `core/README.md`**

```markdown
# core/

Nexacro backend support modules. Each module has `javax` and `jakarta` variants — choose based on runner's servletApi.

Content to be migrated from the existing `nexacro-webflux` project in **Plan 2**:

- `xapi-javax/`, `xapi-jakarta/` — nexacro HTTP API (request/response marshaling)
- `xeni-javax/`, `xeni-jakarta/` — Excel import/export
- `uiadapter-javax/`, `uiadapter-jakarta/` — Spring integration layer

**Status:** Placeholder — modules to land in Plan 2.
```

- [ ] **Step 3: Write `nxui/README.md`**

```markdown
# nxui/

Nexacro N v24 front-end project (`packageN`).

**Status:** Placeholder — full xprj/xadl/xfdl migration lands in Plan 3.

Source reference: `D:\AI\reference\Nexacro24\Sample\packageN`

When migrated:
- `packageN.xprj`, `packageN.xadl` (MDI FrameSet layout)
- `typedefinition.xml` with `svcurl=http://localhost:8080/uiadapter/`
- `frame/`, `Base/`, `pattern/`, `sample/` form folders
```

- [ ] **Step 4: Write `samples/README.md`**

```markdown
# samples/

5 business-code trees + 8 thin runners + shared seed-data.

```
samples/
├── seed-data/                          (HSQL schema + seed — all runners share)
├── shared-business/jdk{8-javax,17-jakarta}/  (plain Spring)
├── shared-business-egov4/jdk8-javax/   (eGov 4.x)
├── shared-business-egov5/jdk17-jakarta/ (eGov 5.x)
├── shared-business-reactive/jdk17-mybatis/ (WebFlux controllers only)
└── runners/                            (8 entry-point modules)
```

**Status:** Skeleton only (Plan 1). Real business code + runners land in Plan 2.
```

- [ ] **Step 5: Write placeholder READMEs in each `shared-business*` and `runners/`**

For each of these 5 files, content follows the same pattern:

`samples/shared-business/README.md`:
```markdown
# shared-business/

Plain Spring business code (no eGov).

- `jdk8-javax/` — Spring 5 / javax / MyBatis 3. Consumed by `boot-jdk8-javax`, `mvc-jdk8-javax`.
- `jdk17-jakarta/` — Spring 6 / jakarta / MyBatis 3. Consumed by `boot-jdk17-jakarta`, `mvc-jdk17-jakarta`, and (via import) `shared-business-reactive/jdk17-mybatis`.

**Status:** Placeholder — Plan 2.
```

`samples/shared-business-egov4/README.md`:
```markdown
# shared-business-egov4/

eGovFramework 4.x business code.

- `jdk8-javax/` — eGov 4.x / Spring 5 / javax. Consumed by `egov4-boot-jdk8-javax`, `egov4-mvc-jdk8-javax`.

**Status:** Placeholder — Plan 2.

Note: eGov4 MVC uses Boot-based source as the authoritative version (per design spec §2.1 resolution).
```

`samples/shared-business-egov5/README.md`:
```markdown
# shared-business-egov5/

eGovFramework 5.x business code.

- `jdk17-jakarta/` — eGov 5.x / Spring 6 / jakarta. Consumed by `egov5-boot-jdk17-jakarta`.

**Status:** Placeholder — Plan 2.
```

`samples/shared-business-reactive/README.md`:
```markdown
# shared-business-reactive/

WebFlux controllers only. Service/mapper layer reuses `samples/shared-business/jdk17-jakarta/` (option A from design spec §2.3).

- `jdk17-mybatis/` — MyBatis synchronous wrapping (`Mono.fromCallable(...).subscribeOn(boundedElastic())`).

**Status:** Placeholder — Plan 2.

Future: `jdk17-r2dbc/` for fully reactive persistence.
```

`samples/runners/README.md`:
```markdown
# runners/

8 thin entry-point modules. Each contains only:

- `pom.xml` (declares business-tree dependency + framework starter)
- `Application.java` (Spring Boot) OR `web.xml` + dispatcher xml (Spring MVC)
- `application.yml` or equivalent config

Heavy lifting (controllers/services/mappers) lives in the consumed `shared-business*` module.

**Status:** Placeholder — Plan 2.
```

- [ ] **Step 6: Commit each README individually**

Run:
```bash
git add core/README.md
git commit -m "docs(core): add placeholder README"
git add nxui/README.md
git commit -m "docs(nxui): add placeholder README"
git add samples/README.md
git commit -m "docs(samples): add overview README"
git add samples/shared-business/README.md
git commit -m "docs(shared-business): add placeholder README"
git add samples/shared-business-egov4/README.md
git commit -m "docs(shared-business-egov4): add placeholder README"
git add samples/shared-business-egov5/README.md
git commit -m "docs(shared-business-egov5): add placeholder README"
git add samples/shared-business-reactive/README.md
git commit -m "docs(shared-business-reactive): add placeholder README"
git add samples/runners/README.md
git commit -m "docs(runners): add placeholder README"
```

---

### Task 2.4: Seed-data schema skeleton

**Files:**
- Create: `samples/seed-data/schema.sql`
- Create: `samples/seed-data/data.sql`
- Create: `samples/seed-data/README.md`

- [ ] **Step 1: Write `samples/seed-data/README.md`**

```markdown
# seed-data/

HSQL schema + seed data shared by all 8 runners.

## Files

- `schema.sql` — DDL for test tables
- `data.sql` — INSERT statements for initial test rows

## Load strategy

Runners load these at startup via:
- Spring Boot: `spring.sql.init.schema-locations` + `data-locations` pointing to classpath:seed-data/*.sql
- MVC war: `@PostConstruct` hook on a `@Component` reading the same files

## Schema evolution

Keep schema.sql idempotent where possible (`CREATE TABLE IF NOT EXISTS`, though HSQL support is limited — use `DROP TABLE IF EXISTS ...; CREATE TABLE ...;` pattern).

## Plan 2 merges

When Plan 2 migrates real schemas from the 8 GitLab repos, use the **richest schema** as the base (design spec §2 — "sql내용이 많을 경우, 많은 sql 파일을 기준으로 한다").
```

- [ ] **Step 2: Write `samples/seed-data/schema.sql`**

```sql
-- nexacroN-fullstack seed schema (HSQL)
-- Covers: login, pattern01 board, pattern04 large-data, sampleDataType dept,
--         sampleBulkColumns wide, sampleFileUpDownload file metadata.

DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS (
    USER_ID        VARCHAR(32)  PRIMARY KEY,
    USER_NAME      VARCHAR(64)  NOT NULL,
    USER_PASSWORD  VARCHAR(64)  NOT NULL
);

DROP TABLE IF EXISTS SAMPLE_BOARD;
CREATE TABLE SAMPLE_BOARD (
    ID         BIGINT IDENTITY PRIMARY KEY,
    TITLE      VARCHAR(200) NOT NULL,
    CONTENT    LONGVARCHAR,
    WRITER     VARCHAR(32),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS DEPT;
CREATE TABLE DEPT (
    DEPT_NO    INT          PRIMARY KEY,
    DEPT_NAME  VARCHAR(64)  NOT NULL,
    LOC        VARCHAR(64)
);

DROP TABLE IF EXISTS LARGE_DATA;
CREATE TABLE LARGE_DATA (
    ID          BIGINT IDENTITY PRIMARY KEY,
    PAYLOAD     VARCHAR(200),
    CREATED_AT  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS WIDE_COLUMNS;
CREATE TABLE WIDE_COLUMNS (
    ID        BIGINT IDENTITY PRIMARY KEY,
    COL_01    VARCHAR(32), COL_02    VARCHAR(32), COL_03    VARCHAR(32),
    COL_04    VARCHAR(32), COL_05    VARCHAR(32), COL_06    VARCHAR(32),
    COL_07    VARCHAR(32), COL_08    VARCHAR(32), COL_09    VARCHAR(32),
    COL_10    VARCHAR(32), COL_11    VARCHAR(32), COL_12    VARCHAR(32),
    COL_13    VARCHAR(32), COL_14    VARCHAR(32), COL_15    VARCHAR(32),
    COL_16    VARCHAR(32), COL_17    VARCHAR(32), COL_18    VARCHAR(32),
    COL_19    VARCHAR(32), COL_20    VARCHAR(32)
);

DROP TABLE IF EXISTS FILE_META;
CREATE TABLE FILE_META (
    FILE_ID    VARCHAR(64) PRIMARY KEY,
    SUB_FOLDER VARCHAR(128),
    FILE_NAME  VARCHAR(256) NOT NULL,
    SIZE_BYTES BIGINT,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- [ ] **Step 3: Write `samples/seed-data/data.sql`**

```sql
-- Seed data (minimal — Plan 2 will merge from 8 GitLab repos).

INSERT INTO USERS (USER_ID, USER_NAME, USER_PASSWORD) VALUES
    ('test1', '테스트유저', 'test1');

INSERT INTO SAMPLE_BOARD (TITLE, CONTENT, WRITER) VALUES
    ('첫 번째 게시글', '샘플 컨텐트 A', 'test1'),
    ('두 번째 게시글', '샘플 컨텐트 B', 'test1'),
    ('세 번째 게시글', '샘플 컨텐트 C', 'test1');

INSERT INTO DEPT (DEPT_NO, DEPT_NAME, LOC) VALUES
    (10, 'ACCOUNTING', 'NEW YORK'),
    (20, 'RESEARCH',   'DALLAS'),
    (30, 'SALES',      'CHICAGO'),
    (40, 'OPERATIONS', 'BOSTON');
```

- [ ] **Step 4: Validate SQL (syntactic check via HSQL driver if available, else basic)**

Run:
```bash
python -c "
sql = open('samples/seed-data/schema.sql', encoding='utf-8').read()
assert 'CREATE TABLE USERS' in sql
assert 'CREATE TABLE SAMPLE_BOARD' in sql
assert 'CREATE TABLE DEPT' in sql
assert 'CREATE TABLE LARGE_DATA' in sql
assert 'CREATE TABLE WIDE_COLUMNS' in sql
assert 'CREATE TABLE FILE_META' in sql
print('OK — 6 tables defined')
"
```
Expected: `OK — 6 tables defined`

- [ ] **Step 5: Commit**

Run:
```bash
git add samples/seed-data/README.md
git commit -m "docs(seed-data): add README"
git add samples/seed-data/schema.sql
git commit -m "feat(seed-data): add HSQL schema with 6 tables"
git add samples/seed-data/data.sql
git commit -m "feat(seed-data): add initial seed rows"
```

---

### Task 2.5: Push monorepo skeleton to GitHub

**Files:** none (remote sync)

- [ ] **Step 1: Review pending commits**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
git log --oneline origin/main..HEAD
```
Expected: ~15 commits (parent pom, api-contract × 3, 8 READMEs, seed-data × 3).

- [ ] **Step 2: Push**

Run:
```bash
git push origin main
```
Expected: `Writing objects: 100% ... Total XX ... To https://github.com/JasonMMo/nexacroN-fullstack.git`

- [ ] **Step 3: Verify remote state**

Run:
```bash
gh repo view JasonMMo/nexacroN-fullstack --json defaultBranch,url,pushedAt
```
Expected: JSON output with `"defaultBranch": "main"` and recent `pushedAt`.

---

## Phase 3 — End-to-end validation

### Task 3.1: Simulate full skill invocation (dry run)

**Files:** none (integration verification)

- [ ] **Step 1: Dispatch Sonnet subagent to simulate the skill**

Dispatch agent with this prompt:

```
You are simulating an execution of the nexacro-fullstack-starter skill to verify Plan 1 is wired correctly. Don't write files — report what would happen.

Load D:\AI\workspace\nexacro-claude-skills\plugins\nexacro-fullstack-starter\skills\nexacro-fullstack-starter\SKILL.md and matrix.json.

Simulate user input:
  nexacroVersion = nexacroN
  jdk = 17
  framework = spring-boot
  projectName = my-app
  targetDir = ./my-app

Walk through Steps 1-6 of SKILL.md. For each step report:
  - What the skill computes
  - What command/operation it would run
  - What output it would produce

Specifically confirm:
  1. Derived values: servletApi=jakarta, springMajor=6, bootMajor=3, egovMajor=null
  2. Runner key resolves to: boot-jdk17-jakarta
  3. Sparse checkout paths: api-contract, core, nxui, pom.xml, README.md, LICENSE, .gitignore, samples/seed-data, samples/shared-business/jdk17-jakarta, samples/runners/boot-jdk17-jakarta
  4. No rejected-combinations match
  5. Final user guidance shows "mvn spring-boot:run" as the run command

Under 400 words.
```

- [ ] **Step 2: Also simulate a rejected combination**

Dispatch another Sonnet subagent:

```
Same context as previous simulation, but input: framework=egov-mvc, jdk=17.

Confirm Step 2 of SKILL.md:
  1. matches the rejectedCombinations entry { framework: egov-mvc, jdk: 17 }
  2. outputs the reason ("eGov4 MVC on jdk17/jakarta is not supported...")
  3. suggests the alternative: egov5-boot-jdk17-jakarta
  4. halts without cloning

Under 200 words.
```

- [ ] **Step 3: Act on results**

If either simulation reports ambiguity or bug, create a follow-up task and fix in the relevant file. Re-run simulation until clean.

---

### Task 3.2: Final codex verification

**Files:** none

- [ ] **Step 1: Dispatch codex:codex-rescue for Plan 1 acceptance check**

Dispatch with:

```
Verify Plan 1 acceptance criteria for nexacro-fullstack-starter v0.1.0:

Repo 1 checks (D:\AI\workspace\nexacro-claude-skills):
  [ ] plugins/nexacro-fullstack-starter/ has plugin.json + SKILL.md + matrix.json + 4 references
  [ ] .claude-plugin/marketplace.json lists 3 plugins
  [ ] README.md, README-ko.md mention the new plugin in both intro table and dedicated section
  [ ] CHANGELOG.md has [1.8.0] entry describing all additions

Repo 2 checks (D:\AI\workspace\nexacroN-fullstack, also verify github.com/JasonMMo/nexacroN-fullstack):
  [ ] Root README.md, LICENSE, .gitignore present
  [ ] pom.xml parses as XML, is packaging=pom
  [ ] api-contract/openapi.yaml has exactly 15 paths
  [ ] api-contract/data-formats.md, api-contract/README.md present
  [ ] core/, nxui/, samples/{shared-business*, runners, seed-data}/ all have README.md
  [ ] samples/seed-data/schema.sql defines 6 tables
  [ ] samples/seed-data/data.sql inserts rows in USERS, SAMPLE_BOARD, DEPT

Cross-checks:
  [ ] matrix.json's repo URL matches the created GitHub repo
  [ ] Every businessTree in matrix.json maps to an existing (even if placeholder) path in Repo 2
  [ ] Every runnerPath in matrix.json maps to a path that will be populated by Plan 2 (placeholder OK now)

Report PASS/FAIL per item + overall verdict. Under 400 words.
```

- [ ] **Step 2: If any FAIL, fix in the relevant task before declaring Plan 1 complete**

No checkpoint commits — fixes go in ad-hoc commits referencing the original task.

---

### Task 3.3: Plan 1 completion commit tag

**Files:** none

- [ ] **Step 1: Tag the plugin repo**

Run:
```bash
cd D:\AI\workspace\nexacro-claude-skills
git tag -a v1.8.0-plan1 -m "Plan 1 complete: nexacro-fullstack-starter scaffolded, nexacroN-fullstack skeleton on GitHub"
git push origin v1.8.0-plan1
```
Expected: tag visible on GitHub.

- [ ] **Step 2: Tag the monorepo**

Run:
```bash
cd D:\AI\workspace\nexacroN-fullstack
git tag -a v0.1.0-skeleton -m "Plan 1 skeleton complete — ready for Plan 2 body fill"
git push origin v0.1.0-skeleton
```

- [ ] **Step 3: Announce Plan 1 complete**

In the chat with the user, report:

```
✅ Plan 1 complete.

Repo 1 (nexacro-claude-skills): v1.8.0-plan1 tagged, plugin installable.
Repo 2 (nexacroN-fullstack):    v0.1.0-skeleton tagged, skeleton in place.

Next: Plan 2 — fill in 5 shared-business trees + 8 runners + contract tests.
```

---

## Self-Review

### 1. Spec coverage

Walking through `2026-04-23-nexacro-fullstack-starter-design.md` sections:

- §1 Overview & Goals → Plan 1 addresses consumer UX (plugin call); provider UX partially (structure in place, body in Plan 2) ✓
- §2 Design Decisions (C'''''' architecture, matrix, derivation) → Task 1.3 matrix.json + Task 1.5 compatibility-matrix.md ✓
- §3 Plugin Structure → Tasks 1.1–1.8 ✓
- §4 Monorepo Structure → Tasks 2.1–2.5 (skeleton only — bodies deferred to Plan 2) ✓ for skeleton scope
- §5 API Contract → Task 2.2 openapi.yaml stub (schemas deferred to Plan 3) ✓ for stub scope
- §6 Skill Invocation Flow → Task 1.4 SKILL.md (7 steps → Plan 1 has 6 steps; consolidated Step 4+5 of design as single Token step) — **document this as intentional compression**
- §7 Orchestration Plan → referenced in plan header + selectively in tasks (1.4 dispatches Sonnet, 1.14 and 3.2 dispatch codex) ✓
- §8 Phased Rollout → Plan 1 covers Phase 0 + Phase 1 + Phase 2 skeleton; Phase 3 archival + Phase 4 release are explicitly Plan 3 ✓
- §9 Risks → addressed inline (eGov MVC jdk17 rejected in matrix, reactive import strategy documented)
- §10 Open Questions → carried forward; no new ones introduced
- §11 Acceptance Criteria → Task 3.2 codex verification explicitly maps to spec acceptance items 1 (install) and implicitly to 4 (monorepo update propagation)

### 2. Placeholder scan

Searched plan for banned patterns (TBD, TODO in task steps, "Add X", "Similar to Task N", undefined types). None found. The `[Plan 2]` and `[Plan 3]` markers in placeholder READMEs are **intentional handoff markers**, not task-internal placeholders.

### 3. Type consistency

- `runner key` naming: always uses full form (e.g. `egov5-boot-jdk17-jakarta`), never shortened — consistent between matrix.json, SKILL.md, compatibility-matrix.md, repo-map.md, runner-selection-guide.md, openapi.yaml tags, runner directory names.
- `businessTree` paths: always `samples/shared-business*/jdk{8-javax,17-jakarta,17-mybatis}` — consistent.
- `tokens`: same set across matrix.json, SKILL.md Step 4, README template — consistent.
- File naming: all reference docs use kebab-case `*.md` — consistent.
- CHANGELOG refers to plugin version `0.1.0` and marketplace release `1.8.0` — distinction preserved across README/plugin.json/CHANGELOG.

### 4. Scope decomposition check

Plan 1 = Phase 0 repo + Phase 1 plugin + Phase 2 skeleton. Independently deliverable: after Plan 1, user can `/plugin install` + `/nexacro-fullstack-starter`, and the clone succeeds (produces an empty but structurally valid project). Plan 2 (business code) and Plan 3 (nxui migration + tests + release) have their own testable deliverables.

---

## Execution Handoff

**Plan complete and saved to `D:\AI\workspace\nexacro-claude-skills\docs\superpowers\plans\2026-04-23-nexacro-fullstack-starter-plan1.md`.** Two execution options:

**1. Subagent-Driven (recommended)** — Opus dispatches a fresh subagent per task, review between tasks, fast iteration. Fits the agreed orchestration model (Opus coordinates, Sonnet/Haiku execute, codex verifies).

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints for review.

**Which approach?**
