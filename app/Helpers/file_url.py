from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from django.conf import settings


def build_file_url(request, file_path: str | None) -> str:
    if not file_path:
        return ""

    parsed = urlparse(file_path)
    if parsed.scheme and parsed.netloc:
        return file_path

    media_path = f"{settings.MEDIA_URL.rstrip('/')}/{str(file_path).lstrip('/')}"
    return request.build_absolute_uri(media_path)


def add_file_urls(request, data: Any) -> Any:
    if isinstance(data, list):
        return [add_file_urls(request, item) for item in data]

    if not isinstance(data, dict):
        return data

    enriched = {
        key: add_file_urls(request, value)
        for key, value in data.items()
    }
    if "file_path" in enriched:
        enriched["file_url"] = build_file_url(request, enriched.get("file_path"))
    return enriched
