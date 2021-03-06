# Contributing

Camply makes use of a couple tools to help with contributing: `pre-commit` and `tox`

```commandline
pip install pre-commit
pip install tox

pre-commit install
pre-commit run
tox
```

- `pre-commit`
    - [pre-commit](https://pre-commit.com/) is a tool to manage git-hooks scripts, which are useful
      for identifying simple issues before submission to code review.
    - `camply`'s instance of `pre-commit` uses tools like [black](https://github.com/psf/black)
      and
      [isort](https://pycqa.github.io/isort/) to format your code in a standardized way
    - `pre-commit` can be installed with pip, brew, or conda.
    - After cloning this repo run `pre-commit install`
    - Done, now pre-commit will run automatically on git commit. To run it manually on your changed
      code run `pre-commit run` on your command line
- `tox`
    - [tox](https://tox.wiki/en/latest/) is a tool to standardize and manage testing and routines
      using Python virtual environments
    - `tox` can be installed with pip
    - `camply`'s instance of `tox` runs Python unit tests, and uses tools like
      [mypy](https://github.com/python/mypy) and [flake8](https://flake8.pycqa.org/en/latest/pre) to
      format
    - To run all `tox` tests (which get run as part of GitHub Actions) locally, just enter `tox`
      into your command line
