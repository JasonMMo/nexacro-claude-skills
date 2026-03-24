# Nexacro Claude Skills

This repository contains Claude Code skills specifically designed for Nexacro platform development.

## 📦 Plugin Marketplace

This plugin is available on the Claude Code Plugin Marketplace. You can install it using:

```bash
claude plugin install nexacro-claude-skills
```

### Requirements

- **Node.js**: >= 16.0.0
- **Claude Code**: >= 1.0.0
- **Nexacro Platform**: Installed on your system
- **Java Runtime**: For Java-based deployments (optional)

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

1. Install the plugin using the commands above
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

## 🔧 Configuration

The plugin automatically detects your environment:
- **Windows**: Uses nexacrodeploy.exe
- **Linux/macOS**: Uses Java-based Nexacro Deploy
- **Language**: Supports both Korean and English commands

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - see LICENSE file for details