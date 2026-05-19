# Handoff — 2026-05-19

웹 셀렉터 → fullstack-starter JAR/WAR 다운로드 서비스 설계 착수.

> **2026-05-19 update (Opus `/think`):** D1–D5 결정 완료. v1 아키텍처는 **권고안 A (GitHub Releases 롤링 `nightly` 태그 + GitHub Pages 정적 셀렉터)** 로 확정. 핸드오프 §"아키텍처 옵션 v1" 의 Cloudflare Worker 가정은 실측(아티팩트 120–180MB) 으로 무효화 — 자세한 근거와 변형은 [`docs/superpowers/specs/2026-05-19-runner-download-service-design.md`](../superpowers/specs/2026-05-19-runner-download-service-design.md) 참조.

## 배경

지금까지 `nexacro-fullstack-starter` 플러그인은 Claude Code 내에서만 동작 — 사용자가
`/nexacro-fullstack-starter (jdk=17, framework=spring-boot, name=foo)` 를 호출하면 7개
런너 중 하나를 `samples/runners/<runner>/` 에서 로컬로 클론·rename 해 주는 방식.

다음 단계: **CLI 없는 사용자**에게 동일한 산출물을 웹에서 제공. 셀렉터 UI에서
JDK / framework / 패키징 선택 → JAR (boot/egov-boot) 또는 WAR (mvc/egov4-mvc) 를
즉시 다운로드.

## 사용자 흐름 (v1 확정)

```
[웹 셀렉터 (GitHub Pages)]
  └─ JDK: 8 / 17
  └─ Framework: spring-boot / spring-mvc / egov4-boot / egov4-mvc / egov5-boot
  └─ (자동 도출) servletApi, packaging, 런너명     ← matrix.json derivationRules
  └─ 거부 조합 차단                                ← matrix.json rejectedCombinations
  └─ 채널 토글: stable (기본) / nightly
[Download 링크 클릭]
  └─ <a href="https://github.com/JasonMMo/nexacroN-fullstack/releases/download/{channel}/{runner}.{ext}">
  └─ GitHub Releases CDN 이 직접 응답 (백엔드 0)
  └─ 사용자: java -jar <file>.jar --server.servlet.context-path=/myapp  (또는 WAR 배포)
```

## 기존 활용 자산

| 자산 | 위치 | 어떻게 쓰나 |
|---|---|---|
| 7-runner 매트릭스 CI | `JasonMMo/nexacroN-fullstack` `.github/workflows/runner-matrix.yml` | 매트릭스 그린 후 `softprops/action-gh-release@v2` step 추가 → `nightly` 태그에 7개 자산 덮어쓰기. |
| 런너 매트릭스 정의 | `samples/runners/<7개>/` + 각 README | 셀렉터 옵션 단일 출처. |
| Selector 도출 로직 | `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md` Step 2 거부 규칙 | 웹 UI 검증 로직(`framework × jdk` 매트릭스)을 그대로 JSON 으로 옮길 수 있음. |
| 런너 셀렉션 가이드 | `plugins/nexacro-fullstack-starter/references/runner-selection-guide.md` | 셀렉터 UI 의 "어떤 걸 골라야 하나요?" 도움말 원문. |
| matrix.json | `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json` | 7개 런너 메타데이터. Pages 빌드 시 동기화하여 정적 사용. |

## 아키텍처 결정 (v1 = 권고안 A 확정)

### v1 — GitHub Releases 롤링 태그 + 정적 셀렉터 ★

- 호스팅: **GitHub Pages** (셀렉터 정적 HTML/JS) + **GitHub Releases** (자산).
- 빌드 시점: 기존 nightly 매트릭스 CI 재활용. 워크플로에 release 발행 step 1개 추가.
- 흐름:
  1. 사용자 선택 → 셀렉터가 `{runner}` 키 결정 + 거부 조합 차단.
  2. 채널 토글 (`stable` / `nightly`) 로 태그 결정.
  3. `<a href="https://github.com/JasonMMo/nexacroN-fullstack/releases/download/{tag}/{runner}.{ext}">` 직접 링크 — GitHub Releases CDN 응답.
- **장점**: 백엔드 0. PAT 0. 인증 0. CDN 무료. 무기한 보관(태그 덮어쓰기까지).
- **제약**:
  - 사용자 입력(프로젝트명, context-path)이 바이너리에 반영 안 됨. → **fat-jar 특성상 무의미** — `--server.servlet.context-path=` 외부 인자로 99% 케이스 해결. 셀렉터에 1줄 안내.
  - 운영 라이선스 `NexacroN_server_license.xml` 미포함 — 셀렉터 안내 배너로 해결.
  - `nightly` 회귀가 사용자에게 노출될 위험. → `stable` 태그를 수동 promote, 셀렉터 기본값을 `stable` 로.

### v2 — 파라미터화된 on-demand Maven 빌드 (보류)

- 핸드오프 원안 그대로 보존. v1 안정화 후 별도 핸드오프로 진행.
- 추가 결정: 사용자 입력이 의미를 가지려면 **source ZIP 다운로드** + 클라이언트 측 sed 또는 `workflow_dispatch` 빌드 둘 중 하나여야 함.

### 기각된 옵션

- **Cloudflare Worker 가벼운 프록시** — 아티팩트 120–180MB / 개, 합 ~1.1GB. Worker 응답 100MB, Vercel Function 50MB 제한. 통과 모델 불가.
- **Worker가 302 redirect** — PAT 보관·rotation 운영 부담. A안 대비 백엔드 1개 추가하면서 얻는 게 없음 (CI 무변경뿐).
- **단일 Spring Boot 백엔드 스트리밍** — v1 "가볍게" 목표와 정면 충돌.

## 결정 완료 (D1–D5)

| # | 결정 | 결론 | 사유 |
|---|---|---|---|
| D1 | 호스팅 | **GitHub Pages + GitHub Releases**, Worker 미사용 | 아티팩트 크기로 Worker 통과 모델 불가. Pages는 무료·CDN·인증 zero. |
| D2 | 라이선스 처리 | 셀렉터 상단 안내 배너만. 자산에 미포함 명시 | upstream 확인 결과 어떤 산출물에도 라이선스 파일 없음. v1 범위 밖 (§범위 밖 line 95). |
| D3 | 프로젝트명 / context-path rewrite | **rewrite 없음**. CLI 인자 안내 1줄 | 아티팩트가 fat-jar — 재빌드 없이 artifactId rewrite는 무의미. 외부 인자로 99% 해결. v2에서 source ZIP 시 재검토. |
| D4 | webflux 런너 노출 | **disabled 옵션 (예정 라벨)** | matrix.json `status: placeholder` + CI matrix 미포함 = 아티팩트 0개. 자동 제외. |
| D5 | 다운로드 형태 | **raw `*.jar` / `*.war` 단일 파일** | 사용자가 즉시 `java -jar` 실행 가능. zip = unzip 단계 추가 = UX 악화. source ZIP은 v2. |

**추가 결정 (위에서 파생):**
- `stable` / `nightly` 듀얼 태그 채널. 셀렉터 기본 = `stable`.
- 셀렉터 페이지 위치: `JasonMMo/nexacroN-fullstack` 의 `gh-pages` 브랜치 (별도 repo 신설 X).
- `matrix.json` 단일 출처 유지 — Pages 빌드 시 동기화.

## 첫 세션이 읽어야 할 파일 (검증 완료, 그대로 진행)

1. **`JasonMMo/nexacroN-fullstack/.github/workflows/runner-matrix.yml`** — 7개 아티팩트 업로드 step 직후에 release publish step 삽입 지점.
2. **`plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/assets/matrix.json`** — 7개 런너 메타데이터 + 거부 규칙. Pages 정적 import 원본.
3. **`plugins/nexacro-fullstack-starter/references/runner-selection-guide.md`** — 셀렉터 UX 카피 원문.
4. **`samples/runners/boot-jdk17-jakarta/src/main/resources/application.yml`** — context-path 기본값 (`/uiadapter`) — CLI override 안내 문구의 근거.
5. **`docs/superpowers/specs/2026-05-19-runner-download-service-design.md`** — 본 핸드오프의 정식 설계 문서. 구현 시 단일 참조 지점.

## 검증 플랜 (v1)

1. **로컬 검증**: `gh run download <last-green-id>` 로 7개 아티팩트 받아 `java -jar` (boot 4개) / Tomcat 배포 (mvc 3개) → `/uiadapter/` 200 확인.
2. **CI 단계 PR (PR-A)**: `runner-matrix.yml` 에 release publish step 추가, `if: github.ref == 'refs/heads/main' && github.event_name == 'schedule'` 가드, 7개 자산 첨부. **명명 규약**: 자산 파일명은 정확히 `{runnerKey}.{packaging}` (예: `boot-jdk17-jakarta.jar`, `mvc-jdk8-javax.war`) — `docs/web-selector-draft/selection.js` 의 `buildUrl()` 와의 계약. 머지 후 첫 nightly에서 `gh release view nightly` 검증.
3. **Pages 단계 PR**: `gh-pages` 브랜치 신설, 셀렉터 HTML + matrix.json sync. 거부 조합 (`egov-mvc × jdk17`, `webflux × jdk8`) UI 차단 확인. 7개 옵션 각각 클릭 → 실제 다운로드 트리거 확인.
4. **롤백 시나리오**: 깨진 nightly 시나리오에서 `stable` 기본값이 사용자 영향 차단함을 확인.

## 범위 밖 (1차 PR)

- 사용자 인증/로그인
- 빌드 옵션 커스터마이즈 (Java 버전 외 라이브러리 버전 변경)
- nxui 프론트엔드 정적 자원 빌드 자동화 (별도 워크플로 필요)
- 운영 라이선스 발급 흐름
- 사용자별 빌드 히스토리 / 재다운로드
- `stable` 태그 자동 promote (수동으로 시작, v1.1에서 자동화 검토)

## 실행 역할 (CLAUDE.md 기준)

| 단계 | 모델 | 액션 |
|---|---|---|
| 설계 / Plan | Opus | ✅ 완료 — D1–D5 결정 + v1 = 권고안 A 확정 |
| CI 워크플로 step 추가 | Sonnet | upstream `JasonMMo/nexacroN-fullstack` 별도 클론에서 PR 1 |
| 셀렉터 UI | Sonnet | upstream `gh-pages` 브랜치 정적 HTML/JS — `matrix.json` import |
| 검증 | Sonnet `/check` | 7개 런너 다운로드 → 기동 smoke |

## 산출물 거주 repo 분리

| 산출물 | 거주 repo | 비고 |
|---|---|---|
| 워크플로 release step | `JasonMMo/nexacroN-fullstack` | 별도 클론 권장 — 이 repo와 섞지 않음 |
| 셀렉터 HTML/JS | `JasonMMo/nexacroN-fullstack` `gh-pages` | Pages 호스팅 |
| 설계 spec | **이 repo** `docs/superpowers/specs/2026-05-19-runner-download-service-design.md` | 단일 진실 |
| 본 핸드오프 | **이 repo** `docs/handoffs/2026-05-19-runner-build-service.md` | 결정 반영 완료본 (현재 파일) |
| `matrix.json` 단일 출처 | **이 repo** `plugins/nexacro-fullstack-starter/skills/.../assets/matrix.json` | Pages 빌드 시 sync |

## 관련 PR / 메모

- 직전 작업: PR [#35](https://github.com/JasonMMo/nexacroN-fullstack/pull/35) (sync automation Tier 1+2), PR [#36](https://github.com/JasonMMo/nexacroN-fullstack/pull/36) (orchestrator + dry-run hotfix + .md 현행화).
- 매트릭스 CI 그린 상태(2026-05-19 확인) — 아티팩트 7개 정상 생산, 크기 120–180MB.
- 가이드 문서는 한글 (PR/커밋/코드 주석은 영문).
