from __future__ import annotations

import argparse
import json
from pathlib import Path

from role_bridge import resolve_role
from team_state import cmd_execution_receipt


ROOT = Path(__file__).resolve().parents[1]


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _resolve_path(root: Path, path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def _extract_section(content: str, heading: str) -> str:
    marker = f"## {heading}\n\n"
    start = content.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_header = content.find("\n## ", start)
    if next_header == -1:
        return content[start:].strip()
    return content[start:next_header].strip()


def _extract_list_section(content: str, heading: str) -> list[str]:
    section = _extract_section(content, heading)
    if not section:
        return []
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if value:
            items.append(value)
    return items


def _extract_key_value_section(content: str, heading: str) -> dict[str, str]:
    section = _extract_section(content, heading)
    values: dict[str, str] = {}
    for item in _extract_list_section(f"## {heading}\n\n{section}", heading):
        if ":" not in item:
            continue
        key, raw_value = item.split(":", 1)
        values[key.strip()] = raw_value.strip()
    return values


def _default_launch_output(packet_path: str) -> str:
    packet = Path(packet_path)
    if packet.parent.name.endswith("packets"):
        return str(packet.parent.parent / "bridge-launches" / f"{packet.stem}.json")
    return str(packet.with_name(f"{packet.stem}-launch.json"))


def _default_receipt_output(packet_path: str) -> str:
    packet = Path(packet_path)
    if packet.parent.name.endswith("packets"):
        return str(packet.parent.parent / "execution-receipts" / packet.name)
    return str(packet.with_name(f"{packet.stem}-receipt{packet.suffix or '.md'}"))


def _derive_default_invocation_spec(packet_path: str) -> str:
    packet = Path(packet_path)
    if packet.parent.name.endswith("packets"):
        return str(packet.parent.parent / "invocation-specs" / packet.name)
    return str(packet.with_name(f"{packet.stem}-invocation{packet.suffix or '.md'}"))


def _parse_packet(root: Path, packet_path: str) -> dict[str, object]:
    packet = _resolve_path(root, packet_path)
    content = _read(packet)
    if not content:
        raise FileNotFoundError(f"Missing packet: {packet}")

    runtime_binding = _extract_key_value_section(content, "Runtime Role Binding")
    writeback_command = _extract_section(content, "Writeback Command") or _extract_section(
        content,
        "Completion Command",
    )

    consumed_artifacts = _extract_list_section(content, "Consumed Artifacts")
    canonical_sources = _extract_list_section(content, "Canonical Sources")
    plan_brief = _extract_section(content, "Plan Brief")
    if canonical_sources:
        consumed_artifacts = [*consumed_artifacts, *canonical_sources]
    if plan_brief:
        consumed_artifacts.append(plan_brief)

    return {
        "path": str(packet),
        "role": _extract_section(content, "Role"),
        "logical_role": _extract_section(content, "Logical Role"),
        "bridge": _extract_key_value_section(content, "Invocation Bridge"),
        "runtime_binding": runtime_binding,
        "writeback_target": _extract_section(content, "Writeback Target"),
        "writeback_command": writeback_command,
        "consumed_artifacts": consumed_artifacts,
    }


def _parse_invocation_spec(root: Path, invocation_spec_path: str) -> dict[str, object]:
    spec_path = _resolve_path(root, invocation_spec_path)
    content = _read(spec_path)
    if not content:
        raise FileNotFoundError(f"Missing invocation spec: {spec_path}")

    return {
        "path": str(spec_path),
        "role": _extract_section(content, "Role"),
        "logical_role": _extract_section(content, "Logical Role"),
        "source_packet": _extract_section(content, "Source Packet"),
        "bridge": _extract_key_value_section(content, "Invocation Bridge"),
        "runtime_skill": _extract_section(content, "Runtime Skill"),
        "metadata": _extract_section(content, "Role Metadata"),
        "consumed_artifacts": _extract_list_section(content, "Consumed Artifacts"),
        "expected_writeback_target": _extract_section(content, "Expected Writeback Target"),
        "expected_writeback_command": _extract_section(content, "Expected Writeback Command"),
    }


def _require_equal(label: str, actual: str, expected: str) -> None:
    if actual != expected:
        raise ValueError(f"{label} mismatch: {actual!r} != {expected!r}")


def _require_in(label: str, actual: str, expected_values: list[str]) -> None:
    if actual not in expected_values:
        raise ValueError(f"{label} mismatch: {actual!r} not in {expected_values!r}")


def _matches_expanded_writeback_command(actual: str, expected_target: str) -> bool:
    return actual.startswith("uv run python ") and expected_target in actual


def build_launch_payload(root: Path, packet_path: str, invocation_spec_path: str) -> dict[str, object]:
    packet = _parse_packet(root, packet_path)
    spec = _parse_invocation_spec(root, invocation_spec_path)
    logical_role = str(spec["logical_role"])
    resolved_role = resolve_role(root, logical_role)

    _require_equal("Packet logical role", str(packet["logical_role"]), logical_role)
    _require_equal("Invocation spec role", str(spec["role"]), resolved_role["display_name"])
    _require_equal("Packet role", str(packet["role"]), resolved_role["display_name"])
    _require_equal(
        "Invocation spec source packet",
        str(_resolve_path(root, str(spec["source_packet"]))),
        str(_resolve_path(root, packet_path)),
    )

    packet_bridge = packet["bridge"]
    spec_bridge = spec["bridge"]
    for key, expected in {
        "agent_type": resolved_role["agent_type"],
        "model": resolved_role["model"],
        "reasoning_effort": resolved_role["reasoning_effort"],
    }.items():
        _require_equal(f"Packet bridge {key}", str(packet_bridge.get(key, "")), expected)
        _require_equal(f"Invocation spec bridge {key}", str(spec_bridge.get(key, "")), expected)

    runtime_binding = packet["runtime_binding"]
    _require_equal("Runtime skill", str(spec["runtime_skill"]), resolved_role["skill"])
    _require_equal("Role metadata", str(spec["metadata"]), resolved_role["metadata"])
    _require_equal(
        "Packet runtime skill",
        str(runtime_binding.get("skill", "")),
        resolved_role["skill"],
    )
    _require_equal(
        "Packet runtime metadata",
        str(runtime_binding.get("metadata", "")),
        resolved_role["metadata"],
    )
    _require_in(
        "Packet canonical writeback target",
        str(runtime_binding.get("canonical_writeback_target", "")),
        [resolved_role["writeback_target"], str(packet["writeback_target"])],
    )
    runtime_binding_command = str(runtime_binding.get("canonical_writeback_command", ""))
    if runtime_binding_command != resolved_role["writeback_command"] and not _matches_expanded_writeback_command(
        runtime_binding_command,
        str(packet["writeback_target"]),
    ):
        raise ValueError(
            "Packet canonical writeback command mismatch: "
            f"{runtime_binding_command!r}",
        )
    _require_equal(
        "Expected writeback target",
        str(spec["expected_writeback_target"]),
        str(packet["writeback_target"]),
    )
    _require_equal(
        "Expected writeback command",
        str(spec["expected_writeback_command"]),
        str(packet["writeback_command"]),
    )

    packet_consumed = [str(_resolve_path(root, item)) for item in packet["consumed_artifacts"]]
    spec_consumed = [str(_resolve_path(root, item)) for item in spec["consumed_artifacts"]]
    packet_path_resolved = str(_resolve_path(root, packet_path))
    if packet_path_resolved not in spec_consumed:
        raise ValueError("Invocation spec must consume the source packet itself.")
    for item in packet_consumed:
        if item not in spec_consumed:
            raise ValueError(f"Invocation spec is missing consumed artifact: {item}")

    launch_message = (
        f"You are the repo-defined role \"{resolved_role['display_name']}\" "
        f"({resolved_role['logical_role']}).\n\n"
        f"Use runtime skill: {resolved_role['skill']}\n"
        f"Use role metadata: {resolved_role['metadata']}\n"
        f"Consume source packet: {packet_path}\n"
        f"Consume invocation spec: {invocation_spec_path}\n"
        "Treat Ops as the dispatch owner; do not redefine the task from chat history.\n"
        f"Write back exactly to: {spec['expected_writeback_target']}\n"
        f"Expected writeback command: {spec['expected_writeback_command']}\n"
        "After writeback, return a concise completion note to Ops."
    )

    return {
        "role": resolved_role["display_name"],
        "logical_role": resolved_role["logical_role"],
        "agent_type": resolved_role["agent_type"],
        "model": resolved_role["model"],
        "reasoning_effort": resolved_role["reasoning_effort"],
        "runtime_skill": resolved_role["skill"],
        "metadata": resolved_role["metadata"],
        "packet_path": packet_path,
        "invocation_spec_path": invocation_spec_path,
        "consumed_artifacts": spec["consumed_artifacts"],
        "expected_writeback_target": spec["expected_writeback_target"],
        "expected_writeback_command": spec["expected_writeback_command"],
        "launch_message": launch_message,
    }


def _load_launch_payload(root: Path, launch_payload_path: str) -> dict[str, object]:
    payload_path = _resolve_path(root, launch_payload_path)
    content = _read(payload_path)
    if not content:
        raise FileNotFoundError(f"Missing launch payload: {payload_path}")
    data = json.loads(content)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object payload in {payload_path}")
    normalized: dict[str, object] = {}
    for key, value in data.items():
        normalized[str(key)] = value
    return normalized


def cmd_assert_pair(args: argparse.Namespace) -> int:
    build_launch_payload(
        args.root,
        args.packet_path,
        args.invocation_spec_path or _derive_default_invocation_spec(args.packet_path),
    )
    print("bridge pair ok")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    payload = build_launch_payload(
        args.root,
        args.packet_path,
        args.invocation_spec_path or _derive_default_invocation_spec(args.packet_path),
    )
    output = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        out = _resolve_path(args.root, args.output)
        _write(out, output + "\n")
        print(f"wrote {out}")
        return 0
    print(output)
    return 0


def cmd_receipt(args: argparse.Namespace) -> int:
    invocation_spec_path = args.invocation_spec_path or _derive_default_invocation_spec(args.packet_path)
    payload = build_launch_payload(args.root, args.packet_path, invocation_spec_path)
    launch_payload_path = args.launch_payload_path or _default_launch_output(args.packet_path)
    if args.launch_payload_path:
        persisted_payload = _load_launch_payload(args.root, args.launch_payload_path)
        for key in [
            "logical_role",
            "agent_type",
            "model",
            "reasoning_effort",
            "runtime_skill",
            "metadata",
            "packet_path",
            "invocation_spec_path",
            "expected_writeback_target",
            "expected_writeback_command",
        ]:
            _require_equal(
                f"Launch payload {key}",
                str(persisted_payload.get(key, "")),
                str(payload.get(key, "")),
            )

    receipt_args = argparse.Namespace(
        root=args.root,
        output=args.output or _default_receipt_output(args.packet_path),
        title=args.title or f"{payload['role']} execution receipt",
        role=str(payload["role"]),
        logical_role=str(payload["logical_role"]),
        source_packet=args.packet_path,
        invocation_spec=invocation_spec_path,
        launch_payload=launch_payload_path,
        execution_status=args.execution_status,
        expected_writeback_target=str(payload["expected_writeback_target"]),
        writeback_status=args.writeback_status,
        specialist_note=args.specialist_note,
        follow_up=args.follow_up,
    )
    return cmd_execution_receipt(receipt_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile repo-backed role packets into a last-hop launch payload")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    assert_pair = subparsers.add_parser(
        "assert-pair",
        help="Validate that a packet and invocation spec form a bridge-consistent pair",
    )
    assert_pair.add_argument("--packet-path", required=True, dest="packet_path")
    assert_pair.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    assert_pair.set_defaults(func=cmd_assert_pair)

    render = subparsers.add_parser(
        "render",
        help="Render a reusable last-hop launch payload from a packet plus invocation spec",
    )
    render.add_argument("--packet-path", required=True, dest="packet_path")
    render.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    render.add_argument("--output")
    render.set_defaults(func=cmd_render)

    receipt = subparsers.add_parser(
        "receipt",
        help="Record a repo-backed execution receipt for a launch compiled through the bridge runner",
    )
    receipt.add_argument("--packet-path", required=True, dest="packet_path")
    receipt.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    receipt.add_argument("--launch-payload-path", dest="launch_payload_path")
    receipt.add_argument("--output")
    receipt.add_argument("--title")
    receipt.add_argument("--execution-status", required=True, dest="execution_status")
    receipt.add_argument("--writeback-status", required=True, dest="writeback_status")
    receipt.add_argument("--specialist-note", required=True, dest="specialist_note")
    receipt.add_argument("--follow-up", action="append", default=[], dest="follow_up")
    receipt.set_defaults(func=cmd_receipt)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
