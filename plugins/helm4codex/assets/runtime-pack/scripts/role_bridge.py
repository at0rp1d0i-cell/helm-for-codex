from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AGENT_TYPES = {"default", "worker", "explorer"}


def _load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected TOML table in {path}")
    return data


def _bridge_root(root: Path) -> Path:
    if (root / ".codex" / "config.toml").exists() and (root / ".codex" / "role_bridge.toml").exists():
        return root
    return ROOT


def configured_roles(root: Path) -> dict[str, str]:
    bridge_root = _bridge_root(root)
    config = _load_toml(bridge_root / ".codex" / "config.toml")
    roles = config.get("roles", {})
    if not isinstance(roles, dict):
        raise ValueError("Expected [roles] table in .codex/config.toml")
    normalized: dict[str, str] = {}
    for role, relpath in roles.items():
        normalized[str(role)] = str(relpath)
    return normalized


def bridge_entries(root: Path) -> dict[str, dict[str, str]]:
    bridge_root = _bridge_root(root)
    bridge = _load_toml(bridge_root / ".codex" / "role_bridge.toml")
    roles = bridge.get("roles", {})
    if not isinstance(roles, dict):
        raise ValueError("Expected [roles] table in .codex/role_bridge.toml")
    normalized: dict[str, dict[str, str]] = {}
    for role, entry in roles.items():
        if not isinstance(entry, dict):
            raise ValueError(f"Expected role table for {role} in role bridge")
        normalized[str(role)] = {str(key): str(value) for key, value in entry.items()}
    return normalized


def resolve_role(root: Path, role: str) -> dict[str, str]:
    bridge_root = _bridge_root(root)
    config_roles = configured_roles(root)
    bridge_roles = bridge_entries(root)
    if role not in config_roles:
        raise KeyError(f"Unknown configured role: {role}")
    if role not in bridge_roles:
        raise KeyError(f"Missing role bridge entry: {role}")

    bridge = bridge_roles[role]
    role_toml = bridge.get("role_toml", "")
    if role_toml != config_roles[role]:
        raise ValueError(
            f"Role bridge mismatch for {role}: {role_toml!r} != {config_roles[role]!r}",
        )

    agent_type = bridge.get("agent_type", "")
    if agent_type not in ALLOWED_AGENT_TYPES:
        raise ValueError(f"Unsupported bridge agent_type for {role}: {agent_type}")

    role_doc = _load_toml(bridge_root / ".codex" / role_toml)
    return {
        "logical_role": role,
        "display_name": str(role_doc.get("display_name", role)),
        "agent_type": agent_type,
        "model": bridge.get("model", ""),
        "reasoning_effort": bridge.get("reasoning_effort", ""),
        "role_toml": role_toml,
        "skill": str(role_doc.get("skill", "")),
        "metadata": str(role_doc.get("metadata", "")),
        "writeback_target": str(role_doc.get("writeback_target", "")),
        "writeback_command": str(role_doc.get("writeback_command", "")),
    }


def assert_sync(root: Path) -> None:
    config_roles = configured_roles(root)
    bridge_roles = bridge_entries(root)
    if set(config_roles) != set(bridge_roles):
        missing_from_bridge = sorted(set(config_roles) - set(bridge_roles))
        missing_from_config = sorted(set(bridge_roles) - set(config_roles))
        raise ValueError(
            "Role bridge mismatch: "
            f"missing_from_bridge={missing_from_bridge}, "
            f"missing_from_config={missing_from_config}",
        )

    for role in sorted(config_roles):
        resolve_role(root, role)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve canonical repo roles through the local bridge")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_roles = subparsers.add_parser("list", help="List bridge-resolved logical roles")
    list_roles.set_defaults(func=cmd_list)

    resolve = subparsers.add_parser("resolve", help="Resolve one logical role through the bridge")
    resolve.add_argument("role")
    resolve.set_defaults(func=cmd_resolve)

    sync = subparsers.add_parser("assert-sync", help="Validate that bridge entries match configured live roles")
    sync.set_defaults(func=cmd_assert_sync)

    return parser


def cmd_list(args: argparse.Namespace) -> int:
    payload = [resolve_role(args.root, role) for role in sorted(configured_roles(args.root))]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    print(json.dumps(resolve_role(args.root, args.role), indent=2, sort_keys=True))
    return 0


def cmd_assert_sync(args: argparse.Namespace) -> int:
    assert_sync(args.root)
    print("role bridge ok")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
