from __future__ import annotations

import re
from collections.abc import Iterable


SPEAKER_LABEL_PATTERN = re.compile(r"^\s*(Speaker\s+\d+)\s*:", re.IGNORECASE | re.MULTILINE)


def count_unique_speakers(contents: Iterable[str]) -> int:
    speakers = {
        label.lower()
        for content in contents
        for label in SPEAKER_LABEL_PATTERN.findall(content or "")
    }
    return len(speakers)
