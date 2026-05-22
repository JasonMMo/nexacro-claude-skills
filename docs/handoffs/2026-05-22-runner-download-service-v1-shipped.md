# Handoff — 2026-05-22

웹 셀렉터 → fullstack-starter JAR/WAR 다운로드 서비스 **v1 완료, 운영 모드 진입**.

> **이 문서의 위치**: [2026-05-19 핸드오프](./2026-05-19-runner-build-service.md)(설계 착수) → [설계 spec](../superpowers/specs/2026-05-19-runner-download-service-design.md)(D1–D5 결정) → **본 문서**(M0–M6 통과 후 v1 종결 + 운영 SOP + v1.1 항목 인계).
>
> 단일 라우터: `RESUME.md` "트랙 B" 행. 본 문서는 그 행이 가리키는 상세 인계서.

---

## TL;DR

- v1 아키텍처(GitHub Pages 정적 셀렉터 + GitHub Releases CDN, 백엔드 0) **그대로 가동 중**. 셀렉터는 https://jasonmmo.github.io/nexacroN-fullstack/ 에서 `stable`을 default로 렌더.
- `nightly` 채널: 매일 03:00 KST cron 자동 빌드·게시. 4개 활성 + 3개 stale snapshot = 자산 7개 항상 존재.
- `stable` 채널: **수동 promote**. M6 첫 promote 는 직접 `gh release upload` 로 수행. 이후부터는 v1.1 task #1 ([PR #46](https://github.com/JasonMMo/nexacroN-fullstack/pull/46))으로 워크플로화 — 머지 후 Actions 1-click.
- 셀렉터·문서 일관성: 7-key 모두 살아있어야 함 (셀렉터는 자산 존재를 가정함). subset promote 금지.
- 미해결 v1.1 작업 3건: (1) promote-stable 머지/검증, (2) webflux 활성화, (3) matrix.json sync 자동화.

---

## 무엇이 어디에 살고 있나 (운영 토폴로지)

```
[사용자 브라우저]
      │
      ▼  GET https://jasonmmo.github.io/nexacroN-fullstack/
[GitHub Pages — orphan branch `gh-pages`]
   ├─ index.html        ← 셀렉터 UI, default channel = "stable"
   ├─ selection.js      ← derivationRules + rejectedCombinations + buildUrl()
   ├─ matrix.json       ← 8 runners (7 implemented + 1 webflux placeholder/disabled)
   └─ .nojekyll
      │
      │  사용자 download 클릭
      ▼  https://github.com/JasonMMo/nexacroN-fullstack/releases/download/{channel}/{runnerKey}.{packaging}
[GitHub Releases — `nightly` + `stable` 태그]
   ├─ nightly (prerelease, 자동 덮어쓰기) — 매일 03:00 KST cron
   └─ stable  (수동 promote)               — Actions > promote-stable
      │
      │  매일 새벽
      ▼
[GitHub Actions — `main` 브랜치]
   ├─ runner-matrix.yml    ← cron + matrix build → `nightly` 자동 publish
   └─ promote-stable.yml   ← workflow_dispatch → `nightly` → `stable` 복사 (PR #46 머지 대기)
      │
      │  CI 가 빌드하는 자료
      ▼
[Source repo `JasonMMo/nexacroN-fullstack` main]
   ├─ samples/runners/<7개>/      ← 각 러너 pom (4-block <resources>/<webResources> 레이어링)
   ├─ nxui/packageN/              ← 소스 XML (.xfdl/.xjs/.xadl/.xprj) + nexacrolib + license
   └─ nxui-build/packageN/        ← nexacrodeploy.exe 출력 (.js + HTML5 wrapper + _resource_ + start.json)
                                    ↑ source 와 형제 트리. CI 가 도구 접근 불가하므로 git 추적.
```

---

## 운영 SOP

### A. 일상 — 무손작업

매일 03:00 KST 에 `runner-matrix.yml` 이 자동으로:
1. 4 활성 러너 빌드 (`boot-jdk17-jakarta`, `mvc-jdk17-jakarta`, `mvc-jdk8-javax`, `egov4-mvc-jdk8-javax`)
2. smoke (boot reachability + `/uiadapter/packageN/index.html` 200)
3. `nightly` 태그에 `{runnerKey}.{packaging}` 파일명으로 덮어쓰기 publish

→ 셀렉터의 `nightly` 라디오 즉시 갱신. `stable` 은 불변.

### B. stable 채널 promote (1주~ 단위, 수동)

**현재 (PR #46 머지 전):**
```bash
# 1. nightly 자산 7개 다운로드
mkdir promote && cd promote
gh release download nightly --repo JasonMMo/nexacroN-fullstack

# 2. stable 에 --clobber 업로드
gh release upload stable * --clobber --repo JasonMMo/nexacroN-fullstack

# 3. (선택) 릴리스 노트에 promote 시점 기록
```

**PR #46 머지 후:**
- GitHub Actions → **promote-stable** → Run workflow
- `source_tag` (default: `nightly`) + `dry_run` (default: false) 만 결정
- dry_run=true 로 한번 돌려 자산 목록 확인 → false 로 본실행
- 릴리스 노트는 자동으로 timestamp/source SHA/actor/asset list 갱신

### C. 새 러너 추가

1. `samples/runners/<new>/` 디렉토리 생성, 4-block pom 레이어링 적용
2. `runner-matrix.yml` `matrix.include` 에 `{ runner: <new>, jdk: N, smoke: jar|war }` 추가
3. 이 repo `plugins/nexacro-fullstack-starter/skills/.../assets/matrix.json` 에 새 키 추가
4. upstream `gh-pages` `matrix.json` 동기화 (현재 수동 — v1.1 task #3)
5. PR 머지 → 다음 nightly cron 으로 자산 자동 생성

### D. 회귀 발생 시 (사용자 보호)

- 셀렉터 default = `stable` 이므로 사용자가 별도 토글 없이는 `nightly` 회귀에 노출 안됨
- 깨진 nightly 가 stable 로 진입한 경우: 이전 정상 시점의 commit SHA 를 source_tag 로 못 씀(태그 단위 promote 만 지원). 대안: 정상 시점 자산을 로컬에 보관해뒀다가 `gh release upload stable * --clobber` 로 수동 롤백.

---

## 검증 결과 (M5 + M6, 2026-05-22)

| 단계 | 항목 | 결과 |
|---|---|---|
| M5-1 | 새 아키텍처(source/build 트리 분리) CI 통과 | nightly run [26274968141](https://github.com/JasonMMo/nexacroN-fullstack/actions/runs/26274968141) 4/4 SUCCESS |
| M5-2 | nightly 자산 다운로드 → `frameLogin.xfdl.js` 내부 로그인 변수 코드 포함 | OK (`strArg = "userId=... password=..."` 발견) |
| M5-3 | `environment.xml.js` `{{BACKEND_URL}}` → `/uiadapter/` 치환 | placeholder 잔류 0건 |
| M5-4 | JDK 17 기동 + `POST /uiadapter/login.do` (hong/1111) | HTTP 200, `ErrorCode=0`, `dsList` 1 row |
| M6-1 | `stable` 릴리스 신규 생성 + 7 자산 업로드 | OK (4 신규 + 3 stale snapshot, 셀렉터 일관성 보존) |
| M6-2 | 7 URL `releases/download/stable/{key}.{pkg}` HEAD | ALL 200, sizes 177/185/188/174/177/161/174 MB |
| M6-3 | stable ↔ nightly size 일치 | OK (etag 는 GH Storage 재할당으로 상이 — 정상) |
| M6-4 | 셀렉터 `stable` default 렌더 (별도 토글 없이도 stable 받음) | OK (`index.html` 134 `checked`) |

---

## v1.1 인계 작업 (3건)

### Task #1 — `stable` promote 워크플로화 ⏳

- **상태**: [PR #46](https://github.com/JasonMMo/nexacroN-fullstack/pull/46) open
- **남은 액션**: 리뷰 + 머지 + 첫 dry_run 실행으로 동작 확인
- **자동 cron promote 는 의도적으로 제외** — v1.x 에서 stable burn-in 데이터(N일 무사고) 축적 후 별도 결정

### Task #2 — webflux runner 활성화 (별도 트랙)

- **현재 상태**: `matrix.json` 에 `status: placeholder`, 셀렉터 UI 에서 `disabled` 옵션으로 노출
- **블로커**: 관련 부서 동의 필요 (사용자 사유, 2026-05-19 결정)
- **활성화 시 작업**:
  1. `samples/runners/webflux-jdk17-jakarta/` 디렉토리 신설 + 4-block pom
  2. `runner-matrix.yml` matrix 에 추가 + smoke 정의 (jar)
  3. `matrix.json` 의 `status` 를 `active` 로 변경
  4. 셀렉터 `disabled` 제거 (이 repo + upstream `gh-pages` 양쪽)

### Task #3 — matrix.json sync 자동화

- **현재 상태**: 수동 sync. 이 repo `plugins/.../assets/matrix.json` 이 단일 진실, upstream `gh-pages/matrix.json` 는 복사본
- **자동화 옵션**:
  - A. cross-repo PR-bot — 이 repo `matrix.json` 변경 push 시 upstream 에 PR 자동 생성
  - B. `gh-pages` 빌드 step 에서 raw.githubusercontent.com 으로 이 repo `matrix.json` fetch → 빌드 시점 sync (사실상 server-side include)
- **권장**: B (Pages 빌드 step 1개로 끝, PR 부담 없음)

### 비활성 3 러너 (별도 dep-fix PR 필요)

`runner-matrix.yml` 에 주석 처리된 3개:
- `boot-jdk8-javax` — hsqldb 2.7.3 needs Java 11
- `egov4-boot-jdk8-javax` — 동일 hsqldb 이슈
- `egov5-boot-jdk17-jakarta` — `log4j-slf4j2-impl` ↔ `log4j-to-slf4j` 충돌

이 3개의 stable 자산은 옛 nightly 시점의 stale snapshot 으로 유지 중. dep 해결 후 matrix 복원 → 자동 갱신.

---

## 트러블슈팅 노트

| 증상 | 원인 | 해법 |
|---|---|---|
| 셀렉터에서 다운로드 클릭 → 404 | 해당 `{runnerKey}.{packaging}` 자산이 `stable`(또는 `nightly`)에 없음 | promote 시 항상 **전체 7개 복사** (subset 금지). stale snapshot 이라도 자산 존재 보장. |
| nightly 빌드는 그린, `nxui` 변경이 반영 안됨 | nexacro 컴파일 산출물(`.xfdl.js` 등) 누락 — CI 는 `nexacrodeploy.exe` 미보유 | 로컬에서 `nexacrodeploy.exe` 로 재생성 후 `nxui-build/packageN/` 트리 통째로 커밋. `.xfdl` 단독 커밋 금지. |
| stable ↔ nightly etag 다른데 content 같음? | GitHub Storage 가 re-upload 시 etag 재할당 | size 일치 + SHA-256 일치로 검증 (etag 신뢰 X). |
| `POST *.do` 가 license 에러 | 평가 라이선스 만료 / 미동봉 | `samples/runners/NexacroN_server_license.xml` 교체. v1 셀렉터 다운로드 자산에는 평가 라이선스가 동봉되어 있음(`.gitignore` 예외). |
| Pages 변경이 즉시 반영 안됨 | Pages build queue | `gh api repos/JasonMMo/nexacroN-fullstack/pages/builds/latest` 로 `status: built` 확인 |

---

## 다음 세션이 읽을 파일 (우선순위)

1. **본 문서** — v1 완료 시점 상태 + v1.1 인계
2. **`RESUME.md` "트랙 B" 행** — 최신 상태 (이정표 ✅ 마킹, decisions log)
3. **`docs/superpowers/specs/2026-05-19-runner-download-service-design.md`** — D1–D5 결정 근거 (변경 없음, 참조용)
4. **upstream `.github/workflows/runner-matrix.yml`** — nightly 자동화 (변경 시 영향 큼)
5. **upstream `.github/workflows/promote-stable.yml`** (PR #46 머지 후) — stable promote 자동화

---

## 산출물 거주처 (변경 없음, 2026-05-19 표 유지)

| 산출물 | 거주처 |
|---|---|
| 워크플로 (runner-matrix, promote-stable) | upstream `JasonMMo/nexacroN-fullstack` `main` `.github/workflows/` |
| 셀렉터 HTML/JS (배포본) | upstream `JasonMMo/nexacroN-fullstack` `gh-pages` branch |
| 셀렉터 초안 (작업용) | 이 repo `docs/web-selector-draft/` |
| 설계 spec + handoff | 이 repo `docs/superpowers/specs/`, `docs/handoffs/` |
| matrix.json 단일 진실 | 이 repo `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json` |
| 릴리스 자산 (jar/war) | upstream `Releases` (`nightly`, `stable` 태그) |

---

## 관련 PR / 링크

- M2 [PR #38](https://github.com/JasonMMo/nexacroN-fullstack/pull/38) — runner-matrix.yml publish step
- M3 [PR #39](https://github.com/JasonMMo/nexacroN-fullstack/pull/39) — `workflow_dispatch.inputs.publish` 토글
- M4 — `gh-pages` orphan 시드 (root-commit `3ad4d67`) + webflux disable hotfix (`c668951`)
- 사이드 [PR #45](https://github.com/JasonMMo/nexacroN-fullstack/pull/45) — 로그인 변수 전달 (`frameLogin.xfdl` `strArg`)
- 사이드 commits `4929192`/`bcb6b8a`/`b9584d3` — 소스/빌드 트리 분리 아키텍처 (M5 검증으로 확인)
- v1.1 task #1 [PR #46](https://github.com/JasonMMo/nexacroN-fullstack/pull/46) — promote-stable workflow
- 셀렉터 (운영 중): https://jasonmmo.github.io/nexacroN-fullstack/
- 가이드 문서 한글 / PR·커밋·코드 주석 영문 (트랙 공통 규약)
