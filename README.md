# Nexacro Claude Skills

This repository contains Claude Code skills specifically designed for Nexacro platform development.

## 📦 설치 방법

### 방법 1: 레포 전체를 플러그인으로 등록
```bash
/plugin marketplace add JasonMMo/nexacro-claude-skills
```

### 방법 2: 특정 스킬만 설치
```bash
/plugin install nexacro-build@JasonMMo/nexacro-claude-skills
```

### 방법 3: 직접 Clone 방식
```bash
git clone https://github.com/JasonMMo/nexacro-claude-skills.git
cp -r nexacro-claude-skills/skills/nexacro-build ~/.claude/skills/
```

### 요구사항

- **Node.js**: >= 16.0.0
- **Claude Code**: >= 1.0.0
- **Nexacro Platform**: 시스템에 설치
- **Java Runtime**: Java 기반 배포 시 필요 (선택 사항)

### Installation

1. **Install from Marketplace**:
   ```bash
   claude plugin install nexacro-claude-skills
   ```

2. **Manual Installation**:
   ```bash
   npm install -g nexacro-claude-skills
   ```

3. **Verify Installation**:
   ```bash
   claude plugin list | grep nexacro-claude-skills
   ```

## 📁 Project Structure

```
nexacro-claude-skills/
├── .claude/                # Plugin configuration
│   └── plugin.json        # Plugin manifest for marketplace
├── .github/                 # GitHub workflow configuration
│   └── workflows/
│       └── publish.yml     # Automated publishing workflow
├── skills/                 # Existing skills directory
│   └── nexacro-build/     # Main skill implementation
├── docs/                   # Documentation
│   ├── skills/             # Individual skill documentation
│   └── API.md              # API reference
├── examples/               # Usage examples
│   ├── basic-usage/        # Basic skill usage examples
│   └── advanced/           # Advanced use cases
├── tests/                  # Test files
│   └── skills/             # Skill tests
├── package.json            # Project dependencies
├── .npmrc                  # npm configuration
├── .gitignore              # Git ignore rules
├── CHANGELOG.md            # Version history
└── CONTRIBUTING.md         # Contribution guidelines
```

## 🚀 Quick Start

1. Choose one of the installation methods above
2. Use natural language commands:
   - "nexacro 빌드해줘"
   - "xfdl 파일 generate 해줘"
   - "nexacrodeploy 실행해줘"
3. Run tests: `npm test`
4. Publish: `npm publish`

## 📋 Available Skills

### nexacro-build
- **Description**: Automates Nexacro XFDL source build and deployment operations
- **Triggers**: nexacro 빌드, xfdl 빌드, nexacrodeploy 실행, generate 해줘, deploy 해줘, 넥사크로 빌드
- **Features**:
  - Supports both nexacrodeploy.exe and Java-based deployments
  - Handles Korean and English commands
  - Automated build and deployment workflows

### nexacro-webflux-port
- **Description**: End-to-end playbook for porting Spring Boot / Spring MVC Nexacro modules (xapi / xeni / uiadapter) to Spring WebFlux
- **Triggers**: webflux 전환, reactive 로 바꿔, 서블릿 제거, nexacro webflux, xapi 포팅, xeni 포팅, uiadapter 포팅, HttpServletRequest 제거
- **Features**:
  - Phase-by-phase checklist (module skeleton → xapi → uiadapter → xeni → sample app)
  - 8 reference docs covering classpath shim, ServletProvider, multipart by type, paramOf equivalence, WebFilter content-type bypass, ResultHandler ordering, stub shim with LIMITATION, base-path and static resources
  - `jdeps | grep jakarta.servlet` = 0 CI gate pattern
  - Traps and regressions table (multipart 500 error, ReadOnlyHttpHeaders.set, filenamelist null, POI NoClassDefFoundError, base-path 404)

## 🔧 Configuration

The plugin automatically detects your environment:
- **Windows**: Uses nexacrodeploy.exe
- **Linux/macOS**: Uses Java-based Nexacro Deploy
- **Language**: Supports both Korean and English commands

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - see LICENSE file for details