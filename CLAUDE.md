# CLAUDE.md — aide_memoire_python

This file provides guidance for AI assistants (and developers) working in this repository.

## Project Overview

**aide_memoire_python** is a Python reference/cheat-sheet project — a curated collection of Python notes, examples, and patterns ("aide-mémoire" is French for "memory aid"). The repository is in its early stages.

## Repository Status

This is a newly initialized repository. The project structure, tooling, and conventions described below are the intended starting points and should be updated as the project evolves.

## Codebase Structure

```
aide_memoire_python/
├── CLAUDE.md          # This file — guidance for AI assistants
```

As the project grows, the expected layout is:

```
aide_memoire_python/
├── CLAUDE.md
├── README.md
├── pyproject.toml     # Project metadata and tool configuration
├── requirements.txt   # Dependencies (if not using pyproject.toml exclusively)
├── src/               # Source code (if packaged)
├── tests/             # Test files
└── docs/              # Additional documentation or notes
```

## Development Conventions

### Python Version

- Target Python 3.10+ unless otherwise specified.

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use type hints where practical (PEP 484 / PEP 604).
- Prefer f-strings over `.format()` or `%` formatting.
- Keep functions short and focused.

### Naming

- `snake_case` for functions, variables, and modules.
- `PascalCase` for classes.
- `UPPER_SNAKE_CASE` for constants.

### Documentation

- Include docstrings (Google or NumPy style) for public functions and classes.
- Keep inline comments minimal — prefer self-documenting code.

## Git Workflow

- **Default branch:** `main`
- Write clear, concise commit messages in imperative mood (e.g., "Add sorting examples").
- Keep commits atomic — one logical change per commit.

## Testing

- Use **pytest** as the test framework.
- Place tests in a `tests/` directory, mirroring the source structure.
- Run tests with: `pytest`

## Linting and Formatting

When tooling is added, prefer:

- **ruff** for linting and formatting (fast, replaces flake8 + isort + black).
- **mypy** for static type checking.

## Common Commands

```bash
# Run tests
pytest

# Run linter (once configured)
ruff check .

# Format code (once configured)
ruff format .

# Type check (once configured)
mypy .
```

## Notes for AI Assistants

- This repository is new; do not assume the existence of files or directories beyond what is present.
- When adding new content, follow the conventions above.
- Update this CLAUDE.md file when significant structural changes are made (new tooling, new directories, changed workflows).
- Prefer minimal, working examples over complex abstractions.
