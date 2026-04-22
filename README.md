# Nexacro Claude Skills

This repository is a **Claude Code plugin marketplace** that distributes skills for Nexacro platform development.

It currently publishes **two plugins**:

| Plugin | Purpose |
|---|---|
| `nexacro-claude-skills` | General-purpose Nexacro utility bundle (xfdl build/deploy, data format reference, xfdl authoring) |
| `nexacro-webflux-port` | Standalone playbook for porting Spring Boot/MVC Nexacro modules to Spring WebFlux |

## 📦 Installation

### 1. Register the marketplace once
```bash
/plugin marketplace add JasonMMo/nexacro-claude-skills
```

### 2. Install the plugin(s) you need
```bash
# general-purpose utilities (build + data-format + xfdl-author)
/plugin install nexacro-claude-skills@nexacro-claude-skills

# Spring WebFlux porting playbook
/plugin install nexacro-webflux-port@nexacro-claude-skills
```

> The syntax is `<plugin-name>@<marketplace-name>`. Both the marketplace and its general-purpose plugin share the name `nexacro-claude-skills`.

### 3. Verify
```bash
/plugin list
```

### Manual installation (clone)
```bash
git clone https://github.com/JasonMMo/nexacro-claude-skills.git
# Copy the plugin of your choice into Claude Code's plugin directory
cp -r nexacro-claude-skills/plugins/nexacro-webflux-port ~/.claude/plugins/
```

### Requirements
- **Claude Code**: >= 2.0
- **Nexacro Platform**: installed on the developer machine (for `nexacro-build`)
- **Java Runtime**: required if using Java-based Nexacro Deploy (optional)

## 📁 Project Structure

```
nexacro-claude-skills/
├── .claude-plugin/
│   └── marketplace.json              # marketplace catalog (2 plugins)
├── plugins/
│   ├── nexacro-claude-skills/        # plugin ①: utility bundle
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       ├── nexacro-build/        # xfdl build/deploy automation
│   │       ├── nexacro-data-format/  # XML / SSV / JSON reference
│   │       └── nexacro-xfdl-author/  # xfdl authoring helper       (planned)
│   └── nexacro-webflux-port/         # plugin ②: WebFlux porting playbook
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── nexacro-webflux-port/
│               ├── SKILL.md
│               └── references/       # 8 detailed reference docs
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## 📋 Available Skills

### Plugin ① — `nexacro-claude-skills`

#### nexacro-build
- **Description**: Automates Nexacro XFDL source build and deployment operations
- **Triggers**: nexacro 빌드, xfdl 빌드, nexacrodeploy 실행, generate 해줘, deploy 해줘, 넥사크로 빌드
- **Features**:
  - Supports both `nexacrodeploy.exe` (Windows) and Java-based Deploy (`start.bat`/`start.sh`)
  - Handles Korean and English commands
  - Persists `build-config.json` across sessions for zero-friction rebuilds

#### nexacro-data-format
- **Description**: Reference for Nexacro client-server data formats (XML / SSV / JSON) with official samples and `_RowType_` semantics
- **Triggers**: nexacro 포맷, SSV 포맷, Dataset XML, nexacro JSON, `_RowType_`, ConstColumn, nexacro 응답 파싱
- **Features**:
  - Full official samples for all 3 formats (XML / SSV / JSON)
  - `_RowType_` (`N` / `I` / `U` / `D` / `O`) state-flag glossary with server-side INSERT/UPDATE/DELETE dispatch rules
  - SSV delimiter reference (`▼` record, `•` field, `:` meta, `,` list)
  - Format-selection guide (throughput vs debuggability trade-offs)

> `nexacro-xfdl-author` skill is planned and will be added to this plugin as a separate commit.

### Plugin ② — `nexacro-webflux-port`

#### nexacro-webflux-port
- **Description**: End-to-end playbook for porting Spring Boot / Spring MVC Nexacro modules (xapi / xeni / uiadapter) to Spring WebFlux
- **Triggers**: webflux 전환, reactive 로 바꿔, 서블릿 제거, nexacro webflux, xapi 포팅, xeni 포팅, uiadapter 포팅, HttpServletRequest 제거
- **Features**:
  - Phase-by-phase checklist (module skeleton → xapi → uiadapter → xeni → sample app)
  - 8 reference docs: classpath shim, ServletProvider, multipart by type, paramOf equivalence, WebFilter content-type bypass, ResultHandler ordering, stub shim with LIMITATION, base-path and static resources
  - `jdeps | grep jakarta.servlet` = 0 CI gate pattern
  - Traps and regressions table (multipart 500, ReadOnlyHttpHeaders.set, filenamelist null, POI NoClassDefFoundError, base-path 404)

## 🔧 Runtime Detection

The `nexacro-build` skill auto-adapts to your environment:
- **Windows** → uses `nexacrodeploy.exe`
- **Linux / macOS** → uses Java-based Nexacro Deploy
- **Language** → Korean and English commands both work

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License — see [LICENSE](./LICENSE).
