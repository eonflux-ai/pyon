# Agent Instructions

## Project Analysis

The agent shall read all Markdown (`.md`) files in the project to understand what the project does.

Then, the agent shall read all Python source files (`.py`) to understand how the documented features were implemented.

Python modules whose filenames end with `copy.py` must be ignored.

## Documentation vs. Implementation Review

Based on the analysis, the agent must identify:

- What has already been implemented.
- What has already been tested.
- What is still pending according to the documentation.
- What should be done next according to the documentation.

The agent must then output a report to the user describing the current state of the project.

## Next-Step Guidance

After showing the report, the agent shall ask the user whether they want hints for the next step.

If the user says yes, the agent must:

- Identify which source code files should be changed.
- Show examples of what code to use.
- Explain why those changes are appropriate.

From that point onward, the agent shall interact with the user to help further advance the software development stage.

## Coding and Documentation Standards

The agent must read `[e-notation (v{n}).md]` and use E-Notation in all examples and implementations. `n` is a version number, use the latest.

All code and documentation must be written in English.

The agent may interact with the user in the user's own language, Brazilian Portuguese.

The agent must preserve the project's visual code organization, blank-line structure, spacing style, and E-Notation layout.

The agent must not collapse deliberately separated code blocks merely to satisfy external style preferences.

After refactors, the agent must re-check E-Notation numbering, especially:

- top-level comments must remain ordered as `# 1`, `# 2`, `# 3`, and so on;
- nested comments must match the indentation level that owns them;
- duplicated numbers, skipped numbers, or reset sequences usually indicate refactor drift;
- numbered comments must include short descriptive text, not only the number.

Trivial one-line functions without docstrings do not need numbered comments.

If a function has a docstring, it should normally use numbered E-Notation body comments unless the surrounding project style clearly establishes otherwise.

## Documentation Synchronization

Project documentation is part of the implementation contract.

After code changes, the agent must evaluate whether documentation may have
become outdated.

If the code change affects public API, result shapes, flags, statuses,
semantics, architecture, tests, roadmap, or conceptual behavior, the agent must
inform the user that documentation should be updated.

Public string-keyed dictionaries are observable API.

The agent must treat result keys, flag tags, statuses, enum values, and documented
dictionary shapes as public contracts when they appear in user-facing results,
tests, or documentation.

The agent must:

- identify which documentation files are affected;
- explain what should be inserted or changed;
- respect the existing documentation taxonomy;
- make only punctual, coherent documentation changes;
- ask the user before editing documentation unless the user explicitly requested documentation updates.

If the code change is purely mechanical, internal, or does not affect documented
behavior, no documentation update is required.

## Documentation Role Clarity

When creating or substantially editing technical documentation, the agent should
ensure the document's role is clear near the beginning, preferably in natural
prose.

The agent must avoid heavy metadata-style headers unless the file already uses
that style.

Human-facing documents such as `README.md`, narrative philosophy documents, and
research notes should remain pleasant to read and should not receive explicit
taxonomy blocks.

For technical contract documents, a short natural paragraph may clarify what
belongs in the file and which related document owns adjacent concerns.

## Context Compaction Safety

The instructions in this file are authoritative and must not be summarized, paraphrased, or compressed when the agent has any control over context compaction.

If context compaction occurs, the agent must preserve these instructions verbatim whenever possible and compact only the user interaction history.

If the agent detects or suspects any context compaction, context reset, resume, memory injection, external context manipulation, or unexpected loss of conversational state, it must immediately re-read:

- this instruction file: `agents/dev-agent.md`.
- notation e file: `doc/e-notation (v{n}).md`. (use latest `n`)

The agent must do this before continuing any code change, documentation change, validation step, implementation step, or project analysis.

After re-reading these files, the agent must resume its role according to this instruction file and must continue enforcing E-Notation as the primary project coding structure.

The agent must never rely on memory alone after context compaction or external context manipulation when the instruction files are available.

## Testing, Linting, and Type Checking

To run `pytest`, the agent must use the project virtual environment located at `.venv`.

The agent must also run `pylint` and `pyright` on the code and inform the user of any validation errors or warnings.

After any code modification, the agent must always run all three commands:

- `pytest`
- `pylint`
- `pyright`

This rule is mandatory even for small code changes.

No error reported by `pytest`, `pylint`, or `pyright` may remain if it was caused by the agent's own changes.

The agent must process validation findings item by item.

For each validation finding, the agent must determine whether it is:

- caused by the agent's own changes;
- caused by existing user changes;
- a real issue;
- a warning;
- a false positive;
- a trivial fix;
- a non-trivial fix requiring user approval.

The agent may fix trivial issues directly when the correction is mechanical,
local, human-reviewable, and does not alter behavior or contracts.

Examples of trivial issues include:

- unused imports;
- clearly unused private local variables;
- obvious typo fixes;
- simple local renames that do not affect public API;
- small local annotation fixes when the intended type is already explicit;
- minor local cleanup that does not alter behavior.

The agent must ask the user before applying any fix that requires:

- refactoring;
- behavior changes;
- logic changes;
- public API changes;
- result shape changes;
- changes to class or function contracts;
- changes to flags, statuses, or documented semantics;
- changes to tests that alter expected behavior;
- removal of apparently unused public methods, classes, constants, or exports;
- suppressing warnings through ignore comments or configuration changes;
- broad formatting changes;
- large batches of unrelated modifications.

The agent must keep each patch small enough for human review before commit.

The agent must not apply large batches of unrelated changes.

If a required fix is non-trivial, the agent must:

- explain the issue;
- identify where it happens;
- explain why it happens;
- suggest one or more possible fixes;
- recommend the safest path;
- wait for user approval before applying the change.

If `pytest` reports errors:

- If the error was caused by the agent's own changes, the agent must fix it before continuing.
- If the error was caused by existing user changes, the agent must inform the user:
  - that the error exists;
  - why it happens;
  - where it happens;
  - how to fix it;
  - what patch should be applied.
- If fixing the user-originated error requires meaningful logic changes, the agent must ask the user before applying the fix.

If `pytest` reports warnings:

- If the warning was caused by the agent's own changes, the agent must fix it before continuing.
- If the warning was caused by existing user changes, the agent must inform the user:
  - that the warning exists;
  - why it happens;
  - where it happens;
  - how to fix it;
  - what patch should be applied.
- The agent must ask the user before applying a user-originated warning fix when the fix changes behavior or logic.

If `pylint` reports errors or warnings:

- If the issue was caused by the agent's own changes, the agent must fix it before continuing.
- If the issue was caused by existing user changes, the agent must inform the user:
  - that the lint issue exists;
  - why it happens;
  - where it happens;
  - how to fix it;
  - what patch should be applied.
- If fixing a user-originated lint issue requires meaningful code or logic changes, the agent must ask the user before applying the fix.
- Simple formatting or style issues introduced by the agent must be fixed immediately, but without using automatic formatting tools.

The agent must not suppress `pylint` warnings or errors through ignore comments or configuration changes unless the user explicitly approves the suppression.

If `pyright` reports errors:

- If the error was caused by the agent's own changes, the agent must fix it before continuing.
- If the error was caused by existing user changes, the agent must inform the user:
  - that the type issue exists;
  - why it happens;
  - where it happens;
  - how to fix it;
  - what patch should be applied.
- If fixing the user-originated type issue requires meaningful logic changes, contract changes, public API changes, or type model changes, the agent must ask the user before applying the fix.

The agent must not weaken type precision merely to satisfy `pyright`.

The agent must not add broad ignore comments, broad casts, or configuration suppressions unless the user explicitly approves them.

## Project Bootstrap and Minimum Documentation Taxonomy

The agent must verify whether the project has a minimum development structure before performing implementation, validation, or documentation work.

The project root is the directory that contains the `agents` folder.

If the agent has difficulty identifying or locating the project root, it may ask the user for clarification before initializing Git, creating files, creating virtual environments, installing dependencies, or changing project configuration.

If the agent detects that the project root is not a Git repository, it must initialize one with `git init`.

The Git repository must be initialized in the project root.

If the agent detects that the project does not contain a `.gitignore` file in the project root, it must create a minimal `.gitignore`.

The minimum `.gitignore` should include common Python, virtual environment, cache, build, coverage, and temporary file entries.

It must also ignore Python source copies whose filenames end with `copy.py`, because those files are not part of the active source review contract.

Recommended minimum `.gitignore`:

```gitignore
.venv/
venv/
env/

.pytest_cache/
**/.pytest_cache/

__pycache__/
**/__pycache__/
*.py[cod]
*$py.class

*.egg-info/
**/*.egg-info/
.eggs/

build/
dist/
pip-wheel-metadata/

.coverage
.coverage.*
htmlcov/

.mypy_cache/
.ruff_cache/
.hypothesis/

tmp/
temp/

*copy.py
```

If the agent detects that the project does not contain a `pyproject.toml` file in the project root, it must create one.

The created `pyproject.toml` must be minimal, valid, and compatible with the current project.

The agent must not invent package metadata when the information is unknown.

If package metadata is unclear, the agent may use conservative placeholders only when necessary and must clearly report what should be reviewed by the user.

The agent must ensure that validation dependencies are declared in the `pyproject.toml` file under `[project.optional-dependencies]`.

The recommended optional dependency groups are:

- `dev` for the primary development trio.
- `debug` for extended audit and diagnostic tools.

Example:

```toml
[project.optional-dependencies]
dev = [
    "pytest",
    "pylint",
]
debug = [
    "pyright",
    "ruff",
    "bandit",
    "radon",
    "vulture",
    "mypy",
    "build",
]
```

If the project already has a `pyproject.toml`, the agent must preserve existing configuration and make only the minimal additions required to include the development dependencies.

If the agent detects that the project does not contain a virtual environment at `.venv` in the project root, it must create one.

When creating or preparing the project virtual environment, the agent must:

- create the virtual environment at `.venv`;
- update the virtual environment's `pip` before installing packages;
- install the project with its development and debug extras into the virtual environment.

The agent must use the `.venv` environment for project validation commands.

The agent must also ensure that the project has a minimum documentation taxonomy.

At minimum, the project should contain:

- `README.md`
- `doc/Architecture.md`

The `README.md` file should provide a concise human-facing overview of the project, including what the project is, what problem it solves, how to install or prepare it, and how to run the main validation or usage commands.

The `doc/Architecture.md` file should describe how the system works internally, including its main modules, responsibilities, data flow, relevant design decisions, and known architectural constraints.

The purpose of `doc/Architecture.md` is to help the agent and future maintainers continue from where development stopped after context loss, task interruption, or later project resumption.

When creating these documents, the agent must keep them minimal, accurate, and aligned with the current implementation.

The agent must not invent undocumented behavior.

If the implementation is incomplete or unclear, the agent must explicitly mark the relevant section as pending, unknown, or requiring user confirmation.

When the agent changes project structure, configuration, public behavior, validation commands, or architectural responsibilities, it must evaluate whether `README.md` or `doc/Architecture.md` should be updated.
