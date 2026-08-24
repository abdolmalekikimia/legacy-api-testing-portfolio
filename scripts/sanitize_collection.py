"""Remove private infrastructure and personal/test data from a Postman collection."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


PRIVATE_HOST = re.compile(
    r"(?:(?:https?://)?(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|"
    r"192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[0-1])\.\d+\.\d+))(?::\d+)?"
)
JWT = re.compile(r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE = re.compile(r"(?<!\d)(?:\+98|0098|0)?9\d{9}(?!\d)")
NATIONAL_CODE = re.compile(r"(?<!\d)\d{10}(?!\d)")


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if not isinstance(value, str):
        return value

    value = PRIVATE_HOST.sub("{{base_url}}", value)
    value = JWT.sub("{{api_token}}", value)
    value = EMAIL.sub("demo@example.test", value)
    value = PHONE.sub("09120000000", value)
    value = NATIONAL_CODE.sub("0000000000", value)
    value = re.sub(r'"password"\s*:\s*"[^"]*"', '"password": "{{password}}"', value, flags=re.I)
    value = re.sub(r'password=[^&"]+', 'password={{password}}', value, flags=re.I)
    value = re.sub(r'username=(?:real_user|pedram|chief_officer)', 'username={{username}}', value, flags=re.I)
    value = re.sub(
        r'"authorizationCode"\s*=\s*[^&"]+',
        '"authorizationCode={{authorization_code}}',
        value,
        flags=re.I,
    )
    return value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/sanitize_collection.py COLLECTION.json", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    destination = Path("postman/complaint-test.sanitized.json")
    data = json.loads(source.read_text(encoding="utf-8-sig"))
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(
        json.dumps(sanitize(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
