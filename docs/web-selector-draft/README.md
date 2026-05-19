# 웹 셀렉터 초안 작업 폴더 (트랙 B)

이 폴더는 **이주 예정 초안**. 완성되면 upstream `JasonMMo/nexacroN-fullstack` 의 `gh-pages` 브랜치로 옮겨 배포됩니다. 이 repo 에는 머물지 않습니다.

## 무엇이 들어오나

- `index.html` — 셀렉터 페이지 (JDK / framework / channel 입력)
- `selection.js` — `matrix.json` 로드 + `derivationRules` + `rejectedCombinations` 평가 + 다운로드 링크 생성
- `matrix.json` — 이 repo `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json` 의 카피 (수동 sync 또는 빌드 단계 자동화)

## 설계 근거

- 핸드오프: `docs/handoffs/2026-05-19-runner-build-service.md`
- 정식 spec: `docs/superpowers/specs/2026-05-19-runner-download-service-design.md`

## 이주 시점

PR-B (upstream `gh-pages` 신설) 작성 시. 이 폴더에서 검증 끝낸 그대로 복사하여 upstream PR 첨부.

## 절대 하지 말 것

- 이 폴더의 산출물을 이 repo `gh-pages` 브랜치로 push (이 repo에는 Pages 미사용).
- `matrix.json` 을 이 폴더에서만 수정 — 단일 진실은 `plugins/.../assets/matrix.json`. 본 폴더 카피는 sync 대상.
