# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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