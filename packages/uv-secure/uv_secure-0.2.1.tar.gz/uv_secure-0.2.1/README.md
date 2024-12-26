# uv-secure

Scan your uv.lock file for dependencies with known vulnerabilities

## Installation

I recommend installing uv-secure as a uv tool or with pipx as it's intended to be used
as a CLI tool, and it probably only makes sense to have one version installed globally.

Installing with uv tool as follows:

```shell
uv tool install uv-secure
```

or with pipx:

```shell
pipx install uv-secure
```

you can optionally install uv-secure as a development dependency in a virtual
environment.

## Usage

After installation, you can run uv-secure --help to see the options.

```text
>> uv-secure --help

 Usage: run.py [OPTIONS] [UV_LOCK_PATHS]...

 Parse uv.lock files, check vulnerabilities, and display summary.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────╮
│   uv_lock_paths      [UV_LOCK_PATHS]...  Paths to the uv.lock files [default: None]  │
╰──────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ --ignore              -i      TEXT  Comma-separated list of vulnerability IDs to     │
│                                     ignore, e.g. VULN-123,VULN-456                   │
│ --version                           Show the application's version                   │
│ --install-completion                Install completion for the current shell.        │
│ --show-completion                   Show completion for the current shell, to copy   │
│                                     it or customize the installation.                │
│ --help                              Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

By default, if run with no arguments uv-secure will look for a uv.lock file in the
current working directory and scan that for known vulnerabilities. E.g.

```text
>> uv-secure
Checking dependencies for vulnerabilities...
╭───────────────────────────────╮
│ No vulnerabilities detected!  │
│ Checked: 160 dependencies     │
│ All dependencies appear safe! │
╰───────────────────────────────╯
```

## Pre-commit Usage

uv-secure can be run as a pre-commit hook by adding this configuration to your
.pre-commit-config.yaml file:

```yaml
  - repo: https://github.com/owenlamont/uv-secure
    rev: 0.2.0
    hooks:
      - id: uv-secure
```

You should run:

```shell
pre-commit autoupdate
```

Or manually check the latest release and update the _rev_ value accordingly.

The uv-secure pre-commit at present assumes the uv.lock file is in the root directory
from where pre-commit is run.

## Roadmap

Below are some ideas (in no particular order) I have for improving uv-secure:

- Support reading configuration from pyproject.toml
- Support reading configuration for multiple pyproject.toml files for mono repos
- Package for conda on conda-forge
- Add rate limiting on how hard the PyPi json API is hit to query package
  vulnerabilities (this hasn't been a problem yet but I suspect may be for uv.lock files
  with many dependencies).
- Explore some local caching for recording known vulnerabilities for specific package
  versions to speed up re-runs.
- Add support for other lock file formats beyond uv.lock.
- Add a severity threshold option for reporting vulnerabilities against.
- Add an autofix option for updating package versions with known vulnerabilities if
  is a more recent fixed version.
- Add translations to support languages beyond English (not sure of the merits of this
  given most vulnerability reports appear to be only in English but happy to take
  feedback on this).

## Related Work and Motivation

I created this package as I wanted a dependency vulnerability scanner but I wasn't
completely happy with the options that were available. I use
[uv](https://docs.astral.sh/uv/) and wanted something that works with uv.lock files but
neither of the main package options I found were as frictionless as I had hoped:

- [pip-audit](https://pypi.org/project/pip-audit/) uv-secure is very much based on doing
  the same vulnerability check that pip-audit does using PyPi's json API. pip-audit
  however only works with requirements.txt so to make it work with uv projects you need
  additional steps to convert your uv.lock file to a requirements.txt then you need to
  run pip-audit with the --no-deps and/or --no-pip options to stop pip-audit trying to
  create a virtual environment from the requirements.txt file. In short, you can use
  pip-audit instead of uv-secure albeit with a bit more friction for uv projects. I hope
  to add extra features beyond what pip-audit does or optimise things better (given the
  more specialised case of only needing to support uv.lock files) in the future.
- [safety](https://pypi.org/project/safety/) also doesn't work with uv.lock file out of
  the box, it does apparently work statically without needing to build a virtual
  environment but it does require you to create an account on the
  [safety site](https://platform.safetycli.com/). They have some limited free account
  but require a paid account to use seriously. If you already have a safety account
  though there is a [uv-audit](https://pypi.org/project/uv-audit/) package that wraps
  safety to support scanning uv.lock files.
- [Python Security PyCharm Plugin](https://plugins.jetbrains.com/plugin/13609-python-security)
  Lastly I was inspired by Anthony Shaw's Python Security plugin - which does CVE
  dependency scanning within PyCharm.

I build uv-secure because I wanted a CLI tool I could run with pre-commit. Statically
analyse the uv.lock file without needing to create a virtual environment, and finally
doesn't require you to create (and pay for) an account with any service.

## Contributing

Please raise issues for any bugs you discover with uv-secure. If practical and not too
sensitive sharing the problem uv.lock file would help me reproduce and fix these issues.
I welcome PRs for minor fixes and documentation tweaks. If you'd like to make more
substantial contributions please reach out by email / social media / or raise an
improvement issue to discuss first to make sure our plans are aligned before creating
any large / time-expensive PRs.
