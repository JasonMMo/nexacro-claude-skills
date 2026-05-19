# Runner Download Service — Design Spec (v1)

- **Date**: 2026-05-19
- **Status**: Approved (user, 2026-05-19)
- **Author**: Claude (Opus `/think`)
- **Target consumer**: 웹 셀렉터 UI 사용자 (Claude Code CLI 비사용자)
- **Target plugin**: `plugins/nexacro-fullstack-starter/` (메타데이터 단일 출처)
- **Target upstream repo**: `github.com/JasonMMo/nexacroN-fullstack`
- **Source handoff**: [`docs/handoffs/2026-05-19-runner-build-service.md`](../../handoffs/2026-05-19-runner-build-service.md)

---

## 1. Overview & Goals

### 1.1 Problem

`nexacro-fullstack-starter` 플러그인은 Claude Code 내부에서만 동작 — CLI를 쓰지 않는 개발자는 7-런너 매트릭스 산출물을 쓸 수 없다. 다운로드 페이지가 없다.

### 1.2 Goal

웹 셀렉터 한 페이지에서 (JDK / framework / packaging) 조합을 선택 → 즉시 해당 `*.jar` 또는 `*.war` 파일 1개를 anonymous 다운로드.

### 1.3 Non-Goals (v1 범위 밖)

- 사용자 입력에 따른 `pom.xml` / `application.yml` rewrite (fat-jar 특성상 v1에서 무의미)
- 사용자 인증 / 라이선스 발급 / 로그인
- on-demand `workflow_dispatch` 빌드 (v2 별도 계획)
- nxui 정적 자원 패키징
- webflux 런너 (upstream `status: placeholder`, CI matrix 미포함)
- 빌드 히스토리 / 사용량 분석
- `stable` 태그 자동 promote (v1.1)

---

## 2. Design Decisions (D1–D5)

| # | 결정 | 결론 | 근거 |
|---|---|---|---|
| D1 | 호스팅 | **GitHub Pages + GitHub Releases** | 아티팩트 120–180MB → Worker(100MB), Vercel(50MB) 응답 한계 초과. Pages는 무료·CDN·인증 zero. |
| D2 | 라이선스 처리 | 셀렉터 안내 배너만 | upstream `samples/runners/**` + `xeni.properties` 어디에도 `NexacroN_server_license.xml` 미포함 확인. v1 범위 밖. |
| D3 | 프로젝트명 / context-path rewrite | rewrite 없음. CLI 인자 안내 | 아티팩트가 fat-jar (`xapi`/`uiadapter` inlined). 재빌드 없는 artifactId rewrite는 무의미. `--server.servlet.context-path=/myapp` 외부 인자로 99% 케이스 해결. |
| D4 | webflux 노출 | disabled (예정 라벨) | `matrix.json.runners.webflux-jdk17-jakarta.status == "placeholder"`. CI matrix 미포함 → 아티팩트 0개. |
| D5 | 다운로드 형태 | raw `*.jar` / `*.war` 단일 파일 | 즉시 `java -jar` 실행 가능. zip은 unzip 단계 추가로 UX 악화. source ZIP은 v2. |

### 2.1 채널 (위에서 파생)

| 태그 | 갱신 주기 | 셀렉터 기본값 | 회귀 노출 |
|---|---|---|---|
| `stable` | 수동 promote (v1.1 자동화 검토) | ✅ | 없음 (검증된 nightly만 promote) |
| `nightly` | 매일 03:00 KST (스케줄) | (토글 선택) | 있음 (사용자 동의 전제) |

---

## 3. Architecture

### 3.1 Data Flow

```
┌──────────────────────────────────────────────────┐
│ JasonMMo/nexacroN-fullstack (upstream repo)      │
│                                                  │
│  ┌──────────────────────┐                        │
│  │ .github/workflows/   │  (1) schedule 03:00 KST│
│  │ runner-matrix.yml    │      매트릭스 빌드     │
│  └─────────┬────────────┘                        │
│            │ (2) green 시                        │
│            ▼                                     │
│  ┌──────────────────────┐                        │
│  │ Releases: nightly    │  자산 7개 덮어쓰기      │
│  │  - boot-jdk17-jakarta.jar                     │
│  │  - boot-jdk8-javax.jar                        │
│  │  - mvc-jdk17-jakarta.war                      │
│  │  - mvc-jdk8-javax.war                         │
│  │  - egov5-boot-jdk17-jakarta.jar               │
│  │  - egov4-boot-jdk8-javax.jar                  │
│  │  - egov4-mvc-jdk8-javax.war                   │
│  └─────────┬────────────┘                        │
│            │ (3) 수동 promote                    │
│            ▼                                     │
│  ┌──────────────────────┐                        │
│  │ Releases: stable     │  (동일 7개)            │
│  └─────────┬────────────┘                        │
│            │                                     │
│  ┌─────────┴────────────┐                        │
│  │ gh-pages 브랜치       │                       │
│  │  - index.html        │  (4) 정적 셀렉터        │
│  │  - matrix.json       │      (synced)         │
│  │  - selection.js      │                        │
│  └─────────┬────────────┘                        │
└────────────┼─────────────────────────────────────┘
             │ (5) anonymous GET
             ▼
       [End user browser]
```

데이터 한 방향, 사이클 없음.

### 3.2 Components (3개)

| 컴포넌트 | 위치 | 역할 |
|---|---|---|
| **CI release step** | `.github/workflows/runner-matrix.yml` (기존 파일에 step 1개 추가) | 매트릭스 그린 시 `nightly` 태그에 7개 자산 덮어쓰기 |
| **Selector page** | `gh-pages` 브랜치 / `index.html` + `selection.js` (~200 LOC) | 사용자 선택 → 거부 규칙 검증 → release URL 생성 |
| **matrix.json sync** | `gh-pages` 브랜치 / `matrix.json` (이 repo의 assets/matrix.json 카피) | 셀렉터의 단일 진실. nexacro-claude-skills sync-automation 인프라 활용 검토 |

### 3.3 외부 의존성

| 항목 | 필요 | 비고 |
|---|---|---|
| `GITHUB_TOKEN` (워크플로 기본) | ✅ | release 발행 권한 — 추가 secret 불필요 |
| GitHub Pages 활성화 | ✅ (1회) | `JasonMMo/nexacroN-fullstack` Settings → Pages → Source: `gh-pages` |
| Cloudflare / Vercel / R2 | ❌ | 미사용 |
| 별도 PAT | ❌ | A안은 워크플로 기본 토큰으로 충분 |
| 운영 라이선스 발급 채널 | (안내 링크만) | v1 범위 밖 |

**mid-implementation에 새 자격증명 요청 없음.**

---

## 4. Implementation Plan

### 4.1 거주 repo 분리

| 산출물 | repo |
|---|---|
| 워크플로 release step | `JasonMMo/nexacroN-fullstack` (별도 클론에서 PR) |
| 셀렉터 페이지 | `JasonMMo/nexacroN-fullstack` `gh-pages` |
| 본 spec + 핸드오프 | `nexacro-claude-skills` (현재 repo) |
| `matrix.json` 단일 출처 | `nexacro-claude-skills/plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json` |

### 4.2 PR 순서

1. **PR-A (upstream)**: `runner-matrix.yml` 에 `softprops/action-gh-release@v2` step 추가
   - 가드: `if: github.ref == 'refs/heads/main' && github.event_name == 'schedule'`
   - 자산 7개 첨부 (`samples/runners/${{ matrix.runner }}/target/*.${{ matrix.smoke }}`)
   - tag: `nightly`, prerelease: true, replace: true
2. **PR-B (upstream)**: `gh-pages` 브랜치 신설
   - `index.html` — JDK 라디오 + framework select + packaging 자동 표시 + 거부 조합 비활성화 + 채널 토글 + 안내 배너 (D2)
   - `selection.js` — `matrix.json` 로드, `rejectedCombinations` 평가, `<a>` href 생성
   - `matrix.json` — 이 repo `assets/matrix.json` 의 카피 (수동 또는 sync 자동화)
3. **PR-C (this repo)**: `matrix.json` Pages sync 자동화 (선택, sync-automation Tier 1+2 후속)

### 4.3 Selector UX 요구사항

- 입력: JDK (8 / 17 라디오), Framework (select: spring-boot / spring-mvc / egov-boot / egov-mvc / webflux), Channel (stable / nightly 토글)
- 자동 도출: `servletApi`, `packaging`, `runner` 키 (matrix.json `derivationRules` 그대로)
- 차단: `rejectedCombinations` 매칭 시 다운로드 버튼 비활성화 + 사유 안내
- 안내 배너 (상단 고정):
  - "운영 라이선스 `NexacroN_server_license.xml` 별도 발급 필요. 다운로드 산출물에 미포함."
  - "context-path 변경: `java -jar app.jar --server.servlet.context-path=/myapp`"
- 도움말 링크: `runner-selection-guide.md` (이 repo) 원본

---

## 5. Verification Plan

| # | 단계 | 통과 기준 |
|---|---|---|
| 1 | 로컬 — 기존 nightly artifact 다운로드 후 7개 모두 `java -jar` 또는 Tomcat 배포 | `/uiadapter/` 200, smoke endpoint 정상 |
| 2 | PR-A 머지 후 첫 nightly | `gh release view nightly --repo JasonMMo/nexacroN-fullstack` 에서 7개 자산 확인 |
| 3 | PR-B 머지 후 Pages 활성화 | `https://jasonmmo.github.io/nexacroN-fullstack/` 셀렉터 로드 |
| 4 | 7개 옵션 각각 클릭 → 다운로드 트리거 | 모두 200, 파일 크기 120–180MB 범위 |
| 5 | 거부 조합 (`egov-mvc + jdk17`, `webflux + jdk8`) | 다운로드 버튼 비활성화 + 사유 텍스트 표시 |
| 6 | 롤백 시뮬 — `nightly` 일부러 깨뜨림 | 셀렉터 기본 `stable` 채널 사용자에게 영향 없음 |

---

## 6. Attack Angle Analysis (`/think` 결과)

| 각도 | 시나리오 | 결과 |
|---|---|---|
| Dependency failure | GitHub Releases 다운 | 다른 GH 자원과 동일 blast radius — 허용 |
| Scale explosion | 10× 사용자 | GitHub Releases CDN은 GB/s 급. 병목 없음 |
| Rollback cost | nightly 회귀 | `stable` 기본값이 직전 검증본을 가리킴 → 사용자 영향 없음 |
| Premise collapse | 가장 약한 전제 | "정적 호스팅으로 충분" — 라이선스/인증 붙으면 백엔드 필요. v1 범위 밖 명시로 차단 |

4각 모두 통과. 변형 없음.

---

## 7. Rollback

- 셀렉터 페이지: `gh-pages` 브랜치 revert 1 commit
- CI release step: `runner-matrix.yml` 의 release step만 제거 (매트릭스 본체 무관)
- 데이터 보전: GitHub Releases 자산은 태그 덮어쓰기 외에는 자동 삭제 없음. 사용자 다운로드 URL은 새 nightly까지 유효

---

## 8. v2 Preview (참고, 본 spec 범위 밖)

사용자 맞춤 산출물(프로젝트명, context-path rewrite)이 필요해지면:

- **Option v2-A**: source ZIP 다운로드 + 클라이언트 측 sed 안내 — 정적 호스팅 유지 가능
- **Option v2-B**: `workflow_dispatch` 기반 on-demand 빌드 + 폴링 응답 — 90–180초 대기, 백엔드 필요

v1 안정화 후 별도 핸드오프에서 결정.
