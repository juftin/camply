# Contributing

## Environment Setup

> TIP: **pipx**
>
> This documentaion uses [pipx] to
> install and manage non-project command line tools like `hatch` and
> `pre-commit`. If you don't already have `pipx` installed, make sure to
> see their [documentation](https://pypa.github.io/pipx/installation/).
> If you prefer not to use `pipx`, you can use `pip` instead.

1.  Install [hatch](https://hatch.pypa.io/latest/)

    ```shell
    pipx install hatch
    ```

    > NOTE: **pre-commit**
    >
    > Hatch will attempt to set up pre-commit hooks for you using
    > [pre-commit]. If you don't already,
    > make sure to install pre-commit as well: `pipx install pre-commit`

2.  Build the Virtual Environment

    ```shell
    hatch env create
    ```

3.  If you need to, you can link a hatch virtual environment to your IDE.
    They can be located by name with the `env find` command:

    ```shell
    hatch env find test
    ```

4.  Activate the Virtual Environment

    ```shell
    hatch shell
    ```

## Using Hatch

### Hatch Cheat Sheet

| Command Description            | Command                     | Notes                                                      |
| ------------------------------ | --------------------------- | ---------------------------------------------------------- |
| Run Tests                      | `hatch run cov`             | Runs tests with `pytest` and `coverage`                    |
| Run Formatting                 | `hatch run lint:fmt`        | Runs `ruff` code formatter                                 |
| Run Linting                    | `hatch run lint:all`        | Runs `ruff` and `mypy` linters / type checkers             |
| Run Type Checking              | `hatch run lint:typing`     | Runs `mypy` type checker                                   |
| Update Requirements Lock Files | `hatch run gen:reqs`        | Updating lock file using `pip-compile`                     |
| Upgrade Dependencies           | `hatch run gen:reqs-update` | Updating lock file using `pip-compile` and `--update` flag |
| Serve the Documentation        | `hatch run docs:serve`      | Serve the documentation using MkDocs                       |
| Run the `pre-commit` Hooks     | `hatch run lint:precommit`  | Runs the `pre-commit` hooks on all files                   |

### Hatch Explanation

Hatch is a Python package manager. Its most basic use is as a standardized build-system.
However, hatch also has some extra features which this project takes advantage of.
These features include virtual environment management and the organization of common
scripts like linting and testing. All the operations in hatch take place in one
of its managed virtual environments.

Hatch has a variety of environments, to see them simply ask hatch:

```bash exec="on" result="markdown" source="tabbed-left" tabs="hatch CLI|Output"
hatch env show
```

That above command will tell you that there are five environments that
you can use:

-   `default`
-   `docs`
-   `gen`
-   `lint`
-   `test`

Each of these environments has a set of commands that you can run.
To see the commands for a specific environment, run:

```bash exec="on" result="markdown" source="tabbed-left" tabs="hatch CLI|Output"
hatch env show default
```

Here we can see that the `default` environment has the following commands:

-   `cov`
-   `test`

The one that we're interested in is `cov`, which will run the tests
for the project.

```bash
hatch run cov
```

Since `cov` is in the default environment, we can run it without
specifying the environment. However, to run the `serve` command in the
`docs` environment, we need to specify the environment:

```bash
hatch run docs:serve
```

You can see what scripts are available using the `env show` command

```bash exec="on" result="markdown" source="tabbed-left" tabs="hatch CLI|Output"
hatch env show docs
```

## Committing Code

This project uses [pre-commit] to run a set of
checks on the code before it is committed. The pre-commit hooks are
installed by hatch automatically when you run it for the first time.

This project uses [semantic-versioning] standards, managed by [semantic-release].
Releases for this project are handled entirely by CI/CD via pull requests being
merged into the `main` branch. Contributions follow the [gitmoji] standards
with [conventional commits].

While you can denote other changes on your commit messages with [gitmoji], the following
commit message emoji prefixes are the only ones to trigger new releases:

| Emoji | Shortcode     | Description                 | Semver |
| ----- | ------------- | --------------------------- | ------ |
| 💥    | \:boom\:      | Introduce breaking changes. | Major  |
| ✨    | \:sparkles\:  | Introduce new features.     | Minor  |
| 🐛    | \:bug\:       | Fix a bug.                  | Patch  |
| 🚑    | \:ambulance\: | Critical hotfix.            | Patch  |
| 🔒    | \:lock\:      | Fix security issues.        | Patch  |

Most features can be squash merged into a single commit on a pull-request.
When merging multiple commits, they will be summarized into a single release.

If you're working on a new feature, your commit message might look like:

```text
✨ New Feature Description
```

Bug fix commits would look like this:

```text
🐛 Bug Fix Description
```

If you're working on a feature that introduces breaking changes, your
commit message might look like:

```text
💥 Breaking Change Description
```

Other commits that don't trigger a release might look like this:

```text
📝 Documentation Update Description
👷 CI/CD Update Description
🧪 Testing Changes Description
🚚 Moving/Renaming Description
⬆️ Dependency Upgrade Description
```

### Pre-Releases

[semantic-release] supports pre-releases. To trigger a pre-release, you
would merge your pull request into an `alpha` or `beta` branch.

### Specific Release Versions

In some cases you need more advanced control around what kind of release you
need to create. If you need to release a specific version, you can do so by creating a
new branch with the version number as the branch name. For example, if the
current version is `2.3.2`, but you need to release a fix as `1.2.5`, you
would create a branch named `1.2.x` and merge your changes into that branch.

See the [semantic-release documentation] for more information about
branch based releases and other advanced release cases.

[pipx]: https://pypa.github.io/pipx/
[pre-commit]: https://pre-commit.com/
[gitmoji]: https://gitmoji.dev/
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[semantic-release]: https://github.com/semantic-release/semantic-release
[semantic-versioning]: https://semver.org/
[semantic-release documentation]: https://semantic-release.gitbook.io/semantic-release/usage/configuration#branches
