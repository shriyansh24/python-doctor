from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.9/3.10 compatibility
    import tomli as tomllib  # type: ignore[no-redef]


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class NetworkConfig:
    vulnerability_intelligence: bool = False


@dataclass(frozen=True)
class AdapterConfig:
    enabled: bool = True
    required: bool = False
    executable: str = ""


@dataclass(frozen=True)
class AdaptersConfig:
    ruff: AdapterConfig = AdapterConfig(executable="ruff")
    bandit: AdapterConfig = AdapterConfig(executable="bandit")
    radon: AdapterConfig = AdapterConfig(executable="radon")


@dataclass(frozen=True)
class DoctorConfig:
    profile: str = "default"
    network: NetworkConfig = NetworkConfig()
    adapters: AdaptersConfig = AdaptersConfig()
    rules: Tuple[Tuple[str, str], ...] = ()
    categories: Tuple[Tuple[str, str], ...] = ()
    ignore_rules: Tuple[str, ...] = ()
    ignore_files: Tuple[str, ...] = ()
    blocking: str = "error"
    require_complete: bool = False


_PROHIBITED_KEYS = {"telemetry", "analytics", "crash_reporting", "remote_scoring"}
_PROFILES = {"default", "strict", "safety-critical"}
_SEVERITIES = {"off", "info", "warning", "error"}
_BLOCKING_LEVELS = {"none", "warning", "error"}


def _reject_prohibited_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _PROHIBITED_KEYS:
                raise ConfigError(f"{normalized} is not supported by Python Doctor")
            _reject_prohibited_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_prohibited_keys(nested)


def _read_toml(path: Path) -> Dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _string_mapping(value: Any, name: str) -> Tuple[Tuple[str, str], ...]:
    if not isinstance(value, dict):
        raise ConfigError(f"{name} must be a table")
    result = []
    for key, severity in value.items():
        if not isinstance(key, str) or not isinstance(severity, str):
            raise ConfigError(f"{name} entries must map strings to severities")
        if severity not in _SEVERITIES:
            raise ConfigError(f"invalid severity for {name}.{key}: {severity}")
        result.append((key, severity))
    return tuple(sorted(result))


def _string_tuple(value: Any, name: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ConfigError(f"{name} must be a list of strings")
    return tuple(value)


def _adapter_config(raw: Dict[str, Any], name: str) -> AdapterConfig:
    value = raw.get(name, {})
    if not isinstance(value, dict):
        raise ConfigError(f"adapters.{name} must be a table")
    enabled = value.get("enabled", True)
    required = value.get("required", False)
    executable = value.get("executable", name)
    if not isinstance(enabled, bool):
        raise ConfigError(f"adapters.{name}.enabled must be a boolean")
    if not isinstance(required, bool):
        raise ConfigError(f"adapters.{name}.required must be a boolean")
    if not isinstance(executable, str) or not executable:
        raise ConfigError(f"adapters.{name}.executable must be a non-empty string")
    if required and not enabled:
        raise ConfigError(f"adapters.{name} cannot be required and disabled")
    return AdapterConfig(enabled, required, executable)


def load_config(project_root: Path) -> DoctorConfig:
    standalone = project_root / "python-doctor.toml"
    pyproject = project_root / "pyproject.toml"
    if standalone.exists():
        raw = _read_toml(standalone)
    elif pyproject.exists():
        raw = _read_toml(pyproject).get("tool", {}).get("python-doctor", {})
    else:
        raw = {}
    _reject_prohibited_keys(raw)
    profile = str(raw.get("profile", "default"))
    if profile not in _PROFILES:
        raise ConfigError(f"unknown profile: {profile}")
    network = raw.get("network", {})
    if not isinstance(network, dict):
        raise ConfigError("network must be a table")
    vulnerability_intelligence = network.get("vulnerability_intelligence", False)
    if not isinstance(vulnerability_intelligence, bool):
        raise ConfigError("network.vulnerability_intelligence must be a boolean")
    adapters = raw.get("adapters", {})
    if not isinstance(adapters, dict):
        raise ConfigError("adapters must be a table")
    ignore = raw.get("ignore", {})
    if not isinstance(ignore, dict):
        raise ConfigError("ignore must be a table")
    ci = raw.get("ci", {})
    if not isinstance(ci, dict):
        raise ConfigError("ci must be a table")
    blocking = ci.get("blocking", "error")
    if not isinstance(blocking, str) or blocking not in _BLOCKING_LEVELS:
        raise ConfigError(f"invalid ci.blocking value: {blocking}")
    require_complete = ci.get("require_complete", False)
    if not isinstance(require_complete, bool):
        raise ConfigError("ci.require_complete must be a boolean")
    return DoctorConfig(
        profile=profile,
        network=NetworkConfig(vulnerability_intelligence=vulnerability_intelligence),
        adapters=AdaptersConfig(
            ruff=_adapter_config(adapters, "ruff"),
            bandit=_adapter_config(adapters, "bandit"),
            radon=_adapter_config(adapters, "radon"),
        ),
        rules=_string_mapping(raw.get("rules", {}), "rules"),
        categories=_string_mapping(raw.get("categories", {}), "categories"),
        ignore_rules=_string_tuple(ignore.get("rules", []), "ignore.rules"),
        ignore_files=_string_tuple(ignore.get("files", []), "ignore.files"),
        blocking=blocking,
        require_complete=require_complete,
    )
