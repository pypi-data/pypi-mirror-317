Stefan The Coder

## Execute locally

```bash
. run_stefan.sh "europ" "fix tag typo in profile component"
```

## Testing

There are two types of tests:
- Fast tests (traditional unit tests) which do not require real API calls. 
- Slow tests which require real API calls (e.g. gspread, llm evals) Should not be called very often because they may hit API limits and since they are calling API they are slow.

To run only fast tests:
```bash
poetry run pytest -m "not slow"
```

To run only slow tests:
```bash
poetry run pytest -m "slow"
```

To run all tests:
```bash
poetry run pytest
```

## Deployment

To deploy to pypi:
1. Bump the version in `pyproject.toml`
2. Run `poetry build`
3. Run `poetry publish`
