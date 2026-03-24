# Nexacro Claude Skills API Documentation

## Overview

This document provides API documentation for all available Claude Code skills in the nexacro-claude-skills package.

## Skills List

### nexacro-build

#### Description
Automates Nexacro XFDL source build and deployment operations.

#### Triggers
- "nexacro 빌드"
- "xfdl 빌드"
- "nexacrodeploy 실행"
- "generate 해줘"
- "deploy 해줘"
- "넥사크로 빌드"

#### Implementation
- Located in: `skills/nexacro-build/`
- Type: Skill automation
- Dependencies: None

#### Usage Examples
```javascript
// The skill is automatically triggered by natural language commands
// No direct API call needed
```

## Skill Development Guidelines

### Creating New Skills

1. **Directory Structure**
   ```
   skills/[skill-name]/
   ├── index.js      # Main implementation
   ├── README.md     # Documentation
   ├── test.js       # Tests
   └── package.json  # Metadata (optional)
   ```

2. **Skill Requirements**
   - Follow conventional commit messages
   - Include comprehensive error handling
   - Maintain 80%+ test coverage
   - Document all parameters and return values

3. **Naming Conventions**
   - Use kebab-case for skill names
   - Keep names descriptive and concise
   - Include nexacro prefix where appropriate

### Testing

All skills should include:
- Unit tests for core functionality
- Integration tests for real-world scenarios
- Error condition testing
- Performance benchmarks where relevant

### Documentation

Each skill must include:
- Clear description of purpose
- Usage examples
- Parameter documentation
- Error handling information
- Troubleshooting guide

## Error Handling Standards

### Error Categories
1. **Validation Errors** - Invalid parameters or configuration
2. **Runtime Errors** - External service failures
3. **System Errors** - Infrastructure or dependency issues

### Error Response Format
```javascript
{
  error: true,
  message: "Human-readable error message",
  code: "ERROR_CODE",
  details: {}
}
```

### Common Error Codes
- `INVALID_PARAMS` - Invalid or missing parameters
- `SERVICE_UNAVAILABLE` - External service down
- `PERMISSION_DENIED` - Authorization failure
- `TIMEOUT` - Operation timed out
- `FILE_NOT_FOUND` - Required file missing

## Performance Guidelines

- Skills should complete within 30 seconds
- Use appropriate timeouts for external calls
- Implement caching where beneficial
- Monitor and log performance metrics