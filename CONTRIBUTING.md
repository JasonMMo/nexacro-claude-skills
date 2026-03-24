# Contributing to Nexacro Claude Skills

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the nexacro-claude-skills repository.

## 📝 Code of Conduct

This project follows a standard Code of Conduct. Please ensure all interactions are professional and respectful.

## 🚀 Development Workflow

### 1. Fork the Repository

- Fork the repository on GitHub
- Clone your fork locally
- Create a feature branch: `git checkout -b feature/new-skill`

### 2. Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/your-username/nexacro-claude-skills.git
cd nexacro-claude-skills

# Install dependencies
npm install

# Run initial tests
npm test
```

### 3. Creating a New Skill

Skills should be placed in the `skills/` directory:

```
skills/
└── your-skill-name/
    ├── index.js          # Main skill implementation
    ├── README.md         # Skill documentation
    ├── test.js          # Test file
    └── package.json     # Skill metadata (optional)
```

### 4. Skill Requirements

Each skill should:

- Follow the skill naming convention: `your-skill-name`
- Include proper error handling
- Have comprehensive test coverage (minimum 80%)
- Include clear documentation
- Use consistent coding style

### 5. Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### 6. Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix
```

### 7. Commit Guidelines

Use conventional commit format:

```
feat: add new nexacro build skill
fix: resolve deployment timeout issue
docs: update skill documentation
test: add unit tests for skill validation
chore: update dependencies
```

### 8. Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Create a pull request to the main branch
4. Fill out the PR template completely
5. Respond to code review comments

## 📋 Pull Request Template

```markdown
## Description
Brief description of the changes

## Changes Made
- [ ] Added new skill functionality
- [ ] Fixed existing issues
- [ ] Updated documentation
- [ ] Added tests

## Testing
- [ ] Manual testing completed
- [ ] Unit tests pass
- [ ] Integration tests pass

## Checklist
- [ ] Code follows project style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] PR description is clear
```

## 📚 Documentation

### Skill Documentation

Each skill should include:

- Description of what the skill does
- Required parameters and their types
- Return values
- Usage examples
- Error scenarios

### API Documentation

Update `docs/API.md` when adding new skill APIs or modifying existing ones.

## 🔧 Troubleshooting

Common issues and their solutions:

### Node.js Version Issues

```bash
# Use Node version specified in package.json
nvm use
```

### Dependency Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Getting Help

- Create an issue for bugs or feature requests
- Join our Discord/Slack community
- Check existing issues before creating new ones

## 📝 License

By contributing, you agree that your contributions will be licensed under the project's license.

## 🎯 Tips for Good Contributions

1. Start with small, focused contributions
2. Check existing issues before starting work
3. Communicate proactively about progress
4. Write tests for new features
5. Update documentation for API changes