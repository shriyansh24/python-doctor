from __future__ import annotations

import ast
from pathlib import Path
from typing import List, Tuple, Union

from python_doctor import __version__
from python_doctor.diagnostics import (
    Diagnostic,
    FixSafety,
    RuleMaturity,
    Severity,
    SourceSpan,
)
from python_doctor.fingerprints import compute_fingerprint
from python_doctor.rules.base import RuleContext


FunctionNode = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class _RecursionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: List[FunctionNode] = []
        self.matches: List[Tuple[FunctionNode, ast.Call]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def _visit_function(self, node: FunctionNode) -> None:
        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_Call(self, node: ast.Call) -> None:
        if self.stack and isinstance(node.func, ast.Name) and node.func.id == self.stack[-1].name:
            self.matches.append((self.stack[-1], node))
        self.generic_visit(node)


class NoDirectRecursionRule:
    def analyze(
        self,
        path: Path,
        source: str,
        context: RuleContext,
    ) -> Tuple[Diagnostic, ...]:
        del context
        tree = ast.parse(source, filename=str(path))
        visitor = _RecursionVisitor()
        visitor.visit(tree)
        findings = []
        relative_path = path.as_posix()
        for function, call in visitor.matches:
            findings.append(
                Diagnostic(
                    fingerprint=compute_fingerprint(
                        relative_path,
                        "python-doctor/safety/no-direct-recursion",
                        "direct-recursion",
                        function.name,
                    ),
                    analyzer="python-doctor",
                    analyzer_version=__version__,
                    rule_id="python-doctor/safety/no-direct-recursion",
                    original_rule_id="no-direct-recursion",
                    title="Direct recursion",
                    message=f"Function '{function.name}' calls itself directly.",
                    rationale="Recursion prevents a static upper bound on stack use.",
                    remediation="Use an explicitly bounded iterative traversal.",
                    category="Reliability",
                    severity=Severity.ERROR,
                    confidence=1.0,
                    maturity=RuleMaturity.EXPERIMENTAL,
                    path=relative_path,
                    span=SourceSpan(
                        function.lineno,
                        function.col_offset + 1,
                        getattr(call, "end_lineno", call.lineno),
                        getattr(call, "end_col_offset", call.col_offset + 1) + 1,
                    ),
                    fix_safety=FixSafety.AGENT_REQUIRED,
                    root_cause_group=None,
                    tags=("safety-critical",),
                )
            )
        return tuple(findings)
