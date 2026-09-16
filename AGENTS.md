# AGENTS.md

`codescape-bank-parse` is a library for multi-format bank documents.

## Repository Layout

- This is a Python 3.12+ `uv` library using the `src/` layout.
- Package code lives in `src/codescape/parse/`.
- Tests live in `tests/` and use pytest.
- Dependencies and tool configuration are defined in `pyproject.toml`; `uv.lock` is committed.
- `pyproject.toml` is the explicit source of truth for Python version, dependency groups, Ruff settings, mypy settings, pytest configuration, and coverage thresholds. If a configuration question arises, check `pyproject.toml` before relying on any other file or editor default.

## Development Commands and Conventions

Use uv from the repository root:

- `uv sync --locked --all-extras --dev`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy .`

Follow these conventions:

- Target Python 3.12 or newer.
- Use 4 spaces and a maximum line length of 88 characters.
- Use double-quoted strings, consistent with Ruff format configuration.
- Add explicit annotations for functions, parameters, and return values.
- Avoid broad refactors and unrelated formatting changes.
- Do not add comments that merely restate the code. Add a comment only when the
  reason for a non-obvious decision cannot be expressed clearly in the code.

## Validation and Verification Commands

Run commands from the repository root with uv available.

### Install and Synchronize

```sh
uv sync --locked --all-extras --dev
```

Use this before validation or when dependencies, repository metadata, or `uv.lock`
change. The locked form ensures the installed dependency graph matches the lockfile.

### CI checks

The authoritative CI workflow is [.github/workflows/ci.yml](.github/workflows/ci.yml).
It runs these commands after installing dependencies:

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest
```

Run the same sequence locally before submitting a change. Ruff lint checks rules
configured in `pyproject.toml`, Ruff format check detects unformatted files, mypy
runs strict type checking, and pytest runs the complete test suite with the
configured coverage threshold.

### Formatting and Linting

```sh
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .
uv run ruff format --check .
```

Use `--fix` and `ruff format .` only when you intend to modify files. Review the
resulting diff afterward. The CI-safe commands are the non-mutating checks.

### Type Checking

```sh
uv run mypy .
```

### Tests and Coverage

```sh
uv run pytest
```

Tests use pytest and are discovered from `tests` according to the root
`pyproject.toml`. The default test command enables branch coverage and fails when
total coverage is below 80%.

Use fixtures and monkeypatching to isolate services, repositories, filesystem paths,
and other external state.

Run focussed tests during development before running the full test suite.

### Pre-commit verification

```sh
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
```

The configured hooks verify the uv lockfile, large files, JSON, TOML, YAML, EOFs,
trailing whitespace, Ruff linting, and Ruff formatting. The pre-push stage also runs:

```sh
uv run pytest
```

Run pre-commit after changing Python, configuration, workflow, or lock files.

### Syntax and diagnostics

```sh
python -m compileall src tests
uv run pytest --collect-only
```

Use `compileall` for a quick Python syntax check and `pytest --collect-only` to
verify test discovery without executing tests.

Also check the VS Code Problems view with Pylance enabled for every changed
Python file and resolve reported errors before submitting the change. Pylance
diagnostics complement -- but do not replace -- the repository-wide mypy check.

## Change Workflow

1. Read the owning implementation and its neighboring tests before editing.
2. Make the smallest change that addresses the requested behavior.
3. Run a focused test or check immediately after the first edit.
4. Run Ruff, mypy, and relevant tests for the touched packages.
5. Run the complete CI-equivalent sequence for cross-package or shared changes.
6. Review `git diff` and ensure generated coverage artifacts or unrelated files are
   not included unintentionally.

## CI and Pull Requests

Changes targeting `main` are validated by the `code-quality` job in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) on pushes and pull requests.
The workflow uses Python 3.12, installs with `uv sync --locked`, and requires all
Ruff, mypy, and pytest checks to pass.

Do not weaken lint, type, test, or coverage settings to make a change pass. Fix the
underlying code or add focused tests for the behavior being changed.
