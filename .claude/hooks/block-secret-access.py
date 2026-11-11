#!/usr/bin/env python3
"""PreToolUse guard: block reads, edits, and shell use of secret-looking files."""
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _payload import allow, deny, fail_closed, read_event, tool_call  # noqa: E402

SECRET_PATTERNS = [
    r"(^|/)\.env(\.[^/]+)?$",
    r"(^|/)\.envrc$",
    r"\.(pem|key|p12|pfx|jks|keystore)$",
    r"(^|/)id_(rsa|ed25519|ecdsa|dsa)(\.pub)?$",
    r"(^|/)\.netrc$",
    r"(^|/)\.git-credentials$",
    r"(^|/)\.aws/credentials$",
    r"(^|/)secrets?\.(ya?ml|json|toml)$",
]
SECRET_RE = [re.compile(pattern, re.IGNORECASE) for pattern in SECRET_PATTERNS]
PATH_KEYS = ("file_path", "path", "notebook_path")


def is_secret(path):
    return any(regex.search(path.replace("\\", "/")) for regex in SECRET_RE)


def main():
    event = read_event()
    if event is None:
        fail_closed()
    name, args = tool_call(event)
    candidates = [args[key] for key in PATH_KEYS if isinstance(args.get(key), str)]
    if name.lower() == "glob" and isinstance(args.get("pattern"), str):
        candidates.append(args["pattern"])
    command = args.get("command")
    if isinstance(command, str):
        try:
            candidates.extend(shlex.split(command))
        except ValueError:
            deny("could not parse the shell command to check for secret paths")
    for candidate in candidates:
        if is_secret(candidate):
            deny(f"Secret-looking path blocked: {candidate}. Ask the owner to supply the value outside this session.")
    allow()


if __name__ == "__main__":
    main()
