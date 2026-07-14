from __future__ import annotations

import hashlib
import re


_WHITESPACE = re.compile(r"\s+")


def compute_fingerprint(path: str, rule_id: str, message_key: str, evidence: str) -> str:
    normalized_path = path.replace("\\", "/").lstrip("./")
    normalized_evidence = _WHITESPACE.sub(" ", evidence).strip()
    canonical = "\x1f".join((normalized_path, rule_id, message_key, normalized_evidence))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
