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

- **상태**: M1 + M2-draft 통과 (2026-05-19) — 셀렉터 3-파일 + V1–V8 검증 + PR-A patch 초안 완료
- **이정표 (M0–M6)**:
  - ✅ M0 설계 결정 (D1–D5)
  - ✅ M1 셀렉터 정적 3-파일 + 로컬 logic 검증 (7 valid + 3 거부 + 채널 토글 ALL PASS)
  - 🟡 M2 PR-A — patch 초안 작성됨 (`docs/web-selector-draft/_pr-a-draft.md`), **upstream 클론에서 PR 작성 대기**
  - ⏳ M3 첫 nightly 자동 실행 → 7 자산 release 게시 확인
  - ⏳ M4 PR-B — upstream `gh-pages` 신설 + 셀렉터 이주
  - ⏳ M5 end-to-end smoke (브라우저 → java -jar)
  - ⏳ M6 `stable` 채널 첫 promote
- **단일 진실 파일**:
  - `docs/handoffs/2026-05-19-runner-build-service.md` — 핸드오프 (결정 반영본 + PR-A 명명 규약)
  - `docs/superpowers/specs/2026-05-19-runner-download-service-design.md` — 정식 설계 spec
  - `docs/web-selector-draft/_pr-a-draft.md` — M2 patch 초안 (다음 세션 입력)
- **다음 액션 (M2 실행)**: 별도 세션·별도 클론 `D:\AI\workspace\nexacroN-fullstack\` 에서 `_pr-a-draft.md` 의 diff 적용 → PR 작성 → 머지 후 1차 nightly 자산 7개 검증
- **작업 초안 폴더 (이 repo)**: `docs/web-selector-draft/` — `index.html`, `selection.js`, `matrix.json` (verbatim sync), `_pr-a-draft.md`. 완성되면 upstream `gh-pages` 로 이주 (`_*` 파일은 이주 제외)
- **재개 첫 메시지**: `@RESUME.md 트랙 B 재개. M2 PR-A 작성 단계. 참조: docs/web-selector-draft/_pr-a-draft.md`

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
