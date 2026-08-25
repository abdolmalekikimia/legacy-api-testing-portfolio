import json
import re

from legacy_api_testing import iter_requests


PRIVATE_HOST = re.compile(
    r"(?i)(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d+\.\d+)"
)
JWT = re.compile(r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b")


def collection_text(collection) -> str:
    return json.dumps(collection, ensure_ascii=False)


def test_collection_name_and_structure(collection):
    assert collection["info"]["name"] == "Restful Booker"
    assert len(collection["item"]) == 5
    assert len(list(iter_requests(collection["item"]))) > 0


def test_service_base_url_variables_are_present(collection):
    variables = {item["key"] for item in collection.get("variable", [])}

    assert {
        "baseurlAUTH",
        "baseurlBASIC",
        "baseurlCOMPLAINT",
        "baseurlORG",
        "baseurlTAMIN",
    } <= variables


def test_sanitized_collection_has_no_private_hosts_or_tokens(collection):
    text = collection_text(collection)

    assert not PRIVATE_HOST.search(text)
    assert not JWT.search(text)
    assert "JSESSIONID=" not in text


def test_request_urls_use_service_variables(collection):
    requests = list(iter_requests(collection["item"]))

    assert requests
    raw_urls = []
    for item in requests:
        url = item["request"].get("url", "")
        raw_urls.append(url.get("raw", "") if isinstance(url, dict) else str(url))
    assert any("{{baseurlAUTH}}" in url for url in raw_urls)
    assert any("{{baseurlCOMPLAINT}}" in url for url in raw_urls)
