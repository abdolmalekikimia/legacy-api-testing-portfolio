from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


COLLECTION_PATH = (
    Path(__file__).resolve().parents[2] / "postman" / "restful-booker.postman_collection.json"
)


def load_collection(path: Path = COLLECTION_PATH) -> dict[str, Any]:
    """Load the sanitized collection without making a network request."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def iter_requests(items: list[dict[str, Any]] | dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Yield every request while preserving the collection's folder structure."""
    if isinstance(items, dict):
        items = [items]
    for item in items:
        if not isinstance(item, dict):
            continue
        if "request" in item:
            yield item
        yield from iter_requests(item.get("item", []))
