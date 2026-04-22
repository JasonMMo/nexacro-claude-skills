# 넥사크로 Claude Skills

이 저장소는 Nexacro 개발용 스킬을 배포하는 **Claude Code 플러그인 마켓플레이스** 입니다.

현재 **2개 플러그인** 을 게시합니다:

| 플러그인 | 용도 |
|---|---|
| `nexacro-claude-skills` | 범용 Nexacro 유틸리티 번들 (xfdl 빌드/배포, 데이터 포맷 레퍼런스, xfdl 작성 헬퍼) |
| `nexacro-webflux-port` | Spring Boot/MVC 기반 Nexacro 모듈을 Spring WebFlux 로 포팅하는 독립 플레이북 |

## 📦 설치 방법

### 1. 마켓플레이스 등록 (최초 1회)
```bash
/plugin marketplace add JasonMMo/nexacro-claude-skills
```

### 2. 필요한 플러그인 설치
```bash
# 범용 유틸리티 (build + data-format + xfdl-author)
/plugin install nexacro-claude-skills@nexacro-claude-skills

# Spring WebFlux 포팅 플레이북
/plugin install nexacro-webflux-port@nexacro-claude-skills
```

> 문법은 `<plugin-name>@<marketplace-name>` 입니다. 범용 유틸리티 플러그인과 마켓플레이스의 이름이 모두 `nexacro-claude-skills` 로 동일합니다.

### 3. 설치 확인
```bash
/plugin list
```

### 직접 Clone 방식
```bash
git clone https://github.com/JasonMMo/nexacro-claude-skills.git
# 원하는 플러그인을 Claude Code plugin 디렉터리에 복사
cp -r nexacro-claude-skills/plugins/nexacro-webflux-port ~/.claude/plugins/
```

### 요구사항
- **Claude Code**: >= 2.0
- **넥사크로 플랫폼**: 개발자 머신에 설치 (nexacro-build 사용 시)
- **Java 런타임**: Java 기반 배포 사용 시 필요 (선택 사항)

## 📁 프로젝트 구조

```
nexacro-claude-skills/
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그 (2개 플러그인)
├── plugins/
│   ├── nexacro-claude-skills/        # 플러그인 ① 유틸리티 번들
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       ├── nexacro-build/        # xfdl 빌드/배포 자동화
│   │       ├── nexacro-data-format/  # XML / SSV / JSON 레퍼런스
│   │       └── nexacro-xfdl-author/  # xfdl 작성 헬퍼              (예정)
│   └── nexacro-webflux-port/         # 플러그인 ② WebFlux 포팅 플레이북
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── nexacro-webflux-port/
│               ├── SKILL.md
│               └── references/       # 8개 상세 레퍼런스 문서
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## 📋 사용 가능한 스킬

### 플러그인 ① — `nexacro-claude-skills`

#### nexacro-build
- **설명**: 넥사크로 XFDL 소스 빌드 및 배포 작업을 자동화합니다
- **트리거**: nexacro 빌드, xfdl 빌드, nexacrodeploy 실행, generate 해줘, deploy 해줘, 넥사크로 빌드
- **기능**:
  - `nexacrodeploy.exe` (Windows) 및 Java 기반 배포(`start.bat`/`start.sh`) 모두 지원
  - 한국어 / 영어 명령어 지원
  - `build-config.json` 에 설정 영속화 — 재실행 시 재입력 불필요

#### nexacro-data-format
- **설명**: Nexacro 클라이언트 ↔ 서버 통신 데이터 포맷(XML / SSV / JSON)의 공식 샘플과 `_RowType_` 의미 참조
- **트리거**: nexacro 포맷, SSV 포맷, Dataset XML, nexacro JSON, `_RowType_`, ConstColumn, nexacro 응답 파싱
- **기능**:
  - 세 포맷(XML / SSV / JSON) 의 공식 전체 샘플 제공
  - `_RowType_` (`N` / `I` / `U` / `D` / `O`) 상태 플래그 용어집과 서버 INSERT/UPDATE/DELETE 분기 규칙
  - SSV 구분자 레퍼런스 (`▼` 레코드 · `•` 필드 · `:` 메타 · `,` 나열)
  - 포맷 선택 가이드 (전송 효율 vs 디버깅 편의 트레이드오프)

> `nexacro-xfdl-author` 스킬은 추후 같은 플러그인에 별도 커밋으로 추가됩니다.

### 플러그인 ② — `nexacro-webflux-port`

#### nexacro-webflux-port
- **설명**: Spring Boot / Spring MVC 기반 Nexacro 모듈(xapi / xeni / uiadapter)을 Spring WebFlux 로 포팅하는 전체 플레이북
- **트리거**: webflux 전환, reactive 로 바꿔, 서블릿 제거, nexacro webflux, xapi 포팅, xeni 포팅, uiadapter 포팅, HttpServletRequest 제거
- **기능**:
  - Phase 별 체크리스트 (모듈 골격 → xapi → uiadapter → xeni → 샘플 앱)
  - 8개 레퍼런스 문서: classpath shim, ServletProvider, 타입 기반 multipart 분기, paramOf 동치, WebFilter content-type bypass, ResultHandler 순서, stub shim + LIMITATION, base-path + 정적 리소스
  - `jdeps | grep jakarta.servlet` = 0 CI 게이트 패턴
  - 회귀 표 (multipart 500, ReadOnlyHttpHeaders.set, filenamelist null, POI NoClassDefFoundError, base-path 404)

## 🔧 런타임 자동 감지

`nexacro-build` 스킬은 OS 에 따라 자동 분기:
- **Windows** → `nexacrodeploy.exe` 사용
- **Linux / macOS** → Java 기반 Nexacro Deploy 사용
- **언어** → 한국어 / 영어 명령 모두 지원

## 🤝 기여

기여 가이드는 [CONTRIBUTING.md](./CONTRIBUTING.md) 참고.

## 📄 라이선스

MIT 라이선스 — [LICENSE](./LICENSE) 참고.
