# Project Overview🏆


IT'S REVOLUTION!

## Python setup

Currently, the project is based on Python 3.10. To run it you would prefer using the following commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python --version # 3.10
which python #.venv/bin/python
```

## Commit hooks

There is a file which is responsible for linting and commit hooks. It is called pre-commit-config.yaml. It is based
on [pre-commit](https://pre-commit.com/). To run it you shoul use the following command:

```bash
pre-commit run --all-files
```

It is very important to run it before committing your changes to maintain the good code quality.

## Our workflow

1. Create a new branch from the main branch called feature/your-feature-name
2. Create a pull request to the main branch
3. Request a review from https://github.com/pro1code1hack or and wait for the review
4. If the review is approved, merge the pull request to the main branch
5. Delete the branch
6. Pull the changes from the main branch

## Tests

```bash
To be continued...
```

## Environmental setup

Create the .env file in the root directory of the project. It should contain the following variables:

```bash
To be continued...
```

## The project structure

```bash
To be continued...
```

## Deployment

```
uvicorn main:app --reload --port 3004
```