# Contributing to PhonePilot

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `cd backend && pytest`
5. Run linter: `cd backend && ruff check .`
6. Commit your changes
7. Push and create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/phonepilot.git
cd phonepilot

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Frontend
cd ../frontend
npm install
```

## Code Style

- **Python**: Ruff for linting and formatting, type hints on all public functions
- **TypeScript**: ESLint, strict mode enabled
- No comments in code — write self-documenting code with clear naming

## Pull Request Process

1. Update documentation if you change public APIs
2. Add tests for new functionality
3. Ensure CI passes (lint + tests)
4. One approval required for merge

## Reporting Issues

- Use GitHub Issues
- Include steps to reproduce
- Include device info and model used
- Attach screenshots/logs if relevant
