"""Offline checks that the Postman collection keeps its intended shape.

These tests never call the API. They guard the structure of the collection so
that a careless edit (a request without assertions, a hard-coded credential)
is caught in CI before the live Newman run.
"""

import re


def test_collection_is_organised_in_folders(collection):
    folders = [item["name"] for item in collection["item"]]

    assert folders == ["Authentication", "Booking workflow", "Negative testing"]


def test_expected_number_of_requests(requests_list):
    assert len(requests_list) == 11


def test_every_request_has_assertions(requests_list):
    for item in requests_list:
        scripts = [e for e in item.get("event", []) if e["listen"] == "test"]
        code = "\n".join(line for e in scripts for line in e["script"]["exec"])

        assert "pm.test(" in code, f"request without assertions: {item['name']}"


def test_assertion_count(collection_text):
    assert collection_text.count("pm.test(") >= 19


def test_crud_methods_are_covered(requests_list):
    methods = {item["request"]["method"] for item in requests_list}

    assert {"POST", "GET", "PUT", "PATCH", "DELETE"} <= methods


def test_negative_scenarios_are_present(requests_list):
    names = [item["name"].lower() for item in requests_list]

    assert sum("invalid" in name for name in names) >= 3


def test_requests_use_the_base_url_variable(requests_list):
    for item in requests_list:
        url = item["request"]["url"]
        raw = url["raw"] if isinstance(url, dict) else url

        assert raw.startswith("{{baseUrl}}"), item["name"]


def test_credentials_are_not_stored_in_the_collection(collection):
    values = {v["key"]: v["value"] for v in collection.get("variable", [])}

    assert values["username"] == ""
    assert values["password"] == ""
    assert values["token"] == ""


def test_no_tokens_or_session_cookies(collection_text):
    jwt = re.compile(r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b")

    assert not jwt.search(collection_text)
    assert "JSESSIONID" not in collection_text
