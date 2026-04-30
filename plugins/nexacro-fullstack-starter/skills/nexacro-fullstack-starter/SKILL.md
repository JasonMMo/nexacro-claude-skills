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
- **매트릭스**: `assets/matrix.json` (현재 2개 runner 구현 완료 + 6개 placeholder)
- **출력 구조**: `<TARGET_DIR>/{nxui/, src/, pom.xml, README.md}` — runner 디렉터리 평탄화 (project root 에서 바로 `mvn` 실행 가능)

## Step 1 — 파라미터 수집 / Collect parameters

### 1-1. 파라미터 수집

CLI 아규먼트(`--jdk`, `--framework` 등)로 전달된 값은 이미 받은 것으로 간주하고 건너뜁니다.

**자동 확정 항목 (질문 없이 즉시 설정):**
- nexacro 버전: `nexacroN` 고정 (현재 유일 지원 버전)
- 타겟 디렉터리: `./<PROJECT_NAME>` 으로 자동 확정 (프로젝트명 입력 후 계산)

**사용자 입력 필요 항목 (3개만 질문):**

```
[1/3] JDK 버전 / JDK version
      선택지: 8 | 17
      - 8  → Spring 5 / javax / Boot 2 / eGov4
      - 17 → Spring 6 / jakarta / Boot 3 / eGov5

[2/3] 프레임워크 / Framework
      선택지:
      - spring-boot  (Spring Boot - embedded Tomcat) ✅ 구현 완료
      - spring-mvc   (전통 MVC - war 배포) ⏳ 업스트림 Plan 2 대기
      - egov-boot    (표준프레임워크 Boot)         ⏳ 업스트림 Plan 2 대기
      - egov-mvc     (표준프레임워크 MVC - jdk8만)  ⏳ 업스트림 Plan 2 대기
      - webflux      (Spring WebFlux - jdk17만)    ⏳ 업스트림 Plan 2 대기

      현재 사용 가능: spring-boot 만. 나머지는 upstream nexacroN-fullstack
      에 placeholder README 만 있으므로 scaffold 시 거부됩니다.

[3/3] 프로젝트 이름 / Project name
      예: my-nexacro-app
      제약: 영숫자 + 하이픈만, 공백 불가
```

3개 질문이 끝나면 자동으로 아래를 확정한다 (추가 질문 없음):
- `NEXACRO_VERSION = nexacroN`
- `TARGET_DIR = ./<PROJECT_NAME>`
- `경고`: TARGET_DIR 이 이미 존재하면 중단 (덮어쓰기 안 함)

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
1. `framework=egov-mvc + jdk=17` — eGov4 MVC jdk17 미지원 → `egov5-boot-jdk17-jakarta` 권장 (단, 아래 3번도 적용)
2. `framework=webflux + jdk=8` — WebFlux는 jdk17+ 전용 → `boot-jdk8-javax` 권장
3. `framework ∈ {spring-mvc, egov-boot, egov-mvc, webflux}` — 업스트림 nexacroN-fullstack 에 placeholder 만 존재 (Plan 2 미구현). 현재는 `spring-boot` 만 scaffold 가능. 사용자에게 alternative 로 `(spring-boot, jdk=8|17)` 권장.

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

## Step 3 — Sparse clone & flatten

> 업스트림 [`JasonMMo/nexacroN-fullstack`](https://github.com/JasonMMo/nexacroN-fullstack) 의 implemented runner (`samples/runners/boot-jdk17-jakarta`, `samples/runners/boot-jdk8-javax`) 는 self-contained 입니다 (parent BOM / shared-business 의존성 없음). 따라서 sparse-checkout 으로 `nxui` + 해당 runner 만 받은 뒤, runner 디렉터리 내용을 project root 로 평탄화하면 바로 빌드 가능합니다.

### 3-0. 실행 환경 가드 (필수)

본 Step 의 모든 셸 명령은 **단일 native shell 세션** 에서 실행해야 합니다. `$TMP_DIR` 변수가 호출 간에 공유되어야 하기 때문입니다.

- ✅ Bash 도구로 `&&` chained command 한 번에 실행
- ✅ 또는 각 단계 직전에 `export TMP_DIR=...` 재선언
- ❌ `ctx_batch_execute` 처럼 호출별 컨테이너 격리가 일어나는 도구 사용 금지 (각 호출마다 새 `/tmp` 가 생성되어 이전 단계 산출물을 못 찾음)

### 3-1. 임시 디렉터리로 sparse clone (--no-cone 모드)

```bash
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"
git clone --filter=blob:none --no-checkout https://github.com/JasonMMo/nexacroN-fullstack.git
cd nexacroN-fullstack
git sparse-checkout init --no-cone
git sparse-checkout set \
  nxui \
  samples/runners/${RUNNER_KEY}
git checkout
```

> `--no-cone` 모드 이유: cone 모드는 디렉터리 단위만 허용하고 파일 단위 패턴을 거부합니다. 일관되게 `--no-cone` 사용. top-level `api-contract`, `core`, root `pom.xml`, root `README.md`, root `LICENSE`, `.gitignore`, `samples/seed-data`, `samples/shared-business*` 는 모두 **체크아웃 대상에서 제외** — runner 가 self-contained 이므로 불필요합니다.

### 3-2. 타겟 디렉터리로 평탄화 복사

`nxui/` 는 그대로 복사하고, runner 디렉터리의 **내용물** (src/, pom.xml, README.md) 을 project root 로 평탄화합니다.

```bash
mkdir -p "${TARGET_DIR}"
cp -r "$TMP_DIR/nexacroN-fullstack/nxui" "${TARGET_DIR}/"
cp -r "$TMP_DIR/nexacroN-fullstack/samples/runners/${RUNNER_KEY}/." "${TARGET_DIR}/"
rm -rf "$TMP_DIR"
cd "${TARGET_DIR}"
```

### 3-3. 산출 트리 검증 (필수)

평탄화가 정확히 적용됐는지 검증:

```bash
# 있어서는 안 되는 디렉터리/파일
for forbidden in api-contract core samples; do
  [ -e "$forbidden" ] && { echo "ERROR: '$forbidden' should not exist after flatten" >&2; exit 1; }
done
# 반드시 있어야 하는 항목
for required in nxui src pom.xml; do
  [ ! -e "$required" ] && { echo "ERROR: required '$required' missing" >&2; exit 1; }
done
echo "✅ flatten verified: nxui/  src/  pom.xml"
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

1. 서버 실행 (project root 에서 바로): `{{RUN_CMD}}`
2. nexacro IDE 에서 `nxui/packageN.xprj` 열기
3. 브라우저: http://localhost:8080/uiadapter/

## Build prerequisite

- JDK 17+ (jdk8 lane 도 빌드 시점은 JDK 17 권장 — HSQLDB 2.7.x 가 Java 11+ 필요)
- Maven 3.6+
- 인터넷 (tobesoft Nexus 에서 nexacro 1st-party JAR 다운로드, 익명 접근)
```

### 5-2. 초기 커밋 (옵션)

```bash
git init
git add .
git commit -m "chore: scaffolded from nexacro-fullstack-starter"
```

사용자에게 물어보고 진행 (기본값: yes).

## Step 6 — nexacro 빌드 / Nexacro build (xfdl → xjs)

scaffold 가 끝난 직후 `nxui/packageN` 의 xfdl 소스를 **xjs 로 1회 빌드**해야 Spring 정적 경로에서 로드할 수 있습니다. 이 단계는 `nexacrodeploy.exe` (Nexacro Studio 설치 시 동봉) 가 필요하므로 Claude 가 자동 실행하기보다는 사용자의 로컬 `/nexacro-build` skill 로 **핸드오프** 합니다.

### 6-1. 빌드 경로 결정 (runner 별)

| Runner family | Build output path |
|---|---|
| `boot-*`, `webflux-*` | `./src/main/resources/static/packageN/` |
| `mvc-*`, `egov*-mvc-*` | `./src/main/webapp/packageN/` |

runner key 의 prefix 로 자동 매핑:

```
case "${RUNNER_KEY}" in
  boot-*|webflux-*)    BUILD_OUT="./src/main/resources/static/packageN/" ;;
  mvc-*|egov*-mvc-*)   BUILD_OUT="./src/main/webapp/packageN/" ;;
esac
```

### 6-2. `/nexacro-build` skill 안내 메시지

사용자에게 아래 문구를 그대로 출력 (자동 실행하지 않음):

```
📦 nexacro xfdl → xjs 1회 빌드가 필요합니다.
   로컬에 Nexacro Studio 가 설치되어 있으면 user skill `/nexacro-build` 로 실행하세요.

   권장 파라미터:
     project_xprj     = ./nxui/packageN/packageN.xprj
     output_path      = {{BUILD_OUT}}
     baselib_path     = ./nxui/packageN/nexacrolib
     generaterule_path= <SDK>/generate

   또는 CLI 로 직접:
     nexacrodeploy.exe \
       -P ./nxui/packageN/packageN.xprj \
       -O {{BUILD_OUT}} \
       -B ./nxui/packageN/nexacrolib \
       -GENERATERULE <SDK>/generate
```

### 6-3. `/nexacro-build` 가 설치되어 있는 경우 자동 연계

Claude 환경에서 `/nexacro-build` skill 이 사용 가능하면 Skill 도구로 직접 호출:

```
Skill(skill: "nexacro-build", args: "project=./nxui/packageN/packageN.xprj output={{BUILD_OUT}}")
```

skill 이 없으면 6-2 의 안내 문구만 출력하고 다음 Step 으로 넘어갑니다 (실패 아님).

> ⚠️ nexacro Studio / `nexacrodeploy.exe` 는 Windows 전용입니다. macOS / Linux 사용자는 Windows 워크스테이션에서 빌드 후 산출물만 커밋하는 워크플로우를 사용하세요 (references/troubleshooting.md 참고).

## Step 7 — 사용자 안내 / Final guidance

실행 요약 출력:

```
✅ 프로젝트 생성 완료 / Scaffold complete
─────────────────────────────────────
경로:     ./{{PROJECT_NAME}}
runner:   {{RUNNER_KEY}}
빌드 경로: {{BUILD_OUT}}
─────────────────────────────────────

다음 단계 / Next steps:
  1. xfdl 빌드:   Step 6 참고 (`/nexacro-build` 또는 nexacrodeploy.exe)
  2. DB 초기화:   (seed-data 는 서버 첫 실행 시 자동 로드)
  3. 서버 실행:   {{RUN_CMD}}   ← project root 에서 바로 실행
  4. nexacro IDE: nxui/packageN.xprj 열기
  5. 브라우저:    http://localhost:8080/uiadapter/

문제 발생 시 references/troubleshooting.md 참고.
```

## 참고 / References

- `references/compatibility-matrix.md` — 매트릭스 전체 + 파생 규칙 상세
- `references/repo-map.md` — `nexacroN-fullstack` 모노레포 트리 설명
- `references/runner-selection-guide.md` — 어떤 runner 를 골라야 하는지 가이드
- `references/troubleshooting.md` — 자주 발생하는 이슈 (port 충돌, JDK mismatch, war 배포)
