from __future__ import annotations

from typing import Tuple

from python_doctor.rules.base import NativeRule
from python_doctor.rules.no_direct_recursion import NoDirectRecursionRule


def built_in_rules(profile: str) -> Tuple[NativeRule, ...]:
    if profile == "safety-critical":
        return (NoDirectRecursionRule(),)
    return ()
