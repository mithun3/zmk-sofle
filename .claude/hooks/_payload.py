"""Shared helpers for PreToolUse guard hooks. Standard library only."""
import json
import sys


def read_event():
    """Return the hook event as a dict, or None when stdin is not a JSON object."""
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def tool_call(event):
    """Return (tool name, tool input) for Claude Code and Copilot payload shapes."""
    name = str(event.get("tool_name") or event.get("toolName") or "")
    args = event.get("tool_input", event.get("toolArgs", {}))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            args = {"command": args}
    return name, (args if isinstance(args, dict) else {})


def allow():
    sys.stdout.write("{}\n")
    sys.exit(0)


def deny(reason):
    decision = {"permissionDecision": "deny", "permissionDecisionReason": reason}
    body = {"hookSpecificOutput": {"hookEventName": "PreToolUse", **decision}, **decision}
    sys.stdout.write(json.dumps(body) + "\n")
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def fail_closed():
    deny("hook input was not a JSON object; blocking by default")
