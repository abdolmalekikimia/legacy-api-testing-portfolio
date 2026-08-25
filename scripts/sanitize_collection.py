"""Sanitize the preserved Postman collection without making network calls."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PRIVATE_HOST = re.compile(
    r"(?i)(?:https?://)?(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|"
    r"192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[0-1])\.\d+\.\d+)(?::\d+)?"
)
JWT = re.compile(r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b")


def service_for(url: str) -> str:
    value = url.lower()
    if "/auth" in value or ":60001" in value or ":8686" in value or "sso." in value:
        return "{{baseurlAUTH}}"
    if "/basic" in value or ":8680" in value or ":60002" in value:
        return "{{baseurlBASIC}}"
    if "/organization" in value or ":60003" in value:
        return "{{baseurlORG}}"
    if "/tamin" in value or ":8081" in value:
        return "{{baseurlTAMIN}}"
    return "{{baseurlCOMPLAINT}}"


def clean_string(value: str, key: str, service: str) -> str:
    if re.search(r"(?i)(mobile|cell)", key):
        return "09100000000"
    if re.search(r"(?i)(phone|telephone|fax)", key):
        return "02100000000"
    if re.search(r"(?i)(national|certificate|foreigner)", key):
        return "0000000000"
    if re.search(r"(?i)email", key):
        return "fake.user@example.test"
    if re.search(r"(?i)password", key):
        return "{{password}}"
    if re.search(r"(?i)username", key):
        return "{{username}}"
    if re.search(r"(?i)(token|cookie|session)", key):
        return "{{token}}"

    value = PRIVATE_HOST.sub(service, value)
    value = re.sub(r"(?i)https?://[^/\s\"]*\.mcls\.gov\.ir", service, value)
    value = JWT.sub("{{token}}", value)
    value = re.sub(r"(?i)(?:JSESSIONID|sessionid)=[^;\s\"]+", "session={{session_cookie}}", value)
    value = re.sub(r"(?i)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", "fake.user@example.test", value)
    value = re.sub(r"(?<!\d)09\d{9}(?!\d)", "09100000000", value)
    value = re.sub(r"(?<!\d)0\d{10}(?!\d)", "02100000000", value)
    return value


def sanitize(value: Any, key: str = "", service: str = "{{baseurlCOMPLAINT}}") -> Any:
    if isinstance(value, dict):
        local_service = service
        url = value.get("url")
        if isinstance(url, dict):
            local_service = service_for(str(url.get("raw", "")))
        result: dict[str, Any] = {}
        for child_key, child_value in value.items():
            if child_key == "response":
                continue
            if child_key == "host":
                result[child_key] = local_service
            elif child_key == "port":
                result[child_key] = ""
            else:
                result[child_key] = sanitize(child_value, child_key, local_service)
        return result
    if isinstance(value, list):
        return [sanitize(item, key, service) for item in value]
    if not isinstance(value, str):
        return value
    if key == "raw" and value.lstrip().startswith(("{", "[")):
        try:
            embedded = json.loads(value)
            return json.dumps(sanitize(embedded, key, service), ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    return clean_string(value, key, service)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "postman" / "restful-booker.postman_collection.json"
    collection = json.loads(path.read_text(encoding="utf-8-sig"))
    collection.setdefault("info", {})["name"] = "Restful Booker"
    collection["variable"] = [
        {"key": "baseurlAUTH", "value": "https://auth.example.test", "type": "string"},
        {"key": "baseurlBASIC", "value": "https://basic.example.test", "type": "string"},
        {"key": "baseurlCOMPLAINT", "value": "https://complaint.example.test", "type": "string"},
        {"key": "baseurlORG", "value": "https://organization.example.test", "type": "string"},
        {"key": "baseurlTAMIN", "value": "https://tamin.example.test", "type": "string"},
        {"key": "token", "value": "", "type": "string"},
    ]
    path.write_text(json.dumps(sanitize(collection), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
