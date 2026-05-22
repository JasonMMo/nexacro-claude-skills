# Resume — 어디까지 했지?

> 오랫만에 다시 들어왔다면 이 파일이 라우터.
> 첫 메시지: `@RESUME.md 지금 어디까지 했는지 알려줘.`

이 파일이 모든 트랙의 단일 진입점. 트랙을 추가하거나 상태가 바뀔 때마다 여기만 갱신.

---

## Active tracks

### 트랙 A — fullstack-starter 스킬 개선

- **상태**: idle
- **단일 진실 파일**:
  - `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md`
  - `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json`
- **다음 액션**: (정의되지 않음 — 작업 시작 시 여기 한 줄 채우기)
- **재개 첫 메시지**: `@RESUME.md 트랙 A 재개`

### 트랙 B — 웹 사용자 다운로드 서비스

- **상태**: M4 통과 (2026-05-19) — Pages 활성화 + 빌드 완료. webflux 옵션은 `disabled` 처리 (matrix 보존 + UI 노출 차단). M5 smoke 진입 준비
- **이정표 (M0–M6)**:
  - ✅ M0 설계 결정 (D1–D5)
  - ✅ M1 셀렉터 정적 3-파일 + 로컬 logic 검증 (7 valid + 3 거부 + 채널 토글 ALL PASS)
  - ✅ M2 PR-A — [JasonMMo/nexacroN-fullstack#38](https://github.com/JasonMMo/nexacroN-fullstack/pull/38) 머지됨 (2026-05-19, 7/7 build SUCCESS)
  - ✅ M3 nightly release — [#39](https://github.com/JasonMMo/nexacroN-fullstack/pull/39) 으로 `workflow_dispatch.inputs.publish` 추가 → run [26078797224](https://github.com/JasonMMo/nexacroN-fullstack/actions/runs/26078797224) 으로 7 자산 정확한 파일명·정확한 개수 게시. 7개 URL `HTTP -IL` 200 최종 (302 chain 정상)
  - ✅ M4 PR-B — `gh-pages` orphan (root-commit `3ad4d67`) + webflux disable hotfix (`c668951`). Pages `status: built`, `https://jasonmmo.github.io/nexacroN-fullstack/` → 200, `matrix.runners` 8 (webflux 보류 항목 1개 포함, UI 에서 `disabled`). DoD 1·2·3·5 통과, DoD-4 = "선택 가능 옵션 = 7" 으로 재해석 통과
  - ⏳ M5 end-to-end smoke (브라우저 → java -jar)
  - ⏳ M6 `stable` 채널 첫 promote
- **단일 진실 파일**:
  - `docs/handoffs/2026-05-19-runner-build-service.md` — 핸드오프 (결정 반영본 + PR-A 명명 규약)
  - `docs/superpowers/specs/2026-05-19-runner-download-service-design.md` — 정식 설계 spec
  - `docs/web-selector-draft/_pr-a-draft.md` — M2 patch 초안 (적용 완료, 참고용 보존)
  - `docs/web-selector-draft/_pr-b-draft.md` — M4 patch 초안 (gh-pages 신설, M3 통과 후 적용)
- **다음 액션 (M5)**: 브라우저에서 `https://jasonmmo.github.io/nexacroN-fullstack/` 열기 → (JDK=17, framework=spring-boot, channel=nightly) → 표시된 URL 로 `.jar` 다운로드 → `java -jar boot-jdk17-jakarta.jar` → `http://localhost:8080/uiadapter/` 200 확인. webflux 옵션이 회색 처리·선택 불가 시각 검증도 함께. M5 DoD 정의는 다음 세션에서 수립.
- **작업 초안 폴더 (이 repo)**: `docs/web-selector-draft/` — `index.html`, `selection.js`, `matrix.json` (verbatim sync), `_pr-a-draft.md`, `_pr-b-draft.md`. 완성되면 upstream `gh-pages` 로 이주 (`_*` 파일은 이주 제외)
- **재개 첫 메시지**: `@RESUME.md 트랙 B 재개. M5 end-to-end smoke 시작.`

---

## 작업물 거주 규칙

| 분류 | 거주처 |
|---|---|
| 스킬 / 플러그인 코드 | 이 repo `plugins/` |
| 설계 / handoff / spec | 이 repo `docs/` |
| 트랙 B 셀렉터 초안 (HTML/JS) | 이 repo `docs/web-selector-draft/` |
| 트랙 B 최종 배포본 (workflow + `gh-pages`) | upstream `JasonMMo/nexacroN-fullstack` |

---

## 트랙 충돌 방지 규칙

1. `matrix.json` 수정 시 커밋 메시지에 `affects: web-selector` 태그 — 트랙 B 재개 시 grep 으로 영향 탐지.
2. 트랙 B는 이 repo 에 코드 안 쓴다. 초안만. 최종은 upstream.
3. PR 제목 prefix: 트랙 A = `feat(skill):` / `docs(skill):`, 트랙 B = `feat(web):` / `docs(web):`.

---

## Recent decisions log

- **2026-05-19** — 트랙 B v1 아키텍처 = GitHub Pages 정적 셀렉터 + GitHub Releases 롤링 `nightly` 태그. Cloudflare Worker 안 기각 (아티팩트 120–180MB > Worker 100MB 응답 한계). 상세: 위 트랙 B 단일 진실 파일 2개.
- **2026-05-19** — 작업 폴더 분리 X. 두 트랙 모두 이 repo + 이 워크트리에서 진행. 미래 망각 방지로 본 `RESUME.md` 가 라우터.
- **2026-05-19** — 트랙 B 셀렉터 3-파일 초안 작성 완료 (`index.html`, `selection.js`, `matrix.json` verbatim). PR-A 자산 명명 규약 = `{runnerKey}.{packaging}` 핸드오프에 명시.
- **2026-05-19** — M1 V1–V8 ALL PASS (HTTP 200×3, 7 valid URL, 3 거부 사유, 채널 토글). M2 PR-A patch 초안 작성 (`docs/web-selector-draft/_pr-a-draft.md`) — upstream 워크플로 read-only 확인 후 unified diff + 정합성 4-필터 + DoD + 위험 표 포함. 이정표 M0–M6 체계 도입.
- **2026-05-19** — M2 통과. PR-A([JasonMMo/nexacroN-fullstack#38](https://github.com/JasonMMo/nexacroN-fullstack/pull/38)) 머지 — `permissions: contents: write` + `rename artifact` + `softprops/action-gh-release@v2` publish step. 7/7 build SUCCESS. M3 = 다음 nightly cron 대기.
- **2026-05-19** — M3 cron 대기 중 M4 PR-B 초안 사전 작성 (`docs/web-selector-draft/_pr-b-draft.md`). orphan `gh-pages` 분기 + 3-파일 + `.nojekyll` seed, Pages 수동 활성, DoD 5개·위험 6개·4-필터 통과. v1.1 sync 자동화 분리.
- **2026-05-19** — M3 통과 (cron 대기 우회). 옵션 C 선택 — PR-A2([#39](https://github.com/JasonMMo/nexacroN-fullstack/pull/39))로 `workflow_dispatch.inputs.publish` boolean (default false) 추가. v1.1 "수동 promote" feature를 1릴리스 앞당겨 영구 채택. manual run [26078797224](https://github.com/JasonMMo/nexacroN-fullstack/actions/runs/26078797224) 7/7 SUCCESS, 7 자산 정확한 이름·개수, 302 chain 정상. M4 진입.
- **2026-05-19** — M4 push 단계 완료. 옵션 A 선택 (이 세션 내 적용). `git worktree add --orphan -b gh-pages D:\AI\workspace\_gh-pages-tmp` 로 격리, 4 파일 시드 후 root-commit `3ad4d67` → `origin/gh-pages` push 성공. `gh api contents?ref=gh-pages` 로 원격 4 파일 (.nojekyll, index.html, matrix.json, selection.js) 정확 게시 확인 (DoD-1 통과). 임시 worktree 정리됨. 남은 DoD-2~5 = 사용자 GitHub UI Pages 활성화 후 자동 검증 가능.
- **2026-05-19** — M4 통과. Pages 활성화는 이미 완료 상태(Save 버튼 비활성=변경 없음, `gh api .../pages` 로 `status: built` 확인). DoD-4 정합성 이슈 발견 — matrix.json 에 `webflux-jdk17-jakarta` 8번째 runner 존재(개발 진행 중)이나 nightly release 에는 7 자산만 있어 webflux 선택 시 404 URL 위험. 결정: matrix.json 단일 진실은 보존(향후 추가될 webflux runner 마커), UI `<option value="webflux" disabled>` 로 노출 차단. 두 곳 hotfix — skills repo `index.html` (commit `05cc808`) + upstream gh-pages (commit `c668951`). Pages build `status: built` (commit `c668951`) 확인. DoD-4 = "UI 선택 가능 옵션 = 7" 으로 의미 재해석 통과. 사용자 사유: "관련부서 동의 필요, 시간 소요". v1.x 에 webflux 활성화 별도 트랙으로 분리.
- **2026-05-22** — (트랙 외 사이드 수정) upstream `JasonMMo/nexacroN-fullstack` 로그인 변수 전달 변경 머지. `frameLogin.xfdl` 의 `strArg` 를 빈 문자열 → `"userId=... password=..."` 로 수정해서 서버 `@ParamVariable("userId")` / `@ParamVariable("password")` 계약과 정렬. 흐름: `feat/login-credentials` 브랜치 → [PR #45](https://github.com/JasonMMo/nexacroN-fullstack/pull/45) 머지 → boot-jdk17-jakarta 러너 빌드 + 브라우저 E2E 검증 (`POST /uiadapter/login.do → 200`, `strArg = "userId=hong password=1111"` 캡처) → 머지 후 compiled artifact gap 발견 (`frameLogin.xfdl.js` 가 PR 에 누락) → `nexacrodeploy.exe` 로 재생성 → main 에 직접 후속 커밋 `ee14028` push, `feat/login-credentials` 로컬·원격 삭제. 교훈: `.xfdl` 수정 시 `.xfdl.js` 동반 커밋 필수 (브라우저는 `.xfdl.js` 만 로드).
