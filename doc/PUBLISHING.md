# Pyon Publishing Guide

This document defines the standard release and publishing workflow for Pyon.

Use it for every public release so branch merges, tags, GitHub, PyPI, badges,
and post-release checks stay aligned.

---

## 1. Release Preconditions

Before publishing:

- The release branch must have a clean working tree.
- The release branch must contain all approved audit patches.
- `pyproject.toml` must contain the target package version.
- `doc/VERSION.md`, `doc/TASKS.md`, `CHANGELOG.md`, and release notes must match the target version.
- `README.md`, examples, and package documentation must match the current project taxonomy.
- `.env` must not be committed and must contain only local secrets or local publishing settings.

Recommended checks:

```powershell
git status --short --branch
rg -n "^version =|^name =" pyproject.toml
```

---

## 2. Synchronize Remotes

Fetch the official GitHub remote before merging or tagging.

If old local tags conflict with remote tags, fetch branches without tags first
and inspect the conflict separately. Do not force-update tags unless the
release owner explicitly approves it.

```powershell
git fetch github --prune
git status --short --branch
```

The official remote should be:

```powershell
git remote -v
```

Expected project remote:

```text
github  https://github.com/eonflux-ai/pyon.git (fetch)
github  https://github.com/eonflux-ai/pyon.git (push)
```

Remove obsolete local remotes only after confirming they are no longer used:

```powershell
git remote remove origin
```

---

## 3. Merge Audit Back To Development

Use `desenv` as the integration branch and `Audit` as the audited release
candidate branch.

```powershell
git switch desenv
git merge --ff-only Audit
```

If local ignored files appear after switching branches, check whether `.gitignore`
differs between branches. Prefer letting the merge bring `.gitignore` from the
audited branch rather than creating a separate local-only commit.

---

## 4. Integrate GitHub Main

Before pushing to GitHub `main`, check whether local `desenv` and
`github/main` diverged.

```powershell
git rev-list --left-right --count github/main...desenv
git merge-base --is-ancestor github/main desenv
```

If `github/main` has commits not present in `desenv`, merge it into `desenv`
instead of force-pushing.

```powershell
git merge github/main
```

When conflicts happen:

- Resolve only the conflicted area.
- Preserve the current project taxonomy.
- Prefer current documentation paths such as `doc/SECURITY.md` over legacy paths such as `docs/SECURITY.md`.
- Re-run validation after the merge commit.

Do not use force-push for release publication unless there is a documented
reason and explicit approval.

---

## 5. Full Validation

Run validation from the project virtual environment.

```powershell
.\.venv\Scripts\pytest --cov=pyon --cov-report=term-missing
.\.venv\Scripts\pyright
.\.venv\Scripts\pylint pyon tests
.\.venv\Scripts\mypy pyon
.\.venv\Scripts\ruff check .
.\.venv\Scripts\bandit -r pyon -x tests
.\.venv\Scripts\radon cc pyon tests -a
.\.venv\Scripts\radon mi pyon tests
.\.venv\Scripts\vulture pyon tests
.\.venv\Scripts\python -m pip install -e ".[dev,debug]" --dry-run
.\.venv\Scripts\python -m build
```

Run all executable examples:

```powershell
Get-ChildItem examples -File -Filter *.py | ForEach-Object {
    .\.venv\Scripts\python $_.FullName *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "FAIL $($_.Name) $LASTEXITCODE"
    } else {
        Write-Output "PASS $($_.Name)"
    }
}
```

Release validation must not proceed if `pytest`, `pyright`, or `pylint` fails.

---

## 6. Verify Badges And Public Links

Check README badges before tagging, pushing to GitHub, or building PyPI
artifacts.

The release tag should point to a commit whose README already contains the
final public badge and link state.

PyPI renders the README from the package artifact metadata. If a badge is fixed
only after upload, GitHub will show the correction but the already-published
PyPI release page will keep the old README metadata for that version.

The PyPI version badge should use Shields, because it reflected the
`pyon-core` pre-release correctly during the `0.2.7a0` publication:

```md
[![PyPI version](https://img.shields.io/pypi/v/pyon-core.svg)](https://pypi.org/project/pyon-core/)
```

Avoid Badge Fury for this project unless it is verified to show the current
pre-release version before tagging and building artifacts.

Useful public links:

```text
https://github.com/eonflux-ai/pyon
https://pypi.org/project/pyon-core/
```

If a badge-only documentation fix is needed after tagging and publishing,
commit and push it to `github/main`, but do not move the release tag unless the
published artifact itself changes. If the PyPI page must also be corrected, a
new package version is required because uploaded release files are immutable.

---

## 7. Create Or Refresh The Release Tag

Create an annotated tag only after the final release commit is known.

```powershell
git tag -a v0.2.7-alpha -m "v0.2.7-alpha"
```

If a merge commit is created after tagging, recreate the local tag before
pushing it:

```powershell
git tag -d v0.2.7-alpha
git tag -a v0.2.7-alpha -m "v0.2.7-alpha"
```

Verify that the tag points to the final release commit:

```powershell
git rev-parse HEAD
git rev-list -n 1 v0.2.7-alpha
git show --no-patch --decorate --oneline v0.2.7-alpha
```

Use the actual target version in the commands above.

---

## 8. Publish To GitHub

Push `desenv` to GitHub `main`.

```powershell
git push github desenv:main
git fetch github --prune
git rev-parse github/main
git rev-parse desenv
```

Push the release tag after the branch push succeeds:

```powershell
git push github v0.2.7-alpha
git ls-remote --tags github "refs/tags/v0.2.7-alpha*"
```

The annotated tag object and dereferenced commit should both appear. The
dereferenced `^{}` commit must match the intended release commit.

---

## 9. Prepare PyPI Artifacts

Install `twine` if missing:

```powershell
.\.venv\Scripts\python -m pip install twine
```

Clean `dist/` before building so old artifacts are not uploaded accidentally:

```powershell
$root = (Resolve-Path .).Path
$dist = Join-Path $root "dist"
$resolvedDist = (Resolve-Path $dist).Path
if ($resolvedDist -eq $dist) {
    Get-ChildItem -LiteralPath $resolvedDist -Force | Remove-Item -Force -Recurse
}
```

Build and inspect artifacts:

```powershell
.\.venv\Scripts\python -m build
Get-ChildItem dist -Force | Select-Object Name,Length,LastWriteTime
```

Validate artifacts:

```powershell
.\.venv\Scripts\python -m twine check dist/*
```

Only the target version artifacts should exist in `dist/`.

---

## 10. Configure PyPI Credentials

Use a PyPI API token with Twine.

The username for API-token authentication is always:

```text
__token__
```

Store local credentials in `.env` only. `.env` must remain ignored by Git.

```env
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-...
```

Load credentials into the current PowerShell session without printing secrets:

```powershell
$envLines = Get-Content .env
foreach ($line in $envLines) {
    if ($line -match "^\s*#" -or $line -notmatch "=") {
        continue
    }
    $key, $value = $line -split "=", 2
    $key = $key.Trim()
    $value = $value.Trim()
    if ($key) {
        Set-Item -Path "Env:$key" -Value $value
    }
}
```

Validate presence only:

```powershell
if ($env:TWINE_USERNAME) { "TWINE_USERNAME=set" } else { "TWINE_USERNAME=missing" }
if ($env:TWINE_PASSWORD) { "TWINE_PASSWORD=set" } else { "TWINE_PASSWORD=missing" }
```

Never print the token value.

---

## 11. Publish To PyPI

Upload artifacts:

```powershell
.\.venv\Scripts\python -m twine upload --non-interactive dist/*
```

Verify publication:

```powershell
.\.venv\Scripts\python -m pip index versions pyon-core --pre
```

For alpha releases, users may need:

```powershell
pip install --pre pyon-core
```

---

## 12. Final Release Checklist

- [ ] `desenv` contains the audited release candidate.
- [ ] `github/main` was merged into `desenv` if needed.
- [ ] Full validation passed.
- [ ] README badges and public links were verified before tagging, GitHub push, and PyPI build.
- [ ] Release tag points to the final release commit.
- [ ] `desenv` was pushed to `github/main`.
- [ ] Release tag was pushed to GitHub.
- [ ] `dist/` contains only the target version artifacts.
- [ ] `twine check dist/*` passed.
- [ ] PyPI upload succeeded.
- [ ] PyPI index shows the target version.
- [ ] README badges reflect the published version.
- [ ] Working tree is clean.
