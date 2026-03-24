# Nexacro Build - Basic Usage Examples

## Overview

This document provides basic usage examples for the nexacro-build skill.

## Common Commands

### 1. Build Commands

```bash
# Korean commands
nexacro 빌드
xfdl �일드
넥사크로 빌드
generate 해줘
deploy 해줘

# English commands
nexacro build
xfdl build
nexacrodeploy run
generate
deploy
```

### 2. Project Types

#### Nexacro Project
```bash
"nexacro 프로젝트 빌드해줘"
"Nexacro 프로젝트를 deploy 해줘"
```

#### XFDL Files
```bash
"xfdl 소스 파일을 generate 해줘"
"XFDL 파일을 빌드해줘"
```

### 3. Deployment Options

#### Using nexacrodeploy.exe
```bash
"nexacrodeploy.exe 실행해줘"
"Windows 환경에서 nexacrodeploy 실행"
```

#### Using Java Deploy
```bash
"Java 기반 Nexacro Deploy 실행 (start.bat)"
"start.sh 스크립트로 배포"
```

## Real-world Examples

### Example 1: Daily Build Process
```bash
"매일 아침 9시에 nexacro 프로젝트 자동 빌드 실행"
"주간 배포를 위한 xfdl 파일 생성"
```

### Example 2: Emergency Deployment
```bash
"긴급 배포가 필요해, nexacrodeploy 실행해줘"
"생산 환경에 바로 배포해"
```

### Example 3: Batch Processing
```bash
"여러 개의 nexacro 프로젝트를 순서대로 빌드해줘"
"batch 모드로 xfdl 파일 생성"
```

## Tips

1. **Timing**: The skill automatically detects the appropriate build method based on your environment
2. **Language**: Supports both Korean and English commands seamlessly
3. **Environment**: Works with both Windows (nexacrodeploy.exe) and Java-based deployments
4. **Error Handling**: Provides clear error messages if build fails

## Troubleshooting

If the skill doesn't work:
1. Check if you're in the correct project directory
2. Verify nexacrodeploy.exe or Java is installed
3. Ensure proper permissions for build operations