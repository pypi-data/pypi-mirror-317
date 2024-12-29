# Sweepr

[![Python Lint](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml/badge.svg)](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml) [![PyPI Publish](https://github.com/activatedgeek/sweepr/actions/workflows/publish.yml/badge.svg?event=release)](https://github.com/activatedgeek/sweepr/actions/workflows/publish.yml) [![PyPI Latest Version](https://img.shields.io/pypi/v/sweepr)](https://pypi.org/project/sweepr)

## Install

To install PyPI package run,
```shell
pip install sweepr
```

To use `wandb` provider, run:
```shell
pip install sweepr[wandb]
```

## Usage

See [examples/sweep.py](./examples/sweep.py) for a condensed example of all features.

## Development

We use [`uv`](https://docs.astral.sh/uv/) to manage dependencies.

Install dependencies as:
```shell
uv sync --refresh --no-install-project --extra dev
```

Then install `sweepr` using

```shell
uv pip install -U -e .[dev]
```

## License

Apache License 2.0
