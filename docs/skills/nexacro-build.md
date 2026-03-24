# Nexacro Build Skill

## Description

The `nexacro-build` skill automates Nexacro XFDL source build and deployment operations. It supports both nexacrodeploy.exe and Java-based Nexacro Deploy operations.

## Usage

```bash
nexacro 빌드
xfdl 빌드
nexacrodeploy 실행
generate 해줘
deploy 해줘
넥사크로 빌드
```

## Parameters

This skill is triggered by natural language commands and does not require specific parameters.

## Features

- Supports nexacrodeploy.exe execution
- Supports Java-based Nexacro Deploy (start.bat/start.sh)
- Automates build and deployment workflows
- Handles both Korean and English commands

## Error Handling

- Validates project structure before build
- Checks for required dependencies
- Provides clear error messages for failed operations
- Handles timeout scenarios

## Examples

```bash
# Basic build command
"nexacro 빌드해줘"

# Generate XFDL files
"xfdl 파일 generate 해줘"

# Deploy to server
"nexacrodeploy 실행해줘"
```