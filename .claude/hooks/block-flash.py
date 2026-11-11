#!/usr/bin/env python3
"""PreToolUse guard: block commands that flash or program firmware."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _payload import allow, deny, fail_closed, read_event, tool_call  # noqa: E402

FLASH_PATTERNS = [
    r"\bwest\s+flash\b",
    r"\bwest\s+build\b.*\s(-t|--target)\s+(flash|uf2)\b",
    r"\b(make|ninja)\s+flash\b",
    r"\bnrfjprog\b",
    r"\bnrfutil\b",
    r"\bdfu-util\b",
    r"\bpicotool\b",
    r"\bopenocd\b",
    r"\bpyocd\b",
    r"\bJLink(Exe)?\b",
    r"\b(cp|mv|ditto|rsync|dd)\b.*\.uf2\b",
]
COMPILED = [re.compile(pattern, re.IGNORECASE) for pattern in FLASH_PATTERNS]
SHELL_TOOLS = {"bash", "shell", "execute", "run_in_terminal", "powershell"}


def main():
    event = read_event()
    if event is None:
        fail_closed()
    name, args = tool_call(event)
    if name.lower() not in SHELL_TOOLS:
        allow()
    command = args.get("command")
    if not isinstance(command, str):
        deny("could not read the shell command; blocking by default")
    for pattern in COMPILED:
        if pattern.search(command):
            deny("Flashing or programming firmware is a manual step. Ask the owner to run it. See skill zmk-flash-runbook.")
    allow()


if __name__ == "__main__":
    main()
