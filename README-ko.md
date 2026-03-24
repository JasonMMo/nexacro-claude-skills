# 넥사크로 Claude 스킬

이 저장소는 넥사크로 플랫폼 개발을 위해 특별히 제작된 Claude Code 스킬들을 포함하고 있습니다.

## 📦 플러그인 마켓플레이스

이 플러그인은 Claude Code 플러그인 마켓플레이스에서 사용 가능합니다. 다음 명령으로 설치할 수 있습니다:

```bash
claude plugin install nexacro-claude-skills
```

### 요구사항

- **Node.js**: >= 16.0.0
- **Claude Code**: >= 1.0.0
- **넥사크로 플랫폼**: 시스템에 설치
- **Java 런타임**: Java 기반 배포 시 필요 (선택 사항)

### 설치 방법

1. **마켓플레이스에서 설치**:
   ```bash
   claude plugin install nexacro-claude-skills
   ```

2. **수동 설치**:
   ```bash
   npm install -g nexacro-claude-skills
   ```

3. **설치 확인**:
   ```bash
   claude plugin list | grep nexacro-claude-skills
   ```

## 📁 프로젝트 구조

```
nexacro-claude-skills/
├── .claude/                # 플러그인 설정
│   └── plugin.json        # 마켓플레이스용 플러그인 매니페스트
├── .github/                 # GitHub 워크플로우 설정
│   └── workflows/
│       └── publish.yml     # 자동 배포 워크플로우
├── skills/                 # 기존 스킬 디렉토리
│   └── nexacro-build/     # 메인 스킬 구현
├── docs/                   # 문서
│   ├── skills/             # 개별 스킬 문서
│   └── API.md              # API 레퍼런스
├── examples/               # 사용 예제
│   ├── basic-usage/        # 기본 스킬 사용법
│   └── advanced/           # 고급 사용 사례
├── tests/                  # 테스트 파일
│   └── skills/             # 스킬 테스트
├── package.json            # 프로젝트 의존성
├── .npmrc                  # npm 설정
├── .gitignore              # Git 무시 파일
├── CHANGELOG.md            # 버전 히스토리
└── CONTRIBUTING.md         # 기여 가이드라인
```

## 🚀 빠른 시작

1. 위 명령으로 플러그인 설치
2. 자연어 명령 사용:
   - "nexacro 빌드해줘"
   - "xfdl 파일 generate 해줘"
   - "nexacrodeploy 실행해줘"
3. 테스트 실행: `npm test`
4. 배포: `npm publish`

## 📋 사용 가능한 스킬

### nexacro-build
- **설명**: 넥사크로 XFDL 소스 빌드 및 배포 작업을 자동화합니다
- **트리거**: nexacro 빌드, xfdl 빌드, nexacrodeploy 실행, generate 해줘, deploy 해줘, 넥사크로 빌드
- **기능**:
  - nexacrodeploy.exe 및 Java 기반 배포 지원
  - 한국어 및 영어 명령어 지원
  - 자동화된 빌드 및 배포 워크플로우

## 🔧 설정

플러그인이 환경을 자동으로 감지합니다:
- **Windows**: nexacrodeploy.exe 사용
- **Linux/macOS**: Java 기반 넥사크로 배포 사용
- **언어**: 한국어 및 영어 명령어 지원

## 🤝 기여

기여 가이드는 [CONTRIBUTING.md](./CONTRIBUTING.md)를 참고해 주세요.

## 📄 라이선스

MIT 라이선스 - LICENSE 파일에서 상세 정보 확인