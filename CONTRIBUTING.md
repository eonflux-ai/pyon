# Contributing to Pyon

Thank you for your interest in contributing to **Pyon**. The project is still in
alpha, so small, focused, reviewable changes are preferred.

## Contribution Scope

We welcome:

- Bug reports and reproducible failing cases.
- Documentation corrections.
- Tests for current public contracts.
- Small fixes that preserve public API behavior.
- New type support proposals after discussion.

Before submitting a pull request:

- Open an issue when the change affects public API, serialization format, decode behavior, or documentation taxonomy.
- Keep each pull request focused on one topic.
- Preserve the existing coding style and E-Notation structure.
- Do not apply automatic formatting to the project.

## Local Setup

The project is configured through `pyproject.toml`. A separate `requirements.txt`
file is intentionally not used.

```bash
git clone https://github.com/eonflux-ai/pyon.git
cd Pyon
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev,debug]"
```

Use the `.venv` environment for all project validation commands.

## Required Validation

At minimum, run the primary validation trio before opening a pull request:

```bash
.venv\Scripts\python -m pytest --cov=pyon --cov-report=term-missing
.venv\Scripts\python -m pyright
.venv\Scripts\python -m pylint pyon tests
```

The full audit validation also includes:

```bash
.venv\Scripts\python -m mypy pyon
.venv\Scripts\python -m ruff check .
.venv\Scripts\python -m bandit -r pyon -x tests
.venv\Scripts\python -m radon cc pyon tests -a
.venv\Scripts\python -m radon mi pyon tests
.venv\Scripts\python -m vulture pyon tests
.venv\Scripts\python -m build
```

Executable examples should remain valid:

```bash
Get-ChildItem examples -File -Filter *.py | ForEach-Object {
    .\.venv\Scripts\python $_.FullName
}
```

## Packaging

Runtime dependencies, optional development dependencies, package metadata, and
tool configuration live in `pyproject.toml`.

The package includes `pyon/py.typed`, so public inline annotations are part of
the distributed typing contract. Changes to public signatures should be treated
as API changes and reviewed carefully.

## Documentation

Keep documentation in the existing taxonomy:

- `README.md`: user-facing overview and quick-start material.
- `CONTRIBUTING.md`: contribution workflow.
- `CHANGELOG.md`: release history and unreleased user-visible changes.
- `doc/`: roadmap, tasks, version, security, release notes, and auxiliary docs.
- `examples/EXAMPLES.md`: documentation for executable examples.
- `pyon/file/README.md`: `File` submodule documentation.

Do not move historical release notes or audit records unless there is a clear
taxonomy change.

## Contact

For private contact, use:

**Email**: [pyon@eonflux.ai](mailto:pyon@eonflux.ai)

## Future Direction

As the project matures, we plan to:

- Formalize more contribution checks into CI.
- Keep automated testing and audit commands aligned with `pyproject.toml`.
- Invite trusted contributors to help maintain the library.

---

Thank you again for your support and interest in Pyon. Every thoughtful
contribution helps make it a better tool for the Python ecosystem.
