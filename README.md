# legacy-api-testing-portfolio

Postman / Newman API tests for the public Restful Booker service.

[![API tests](https://github.com/abdolmalekikimia/legacy-api-testing-portfolio/actions/workflows/api-tests.yml/badge.svg)](https://github.com/abdolmalekikimia/legacy-api-testing-portfolio/actions/workflows/api-tests.yml)

A Postman collection with 11 requests and 19 assertions for the public
[Restful Booker](https://restful-booker.herokuapp.com/apidoc/index.html) practice API. It covers
authentication, the full create / read / update / delete workflow and negative cases, and it runs
automatically with Newman in GitHub Actions.

## Who did what

I am a QA engineer whose main work is API testing with Postman. **This collection and the
Python checks in `tests/` were generated with AI assistance.** My part was choosing the scenarios
(positive and negative), reviewing the requests and assertions, running the collection and checking
the results. This repository is a small QA showcase; it is not evidence of independent
software-engineering work.

## What the collection covers

| Folder | Requests | What is checked |
|---|---|---|
| Authentication | Authenticate, Invalid credentials | Token is returned for valid credentials; bad credentials return the "Bad credentials" reason |
| Booking workflow | Create booking, Get booking IDs, Get booking, Update booking, Partial update booking, Delete booking, Verify deletion | Status codes, response fields, that updates are returned and persisted, `201` on delete, `404` afterwards |
| Negative testing | Invalid booking ID, Invalid booking payload | Unknown IDs return `404`; an empty payload is rejected with an error status (the demo service answers `500`, a quirk worth reporting in a real project) |

Requests are chained: the token and the booking ID returned by earlier requests are stored in
collection variables and reused by later ones. Test data is generated with Postman dynamic
variables.

## Run it

Newman (the Postman command-line runner) needs Node.js:

```bash
npm install --global newman
newman run postman/restful-booker-api.postman_collection.json \
  -e postman/restful-booker.postman_environment.json
```

The environment file holds the demo credentials (`admin` / `password123`) that the Restful Booker
documentation publishes for everyone. The collection itself stores no credentials. You can also
import both files into Postman and run the collection with the Collection Runner.

## Continuous integration

`.github/workflows/api-tests.yml` runs two jobs on every push, on pull requests and weekly:

1. **Collection structure (offline).** `ruff` and `pytest` check that the collection keeps its shape:
   three folders, 11 requests, an assertion in every request, all CRUD methods, at least three
   negative scenarios, only the `{{baseUrl}}` variable in URLs and no stored credentials or tokens.
   These tests never call the API.
2. **Newman against the public service.** The real collection run, with a JUnit report uploaded as
   an artifact.

## What this does and does not show

- It shows how I organise API tests, chain requests and write assertions with AI help.
- Restful Booker is a shared practice service. It can be slow, reset its data or be unavailable,
  so the live job can fail for reasons unrelated to the tests.
- The collection tests a demo booking API. It is not a test of any company system.
- Earlier versions of this repository (see the commit history) contained a sanitized collection from a
  former workplace. It was provided by that project's backend team and is not my work, so it has been
  removed.
