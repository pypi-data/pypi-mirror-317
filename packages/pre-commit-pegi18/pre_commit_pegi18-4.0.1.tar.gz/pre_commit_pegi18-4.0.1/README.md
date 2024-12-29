[![build status](https://github.com/pre-commit/pre-commit/actions/workflows/main.yml/badge.svg)](https://github.com/pre-commit/pre-commit/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit/main.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit/main)

# Attention !
This version is a little patch do to modification during pre-commit. Because you're not child and assume the consequence.

/!\ It's just a really quick hack. there is no safeguard nor configuration by hook. Can add option if some people is interested. In this case I'll do an Autopatch CI to build from the upstream repo and stay up to date. I do not change the name of the package builded so it replace the initial one.

# Installation

there is no release for now
- install with
```
pip install git+https://github.com/ethan-0l/pre-commit-pegi18.git
```

or git local
```
git clone https://github.com/ethan-0l/pre-commit-pegi18.git
cd pre-commit-pegi18
pip install .
```
poetry :
```
poetry add git+https://github.com/ethan-0l/pre-commit-pegi18.git
```

# Use
- Add allow_modifications: true to hook
- Add allow_return_nzero: true to hook <- use with more caution
- Add allow_return_codes: [1,2,3.....,42,...] <- 0 is always allowed. Usefull for hook that has proper handling of failure vs modification.


*.pre-commit-config.yaml*
```yaml
  - repo: https....
    rev: v3.14.2
    hooks:
      - id: ...
        args: []
        stages:
          - pre-commit
        allow_modifications: true
```
ou set PRE_COMMIT_ALLOW_MODIFICATIONS a true
```pwsh
$env:PRE_COMMIT_ALLOW_MODIFICATIONS="true"
```
```bash
export PRE_COMMIT_ALLOW_MODIFICATIONS=true
```
also available : PRE_COMMIT_ALLOW_RETURN_NZERO
## pre-commit

A framework for managing and maintaining multi-language pre-commit hooks.

For more information see: https://pre-commit.com/
