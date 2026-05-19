# PR-B 초안 — upstream `gh-pages` 신설 + 셀렉터 3-파일 이주

> **거주 repo**: `JasonMMo/nexacroN-fullstack` (이 repo 아님 — 별도 클론에서 적용)
> **목적**: 트랙 B 셀렉터 정적 페이지를 upstream `gh-pages` 브랜치로 이주하고 GitHub Pages 호스팅 활성화
> **계약**: 셀렉터의 `buildUrl()` 가 `nightly` 태그의 7 자산을 정확히 가리킨다 (PR-A 결과 사용)
> **선행 조건**: M3 통과 — `gh release view nightly` 에 7개 자산 정확 게시 확인됨
> **생성**: 2026-05-19, M3 대기 중 사전 작성

---

## 0. 사전 검증 (M3 → M4 게이트)

이 PR 작업 *시작 전* 다음 1번이라도 실패하면 M4 진입 보류:

```bash
gh release view nightly --repo JasonMMo/nexacroN-fullstack \
  --json assets --jq '[.assets[].name] | sort' | tee /tmp/nightly-names.json
# expect (sorted):
# ["boot-jdk17-jakarta.jar","boot-jdk8-javax.jar","egov4-boot-jdk8-javax.jar",
#  "egov4-mvc-jdk8-javax.war","egov5-boot-jdk17-jakarta.jar",
#  "mvc-jdk17-jakarta.war","mvc-jdk8-javax.war"]

curl -sI https://github.com/JasonMMo/nexacroN-fullstack/releases/download/nightly/boot-jdk17-jakarta.jar | head -1
# expect: HTTP/2 302
```

---

## 1. 적용 절차 (다음 세션 — upstream 클론)

> 메인 클론(`D:\AI\workspace\nexacroN-fullstack\`)에서 진행. 워크트리도 무방.

```powershell
# 0) 이 repo 의 셀렉터 3-파일을 새 빈 디렉토리로 미리 복사 (안전망)
$src = 'D:\AI\workspace\nexacro-claude-skills\.claude\worktrees\beautiful-matsumoto-3984eb\docs\web-selector-draft'
$stage = 'D:\AI\workspace\_stage-ghpages'
New-Item -ItemType Directory -Force $stage | Out-Null
Copy-Item "$src\index.html","$src\selection.js","$src\matrix.json" $stage

# 1) upstream 클론으로 이동, gh-pages 오펀 브랜치 신설
cd D:\AI\workspace\nexacroN-fullstack
git fetch origin
git checkout --orphan gh-pages
git rm -rf .                                # 모든 추적 파일 제거 (오펀이라 빈 commit)
git clean -fdx                              # 추적되지 않는 파일까지 정리

# 2) 셀렉터 3-파일 + .nojekyll 배치
Copy-Item "$stage\index.html","$stage\selection.js","$stage\matrix.json" .
New-Item -ItemType File .nojekyll | Out-Null

# 3) 검증: 3개 파일 + .nojekyll 만 존재
git status --short
# expect: A index.html / A matrix.json / A selection.js / A .nojekyll

# 4) commit + push
git add index.html selection.js matrix.json .nojekyll
git commit -m "feat(web): seed gh-pages with selector v1 (3 files + .nojekyll)"
git push -u origin gh-pages

# 5) GitHub UI: Settings → Pages → Source = "Deploy from a branch"
#    Branch = gh-pages / (root). Save. 1–2분 후 https://jasonmmo.github.io/nexacroN-fullstack/ 활성.
```

---

## 2. 왜 오펀 브랜치인가

- **격리**: `main` 의 자바 코드와 Pages 자산을 동일 history 에 섞지 않음. `git log gh-pages` 가 자산 변경만 포함.
- **공간**: 오펀이라 main commit graph 복사 안 됨.
- **convention**: `gh-pages` 라는 이름 자체가 GitHub Pages 표준 분기.

대안(거부): main 의 `/docs` 폴더에서 Pages serve. 거부 이유 — main history 가 셀렉터 작업으로 오염되고, matrix.json 자동 sync workflow 추가 시 push loop 위험.

---

## 3. 왜 `.nojekyll` 인가

- GitHub Pages 기본 = Jekyll. Jekyll 은 `_` 시작 파일/폴더를 빌드 제외.
- 우리는 `_*` 파일을 이주하지 않기로 했지만, 미래 추가될 수도 있고 vendor JS(예: `_nuxt`, `_next`)와 충돌 방지로 disable 이 안전.
- 0-byte 파일 하나로 끝.

---

## 4. 왜 GitHub Actions 자동 배포 워크플로 *안 만드는가* (v1 단순화)

- 트랙 B v1 = "수동 sync, 단순함이 무기" (RESUME.md §트랙 충돌 방지 #2 정신).
- matrix.json 변경 시 사람이 이 repo `affects: web-selector` 태그 커밋 → 다음 PR-B' (sync 전용 PR) 에서 한 줄 복사. v1.1 에서 자동화.

---

## 5. PR 본문 초안 (영문)

```
## Summary

- Seed new `gh-pages` orphan branch with the Track B static selector (3 files + `.nojekyll`)
- Enables https://jasonmmo.github.io/nexacroN-fullstack/ as the public runner-selection UI
- Selector resolves (jdk, framework) -> runner key, evaluates rejected combinations,
  and emits a download URL pointing to the rolling `nightly` release (created by PR #38)

## Files

- index.html        — selector page (radio + select + result panel)
- selection.js      — pure-JS rule evaluation + URL assembly (no build chain)
- matrix.json       — verbatim copy of the upstream skills repo's matrix
- .nojekyll         — disable Jekyll processing (we are not a Jekyll site)

## How it works

1. User picks JDK (8|17) and framework (boot|mvc|egov-boot|egov-mvc)
2. selection.js calls findRunner() against matrix.runners
3. If a rejection rule matches, show the reason; otherwise show the download URL
4. URL pattern: ${RELEASE_BASE}/${channel}/${runnerKey}.${packaging}
   - RELEASE_BASE = github.com/JasonMMo/nexacroN-fullstack/releases/download
   - channel = nightly (v1 default; stable in v1.1)

## Activation

After merge:
1. Settings → Pages → Source = "Deploy from a branch"
2. Branch = gh-pages / (root)
3. Save. Public URL live within 1–2 minutes.

## Test plan

- [ ] After merge + Pages enable, fetch https://jasonmmo.github.io/nexacroN-fullstack/
      returns HTTP 200 with selector form rendered
- [ ] Picking (17, boot) shows download URL containing `boot-jdk17-jakarta.jar`
      and `curl -I` on that URL returns 302
- [ ] Picking (8, jakarta-incompatible combo) shows a rejection reason
- [ ] Browser DevTools network tab: matrix.json fetched from `./matrix.json`
      (same origin, no CORS)

## Rollback

- `git push origin --delete gh-pages` removes the branch
- GitHub Pages auto-disables when source branch missing
- No effect on main / nightly release
```

---

## 6. 정합성 체크 (4-필터)

| 필터 | 결과 | 근거 |
|---|---|---|
| F1 북극성 진척 | ✅ | M4 (선택 UI 가동) 의 직접 입력. 사용자 = 브라우저로 jar/war 선택 → 다운로드. |
| F2 D1–D5 위반 없음 | ✅ | 백엔드 0 / PAT 0 (push 만 사용) / 라이선스 = 상위 repo 그대로 / 재빌드 없음 / Pages 정적 호스팅. |
| F3 M5 입력 | ✅ | end-to-end smoke = 브라우저로 셀렉터 열어 jar URL 받기 → `java -jar` 실행. Pages 활성화가 M5 의 선행. |
| F4 롤백 ≤ 1커밋 | ✅ | `gh-pages` 브랜치 삭제 = 1 명령. Pages source 분기 사라지면 자동 비활성. main 무영향. |

---

## 7. M4 종료 정의 (Definition of Done)

다음 모두 충족 시 M4 통과 → M5 자동 진입:

1. `gh-pages` 브랜치가 upstream 에 존재, 3 파일 + `.nojekyll` 만 포함
2. Settings → Pages 에서 source = `gh-pages` / root 로 설정됨
3. `curl -sI https://jasonmmo.github.io/nexacroN-fullstack/` → `HTTP/2 200`
4. `curl -s https://jasonmmo.github.io/nexacroN-fullstack/matrix.json | jq '.nexacroVersions.nexacroN.runners | keys | length'` → `7`
5. 셀렉터에서 (jdk=17, framework=boot) 선택 시 표시되는 다운로드 URL = `${RELEASE_BASE}/nightly/boot-jdk17-jakarta.jar`

---

## 8. 위험과 대응

| 위험 | 가능성 | 영향 | 대응 |
|---|---|---|---|
| `git checkout --orphan` 후 실수로 main 파일 commit | 낮음 | 높음 (Pages 가 자바 코드 노출) | 절차 §1 의 `git rm -rf . && git clean -fdx` 필수. `git status --short` 검증 게이트. |
| Pages 활성화가 GitHub UI 수동 단계 | 100% | 낮음 | PR 본문 §Activation 에 명시. v1.1 에서 `actions/configure-pages` 워크플로로 자동화. |
| matrix.json 의 cross-origin fetch 실패 | 매우 낮음 | 높음 | `./matrix.json` 상대 경로 = 동일 origin. CORS 없음. |
| `nightly` release 가 만료/삭제 | 낮음 | 중간 | release publish 워크플로 (PR-A) 가 매 nightly 갱신. 셀렉터는 URL 만 합성, asset 존재는 GitHub Release 측에서 보장. |
| Jekyll 처리로 `_resource_` 같은 향후 파일 누락 | 중간 | 낮음 | `.nojekyll` 0-byte 파일로 사전 차단. |
| matrix.json 이 이 repo 의 것과 sync 안 됨 | 중간 | 중간 (사용자가 실제와 다른 옵션 봄) | RESUME.md §트랙 충돌 방지 #1 (`affects: web-selector` 태그 grep). v1.1 에서 sync workflow 자동화. |

---

## 9. 범위 밖 (이 PR 미포함)

- `stable` 채널 promote — M6
- matrix.json 자동 sync workflow — v1.1
- Custom domain — v1.2 검토
- 다국어 (영/한 토글) — 사용자 검토 후 v1.3

---

## 10. M4 다음 세션 시작 메시지 (복붙용)

```
@RESUME.md 트랙 B 재개. M4 PR-B 작성 단계 (gh-pages 신설).
참조: docs/web-selector-draft/_pr-b-draft.md (이 repo)
별도 클론에서 작업: D:\AI\workspace\nexacroN-fullstack\
사전 게이트: M3 통과 (gh release view nightly 에 7 자산 확인) 필수
```
