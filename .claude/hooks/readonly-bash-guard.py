#!/usr/bin/env python3
"""PreToolUse guard for read-only agents: allow only read-only shell commands."""
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _payload import allow, deny, fail_closed, read_event, tool_call  # noqa: E402

SIMPLE_PROGRAMS = {"ls", "cat", "head", "tail", "grep", "rg", "wc", "file", "stat", "pwd", "sort", "uniq", "cut", "diff", "tree"}
GIT_SUBCOMMANDS = {"status", "log", "diff", "show", "blame", "ls-files", "rev-parse", "describe", "shortlog", "grep"}
WEST_SUBCOMMANDS = {"list", "topdir"}
FIND_ACTIONS = {"-exec", "-execdir", "-ok", "-okdir", "-delete", "-fprint", "-fprint0", "-fprintf", "-fls"}
CHAIN = re.compile(r"[;&<>`\n\r]|\$\(")


def segment_reason(tokens):
    if not tokens:
        return "empty command segment"
    program, args = tokens[0], tokens[1:]
    if "/" in program:
        return f"path-qualified program '{program}' is not allowed"
    if any(arg.startswith("--output") for arg in args) or (program in {"sort", "tree"} and "-o" in args):
        return "output flags can write files"
    if program == "find":
        bad = [arg for arg in args if arg in FIND_ACTIONS]
        return f"find action '{bad[0]}' changes files" if bad else None
    if program == "git":
        if not args or args[0] not in GIT_SUBCOMMANDS:
            return f"git subcommand '{args[0] if args else ''}' is not on the read-only list"
        return None
    if program == "west":
        if not args or args[0] not in WEST_SUBCOMMANDS:
            return "west subcommand is not on the read-only list"
        return None
    if program in SIMPLE_PROGRAMS:
        return None
    return f"'{program}' is not on the read-only list"


def check_command(command):
    if not isinstance(command, str) or not command.strip():
        return "empty or non-text command"
    if CHAIN.search(command):
        return "chaining, redirects, background jobs, and command substitution are not allowed"
    for segment in command.split("|"):
        try:
            tokens = shlex.split(segment)
        except ValueError as exc:
            return f"could not parse command: {exc}"
        reason = segment_reason(tokens)
        if reason:
            return reason
    return None


def main():
    event = read_event()
    if event is None:
        fail_closed()
    _, args = tool_call(event)
    if "command" not in args:
        allow()
    reason = check_command(args.get("command"))
    if reason:
        deny(f"Read-only agent blocked this command: {reason}. Use Read, Grep, or Glob, or ask the owner to run it.")
    allow()


if __name__ == "__main__":
    main()
