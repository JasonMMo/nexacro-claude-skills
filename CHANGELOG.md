# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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