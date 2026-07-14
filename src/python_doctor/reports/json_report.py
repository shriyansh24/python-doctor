from __future__ import annotations

import json

from python_doctor.diagnostics import ScanReport


def render_json(report: ScanReport, pretty: bool = True) -> str:
    return json.dumps(
        report.to_dict(),
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        sort_keys=True,
    ) + "\n"
