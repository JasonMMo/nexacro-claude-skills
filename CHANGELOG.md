# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.8.1] - 2026-04-24

### Added
- **`nxui/packageN` 프로젝트 본체** (`nexacroN-fullstack` 모노레포, tag `v0.4.0-nxui-packageN`)
  - `asis/jakarta-example/src/main/nxui/packageN` 기반 (1531 파일 / 56 MB)
  - `packageN.xprj`, `packageN.xadl`, `appvariables.xml`, `environment.xml`
  - `_resource_/` (theme, initvalue, images, font, xcss) + `nexacrolib/` (1379 파일 / 55 MB) 런타임
  - `frame/` 8종 (frameBottom/Left/Login/Main/MDI/Top/Work/WorkTitle)
  - `pattern/` 4종 (transaction, excel, FileUpTransfer, largeData)
  - `sample/` 13종 (Calendar, Grid, Message, Popup, Script, FileUpDownloadTrans, streaming video, bulk columns, …)
  - `cmm/cmmAlert.xfdl`, `cmm/cmmConfirm.xfdl`, `lib/cmmInclude.xjs`, `debugging/`, `images/`
- **`typedefinition.xml` Services 블록 2-tier 재구성**
  - Core 9 (nexacroN v24 표준 고정 레이아웃): `theme` / `initvalue` / `imagerc` / `font` / `extPrototype` / `lib` / `frame` / `xcssrc` / `images`
  - Scaffold 보조 4: `svcurl` → `{{BACKEND_URL}}` (플러그인 토큰 치환), `cmm` / `sample` / `pattern` (form 폴더 마운트)
- **`nxui/README.md`** — services contract 표, runner family 별 build output 경로, nexacrolib 동봉 근거 문서화
- **`docs/releases/v1.8.1.md`** — 릴리스 노트

### Changed
- **`plugins/nexacro-fullstack-starter/.../SKILL.md`** — `Step 6 — nexacro 빌드 / Nexacro build` 신규 단계 삽입
  - Runner family 별 build output 경로 자동 매핑 (`boot-*` / `webflux-*` → `src/main/resources/static/packageN/`; `mvc-*` / `egov*-mvc-*` → `src/main/webapp/packageN/`)
  - `/nexacro-build` user skill 자동 연계 (`Skill(skill: "nexacro-build", args: ...)`)
  - `/nexacro-build` 미설치 시 `nexacrodeploy.exe` CLI 복붙 안내로 우아하게 폴백
  - Windows 전용 주의사항 문서화
  - 기존 Step 6 (Final guidance) → **Step 7** 로 승격, 새 build path 를 next-steps 리스트에 노출
- **`.gitignore` (monorepo)** — `$Geninfo$.geninfo`, `*.geninfo` (nexacro IDE 캐시) 추가

### Deferred to v1.8.2
- `core/` 모듈 import (xapi/xeni/uiadapter × {jakarta, javax}) — 조사 결과 현재 러너가 `shared-business-*` 트리 안에 nexacro envelope / uiadapter surface 를 inline 으로 이미 보유 (`com.nexacro.fullstack.business.xapi.*`, `com.nexacro.fullstack.business.uiadapter.*`). 외부 jar 로 전환하는 작업은 소스 교체 성격이므로 별도 minor 로 분리.
- 14-endpoint 컨트롤러 계약 정렬 — 백킹 서비스/DAO/MyBatis XML/HSQL seed 확장이 필요하여 패치 릴리스 범위 초과.

## [1.8.0] - 2026-04-23

### Added
- **신규 플러그인 `nexacro-fullstack-starter`** (v0.1.0) — Nexacro N v24 풀스택 프로젝트 스캐폴드
  - `jdk × framework` 매트릭스에서 8개 runner 중 하나를 선택하여 `nexacroN-fullstack` 모노레포로부터 sparse-clone
  - 8 runners: `boot-jdk17-jakarta` (기본) / `boot-jdk8-javax` / `mvc-jdk17-jakarta` / `mvc-jdk8-javax` / `egov5-boot-jdk17-jakarta` / `egov4-boot-jdk8-javax` / `egov4-mvc-jdk8-javax` / `webflux-jdk17-jakarta`
  - 도출 규칙: `servletApi = jdk>=17 ? jakarta : javax`, `springMajor = jakarta ? 6 : 5`, `bootMajor = jakarta ? 3 : 2`
  - 거부 조합 (fail-fast + 대안 제시): `egov-mvc + jdk17`, `webflux + jdk8`
  - 토큰 치환: `{{PROJECT_NAME}}` / `{{BACKEND_URL}}` / `{{CONTEXT_PATH}}` / `{{SERVER_PORT}}`
  - 5 business tree (`shared-business/{jdk8-javax,jdk17-jakarta}`, `shared-business-egov4/jdk8-javax`, `shared-business-egov5/jdk17-jakarta`, `shared-business-reactive/jdk17-mybatis`)
  - 15개 API endpoint (공통 14 + webflux 전용 `exim_exchange` 스트리밍 데모 1)
  - HSQL 인메모리 seed data (USERS / SAMPLE_BOARD / DEPT / LARGE_DATA / WIDE_COLUMNS / FILE_META)
- `plugins/nexacro-fullstack-starter/.claude-plugin/plugin.json` (v0.1.0)
- `plugins/nexacro-fullstack-starter/skills/nexacro-fullstack-starter/SKILL.md` — 6-step 플로우 (파라미터 → 호환성 검사 → sparse clone → 토큰 치환 → 후처리 → 사용자 가이드)
- `assets/matrix.json` — 143 라인 매트릭스 정의 (8 runners + rejected combinations + derivation rules + tokens)
- 레퍼런스 4종: `compatibility-matrix.md`, `repo-map.md`, `runner-selection-guide.md`, `troubleshooting.md`
- 신규 GitHub 저장소 [`JasonMMo/nexacroN-fullstack`](https://github.com/JasonMMo/nexacroN-fullstack) — 플러그인이 sparse-clone 하는 모노레포 (MIT)

### Changed
- `.claude-plugin/marketplace.json`: 2개 → 3개 플러그인 등록
- `README.md` / `README-ko.md`: `three plugins` / `3개 플러그인` 으로 업데이트, 설치 명령 + 플러그인 ③ 섹션 + 프로젝트 구조 트리 확장

## [1.7.0] - 2026-04-22

### Added
- `nexacro-project-maker` skill 에 **프레임 스타일 옵션** 도입 (`FRAME_STYLE` 파라미터)
  - `minimal` (기본값) — 기존 단일 `ChildFrame` 스캐폴드 (7 파일)
  - `packageN` — MDI / 프레임셋 풀레이아웃 스캐폴드 (15 파일)
    - `VFrameSet[44,0,*,0]` → `HFrameSet[240,*]` → `VFrameSet1[32,*,0]` 트리
    - 프레임 xfdl 8종: `frameTop` / `frameLogin` / `frameLeft` / `frameMDI` / `frameMain` / `frameBottom` / `frameWork` / `frameWorkTitle`
    - `nexacron/uiadapter-jakarta/packageN` 공식 샘플 기반
- `assets/skeleton-frames/packageN/` 신규 번들 (11 파일)
  - `{{PROJECT_NAME}}.xadl` — VFrameSet + HFrameSet MDI 레이아웃 (tokenized)
  - `typedefinition.xml` — `frame::` 서비스 prefix + extPrototype/ListView/traceLog 모듈 포함
  - `appvariables.xml` — packageN 공식 전역변수 세트 (메뉴/세션)
  - `frame/*.xfdl` 8 파일 (as-is 복사)
- `references/xadl-frame-patterns.md` 신규 레퍼런스 — Frame Tree 개념 / minimal vs packageN 비교 / 커스터마이징 팁

### Changed
- `nexacro-project-maker/SKILL.md`
  - Step 1 파라미터 #6 (`FRAME_STYLE`) 추가
  - Step 2 치환 로직 분기 (minimal / packageN)
  - Step 3 검증 출력 스타일별 분리
- `references/service-prefixes.md` 에 `frame::` 엔트리 추가

## [1.6.0] - 2026-04-22

### Changed
- **BREAKING (skill rename)**: Nexacro 도메인 용어(Form = 화면 단위)에 맞춰 2개 skill 이름 변경
  - `nexacro-xfdl-author` → `nexacro-form-maker`
  - `nexacro-project-init` → `nexacro-project-maker`
- `SKILL.md` frontmatter 의 `name` / 트리거 문구 업데이트
- 디렉터리 `git mv` 로 rename (히스토리 보존)
- 교차 참조 업데이트: `typedefinition-spec.md`, `nexacro-webflux-port/SKILL.md`, README / README-ko

### Migration
- 사용자는 `/plugin install nexacro-claude-skills@nexacro-claude-skills` 재설치 후 새 이름으로 호출
- 기존 이름(`nexacro-xfdl-author` / `nexacro-project-init`) 은 더 이상 존재하지 않음

## [1.5.0] - 2026-04-22

### Added
- `nexacro-xfdl-author` skill 확장 (v1 코어 13 → v2 총 43종 컴포넌트)
  - **모던 입력 + 선택 확장** (6): `textfield`, `multilinetextfield`, `spin`, `listbox`, `checkboxset`, `multicombo`
  - **날짜 확장 + 내비게이션** (8): `daterangepicker`, `popupdaterangepicker`, `tab`, `groupbox`, `menu`, `popupmenu`, `popupdiv`, `panel`
  - **디스플레이 + 파일 I/O** (9): `imageviewer`, `progressbar`, `listview`, `virtualfile`, `filedialog`, `filedownload`, `fileupload`, `filedowntransfer`, `fileuptransfer`
  - **미디어 / 플러그인 / 데이터** (7): `plugin`, `webbrowser`, `sketch`, `googlemap`, `videoplayer`, `graphics`, `dataobject`
- `nexacro-xfdl-author/SKILL.md` 외부 공식 참고자료 섹션 추가 (공개 샘플 / 온라인 도움말 / 워크북)

### Changed
- `nexacro-xfdl-author/SKILL.md` 컴포넌트 카탈로그 재구조 (코어 13 / 확장 30 2-섹션 분리)
- 일부 확장 컴포넌트(`Sketch` / `Graphics` / `Plugin` 등)는 공식 샘플 부재로 최소 레퍼런스만 제공하며 공식 문서 링크로 대체

## [1.4.0] - 2026-04-22

### Added
- `nexacro-project-init` skill (nexacro-claude-skills 번들)
  - SKILL.md — 7-파일 스캐폴드 플로우, 파라미터 수집 / 치환 / 검증 단계
  - `assets/skeleton/` — `{{PROJECT_NAME}}.xprj`, `{{PROJECT_NAME}}.xadl`, `typedefinition.xml`, `environment.xml`, `appvariables.xml`, `bootstrap.xml`, `Base/main.xfdl` 파라미터화 템플릿
  - `references/xprj-spec.md` — `.xprj` 엔트리 엘리먼트 레퍼런스
  - `references/xadl-spec.md` — Application / MainFrame / ChildFrame 속성 + 다국어 screenid
  - `references/typedefinition-spec.md` — Modules / Components / Services 3-섹션 구조
  - `references/service-prefixes.md` — `Base::` / `imagerc::` / `theme::` 등 prefix 매핑 규칙
- `nexacro-xfdl-author` skill (nexacro-claude-skills 번들)
  - SKILL.md — Form 골격 + 13종 코어 컴포넌트 + Dataset 바인딩 플로우
  - `assets/form-skeleton.xfdl` — 재사용 가능한 빈 Form 템플릿
  - `references/form-structure.md` — `<Form>` / `<Layouts>` / `<Objects>` / `<Script>` 4-섹션 상세
  - `references/binding-patterns.md` — BindItem / innerdataset / binddataset 3-패턴 비교
  - `references/components/*.md` — 13개 컴포넌트 블록 (button, edit, maskedit, textarea, combo, radio, checkbox, calendar, datefield, static, div, grid, dataset)
- README.md / README-ko.md 에 2개 신규 skill 섹션 추가 (planned → available)

### Changed
- `nexacro-claude-skills` plugin.json: version 1.0.0 → 1.4.0, description / keywords 확장

## [1.3.0] - 2026-04-22

### Added
- `nexacro-data-format` skill (nexacro-claude-skills 번들에 추가)
  - SKILL.md — XML/SSV/JSON 포맷 개요, `_RowType_` (`N`/`I`/`U`/`D`/`O`) 공통 의미 표, 포맷 선택 가이드
  - `references/xml-format.md` — 전체 샘플 + 엘리먼트/타입/`_RowType_` 속성 레퍼런스
  - `references/ssv-format.md` — 구분자(`▼`/`•`/`:`/`,`) 해설 + Dataset 2개 샘플 + 파싱 주의점
  - `references/json-format.md` — 필드 레퍼런스 + trailing 콤마 이슈 + WebFlux 파싱 팁
- README.md / README-ko.md 에 `nexacro-data-format` 섹션 추가 (planned → available)

## [1.2.0] - 2026-04-22

### Changed
- **BREAKING (repo layout)**: 저장소를 Claude Code 공식 플러그인 마켓플레이스 포맷으로 재구성
  - 루트에 `.claude-plugin/marketplace.json` 카탈로그 추가 (2개 플러그인 게시)
  - `skills/*` → `plugins/<plugin-name>/skills/*` 로 이동 (git history 보존)
  - 비표준 `.claude/plugin.json` 제거
- 플러그인 분리 구조:
  - `nexacro-claude-skills` — 범용 유틸리티 번들 (현재 `nexacro-build` 포함, `nexacro-data-format` / `nexacro-xfdl-author` 예정)
  - `nexacro-webflux-port` — WebFlux 포팅 전용 독립 플러그인 (SKILL.md + 8 references)
- 설치 명령 변경:
  - (이전) 수동 clone / 비공식 manifest
  - (신규) `/plugin marketplace add JasonMMo/nexacro-claude-skills` 후
    - `/plugin install nexacro-claude-skills@nexacro-claude-skills`
    - `/plugin install nexacro-webflux-port@nexacro-claude-skills`
- README.md / README-ko.md 전면 재작성 (2-플러그인 마켓플레이스 프레젠테이션)
- `.gitignore` 정리 (`.claude/plugin.json` 예외 규칙 제거, `.obsidian/` / `.tmp.*` 추가)

### Added
- `plugins/nexacro-claude-skills/.claude-plugin/plugin.json` 생성
- `plugins/nexacro-webflux-port/.claude-plugin/plugin.json` 생성

### Removed
- `.claude/plugin.json` (비공식 포맷)

## [1.1.0] - 2026-04-22

### Added
- `nexacro-webflux-port` skill — Spring Boot/MVC → Spring WebFlux 포팅 플레이북
  - Phase A~E 체크리스트 (모듈 골격 / xapi / uiadapter / xeni / 샘플 앱)
  - 8개 references 문서:
    - `classpath-shim.md` — maven-dependency-plugin unpack + excludes 패턴
    - `servlet-provider-shim.md` — ServletProvider 요청 스코프 shim 계약
    - `multipart-import-by-type.md` — FilePart/FormFieldPart 타입 기반 분기
    - `getparameter-equivalence.md` — paramOf() 헬퍼 (query + form 머지)
    - `stub-shim-with-limitations.md` — UnsupportedOperationException + LIMITATION Javadoc
    - `webfilter-content-type-bypass.md` — multipart/form-urlencoded bypass
    - `result-handler-ordering.md` — ORDER + supports() 상호배제
    - `basepath-and-static-resources.md` — contextPath + ResourceHandlerRegistry
- plugin.json 에 `nexacro-webflux-port` skill 등록
- README.md / README-ko.md 에 신규 skill 섹션 추가

## [1.0.0] - 2024-03-24

### Added
- nexacro-build skill for automating XFDL source build and deployment
- Standardized project structure for GitHub deployment
- Comprehensive documentation and contribution guidelines
- Test framework setup
- GitHub workflow configuration

### Changed
- Initial release preparation

### Deprecated
- Nothing

### Removed
- Nothing

### Fixed
- Nothing

### Security
- Nothing