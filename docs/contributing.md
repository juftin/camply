# Contributing

## Quickstart

```shell
pipx install pre-commit
pipx install hatch
pre-commit install
hatch env create
hatch shell
```

## Tools

This project makes use of a couple tools to streamline the development process:
[pre-commit](https://pre-commit.com/) and [hatch](https://hatch.pypa.io/).

### pre-commit

[pre-commit] is a tool to manage git-hooks scripts, which are useful
for identifying simple issues before submission to code review.

```commandline
pipx install pre-commit
pre-commit install
```

To use pre-commit, you must first install it. [pipx] is preferred, but you can also install with
`pip`. Once [pre-commit] is installed, run `pre-commit install` to install the git-hooks scripts
into the local repository. Done, now pre-commit will run automatically on git commit. To run it
manually on your changed files run `pre-commit run` on your command line.

### hatch

[hatch](https://hatch.pypa.io/) is a tool to manage the packaging and distribution of Python packages. It also
used to manage the virtual environment for the project and running common scripts.

```commandline
pipx install hatch
hatch env create
hatch run test
```

## Commit Message Format

Releases for this project are handled entirely by CI/CD via Pull requests being merged into
the `main` branch. Contributions follow the [gitmoji] standards with [conventional commits],
orchestration is handled by the [semantic-release] tool.

While you can denote other changes on your commit messages with gitmoji, the following
commit message emoji prefixes are the only ones to trigger new releases:

| Emoji | Shortcode   | Description                 | Semver |
| ----- | ----------- | --------------------------- | ------ |
| 💥    | :boom:      | Introduce breaking changes. | Major  |
| ✨    | :sparkles:  | Introduce new features.     | Minor  |
| 🐛    | :bug:       | Fix a bug.                  | Patch  |
| 🚑    | :ambulance: | Critical hotfix.            | Patch  |
| 🔒    | :lock:      | Fix security issues.        | Patch  |

Most features can be squash merged into a single commit. If you're working on a
feature, your commit message might look like:

```text
✨ New Feature Description
```

Bug fix commits would look like this:

```text
🐛 Bug Fix Description
```

## Scripts

All common scripts for this repository are managed by [hatch](#hatch).

```shell
hatch run <script>
```

| Script         | Script Description                                      |
| -------------- | ------------------------------------------------------- |
| `format`       | Code Formatting [black] and [ruff]                      |
| `lint`         | Code Linting [black] and [ruff]                         |
| `check`        | Type Checking with [mypy]                               |
| `test`         | Unit Testing with [pytest]                              |
| `all`          | Run multiple scripts: `format`, `lint`, `check`, `test` |
| `docs-serve`   | Documentation Serving [MkDocs] and [mkdocs-material]    |
| `requirements` | Lock File Updates with [pip-tools]                      |

!!! note

    While the camply codebase is undergoing some refactoring, the `check` script is not
    required. Once the codebase is fully typed, the `check` script will be required to pass
    before a Pull Request can be merged. In the meantime, please use
    [type annotations](https://docs.python.org/3/library/typing.html) on any new changes.

## Dependencies

Dependencies are managed by [pip-tools / pip-compile](https://github.com/jazzband/pip-tools/).
After updating dependencies in the `pyproject.toml` file, run the following to update the
underlying `requirements.txt` files:

```shell
hatch run requirements
```

[pipx]: https://pipxproject.github.io/pipx/
[pre-commit]: https://pre-commit.com/
[gitmoji]: https://gitmoji.dev/
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[semantic-release]: https://github.com/semantic-release/semantic-release
[black]: https://github.com/psf/black
[ruff]: https://github.com/charliermarsh/ruff
[mypy]: https://mypy.readthedocs.io/en/stable/
[pytest]: https://docs.pytest.org/en/stable/
[MkDocs]: https://www.mkdocs.org/
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[pip-tools]: https://github.com/jazzband/pip-tools/
