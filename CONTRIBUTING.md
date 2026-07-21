# Contributing to CrimeMatrix

Thank you for your interest in contributing to CrimeMatrix. This document provides guidelines and instructions for contributing.

---

## How to Report Bugs

1. Check [existing issues](https://github.com/your-org/CrimeMatrix/issues) to avoid duplicates
2. Open a new issue using the **Bug Report** template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, Node version)

---

## How to Suggest Features

1. Check [existing issues](https://github.com/your-org/CrimeMatrix/issues) for similar suggestions
2. Open a new issue using the **Feature Request** template
3. Describe:
   - The problem the feature solves
   - How it would work
   - Why it matters for law enforcement use cases

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama (for AI features)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/CrimeMatrix.git
cd CrimeMatrix

# Run setup
make setup

# Seed the database
make seed

# Start development servers
make dev
```

This starts:
- Backend at `http://localhost:8000`
- AI Services at `http://localhost:8002`
- Frontend at `http://localhost:5173`

---

## Code Style

### Python (Backend & AI Services)

- Follow PEP 8
- Use type hints
- Keep functions focused and short
- Use `structlog` for logging
- Write docstrings for public functions

### JavaScript (Frontend)

- Use functional components with hooks
- Follow the existing component patterns in `src/components/`
- Use Tailwind CSS for styling
- Keep components focused and reusable

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style guidelines
4. **Test your changes**:
   ```bash
   make test
   ```
5. **Commit** with a clear message:
   ```bash
   git commit -m "Add: brief description of change"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** against `main`

### Commit Message Format

```
Type: Short description (optional longer description)

Types:
- Add: New feature or file
- Fix: Bug fix
- Update: Enhancement to existing feature
- Remove: Removing code or files
- Refactor: Code restructuring without behavior change
- Docs: Documentation changes
- Test: Adding or updating tests
```

---

## What to Contribute

### High Priority

- Bug fixes
- Test coverage improvements
- Documentation improvements
- Performance optimizations

### Medium Priority

- New AI tools for the tool registry
- New investigation workflows
- UI/UX improvements
- Additional crime type support

### Ideas

- New prediction models
- Additional language support
- Mobile-responsive improvements
- Accessibility improvements

---

## Questions?

Open an issue with the **Question** label, or start a discussion in the repository's Discussions tab.
