import json
from pathlib import Path

import pytest

POSTMAN_DIR = Path(__file__).resolve().parents[1] / "postman"


def iter_requests(items):
    """Yield every request item, walking through nested folders."""
    for item in items:
        if "item" in item:
            yield from iter_requests(item["item"])
        else:
            yield item


@pytest.fixture(scope="session")
def collection():
    path = POSTMAN_DIR / "restful-booker-api.postman_collection.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def requests_list(collection):
    return list(iter_requests(collection["item"]))


@pytest.fixture(scope="session")
def collection_text(collection):
    return json.dumps(collection, ensure_ascii=False)
