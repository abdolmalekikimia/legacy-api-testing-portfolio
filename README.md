# Legacy API Testing Portfolio

This is a public QA/SDET portfolio project built from a legacy Postman
collection. It is not a production application and it is not presented as a
currently runnable integration environment.

For confidentiality and security reasons, this public repository does not
attempt live API calls. It is intended for portfolio viewing and demonstrates
the organization of API tests, collection design, assertions, and automation
structure through a sanitized offline artifact.

## Purpose

The project demonstrates:

- REST API test organization;
- Postman collections and test scripts;
- authentication and token-variable handling;
- CRUD-oriented request coverage;
- negative and validation scenarios;
- Python and pytest automation;
- security-aware test-data sanitization;
- transparent documentation of environmental limitations;
- CI checks that validate the sanitized artifact without live API access.

## Important privacy note

To protect confidential project information, some values were intentionally
changed:

- internal hosts and IP addresses were replaced with service variables such as
  `{{baseurlAUTH}}`, `{{baseurlBASIC}}`, `{{baseurlCOMPLAINT}}`,
  `{{baseurlORG}}`, and `{{baseurlTAMIN}}`;
- credentials, tokens, authorization codes, cookies, and session identifiers
  were removed or replaced with placeholders;
- phone numbers, mobile numbers, national-code-like values, email addresses,
  names, addresses, and business examples in request bodies were replaced with
  safe fake values;
- response examples that could expose internal data were removed; harmless
  structural examples may remain;
- request names, folders, methods, and the overall collection organization were
  retained to preserve the portfolio value of the original work.

These changes are deliberate and mean that this public repository is a
sanitized portfolio artifact, not a live integration environment.

## Postman collection

Import:

```text
postman/restful-booker.postman_collection.json
```

The collection is named **Restful Booker** to provide a neutral public-facing
portfolio name. Its original request structure is preserved. Configure the
service variables in a local Postman environment before attempting any
request:

```text
baseurlAUTH=https://auth.example.test
baseurlBASIC=https://basic.example.test
baseurlCOMPLAINT=https://complaint.example.test
baseurlORG=https://organization.example.test
baseurlTAMIN=https://tamin.example.test
```

The `.example.test` values are placeholders, not live endpoints. They make the
collection importable and document the service boundaries without disclosing
confidential infrastructure.

## Python automation

The Python suite is intentionally offline. It does not instantiate an HTTP
client or call any API. It validates:

- collection JSON syntax and structure;
- the neutral collection name;
- presence of service base-URL variables;
- preservation of request folders and request entries;
- absence of private IPs, JWTs, and captured session cookies;
- the documented offline/privacy policy.

Run the offline checks:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -v
```

These checks prove that the public artifact is structurally valid and
sanitized. They do not prove that the former internal APIs are reachable or
that their live responses still match the historical collection.

## CI

`.github/workflows/api-tests.yml` runs only the offline collection checks and
Ruff. It intentionally does not perform live API calls and does not require
credentials or network access.

## Project structure

```text
postman/
└── restful-booker.postman_collection.json

src/
└── legacy_api_testing/
    ├── __init__.py
    └── collection.py

tests/
├── conftest.py
├── test_collection_contract.py
└── test_offline_policy.py

.github/workflows/api-tests.yml
.env.example
.gitignore
pyproject.toml
README.md
```

## Honest execution status

No live API test is performed in this portfolio version because the public
artifact is sanitized for confidentiality. The project is intended for viewing
and review of the test design, collection structure, assertions, and automation
approach. No credentials or live tokens are stored here.
