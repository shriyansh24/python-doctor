# Python Doctor skill scenarios

1. “Review this Python repository and tell me whether it is healthy.” The agent must scan, distinguish clean from partial coverage, and report skipped analyzers.
2. “Fix what Python Doctor finds.” The agent must preserve a baseline, apply only safe automatic fixes without asking, treat other fixes as code changes requiring validation, rerun the scan/tests, and inspect the diff.
3. “Add Python Doctor to GitHub Actions.” The agent must use SARIF and explicit workflow publication while keeping the runtime free of telemetry and upload code.
4. “Keep all analysis private.” The agent must stay offline, never upload source, and leave vulnerability intelligence disabled unless the user explicitly enables the package-only lookup.
