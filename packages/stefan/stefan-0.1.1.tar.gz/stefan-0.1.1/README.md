KMP coder

## Testing

```bash
poetry run pytest # Will run all tests
```

```bash
poetry run pytest -m "not slow" # Will run all tests except slow tests with real API calls (e.g. gspread)
```

```bash
poetry run pytest -m "slow" # Will run all slow tests with real API calls (e.g. gspread)
```
