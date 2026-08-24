# Complaint API Testing

Python API test automation extracted from a legacy Postman collection.

The original collection referenced private infrastructure, expired credentials,
and test data. Those values are intentionally **not** published here. The
sanitized collection and the Python tests use safe placeholders and a local
deterministic mock transport, so the project is runnable in a clean checkout
without access to the old environment.

## Quick start

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

Run the collection sanitizer after changing the source collection:

```powershell
python scripts/sanitize_collection.py path\to\collection.json
```

The generated collection is written to `postman/complaint-test.sanitized.json`.

## What is covered

- health and contract checks for representative auth, basic-data, complaint,
  organization, and Tamin endpoints;
- request construction with environment-based base URL and token;
- validation of response status, JSON shape, and error handling;
- CI execution through GitHub Actions.

To run against a real environment, set `API_BASE_URL` and `API_TOKEN` locally.
Never commit `.env` or live tokens.

## Project layout

```text
src/complaint_api_testing/  reusable API client and endpoint catalog
tests/                      deterministic pytest tests
postman/                    sanitized, shareable collection
scripts/                    collection sanitization utility
.github/workflows/          CI automation
```
