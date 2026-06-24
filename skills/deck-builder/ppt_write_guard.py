#!/usr/bin/env python3
"""
ppt_write_guard.py — Deck Builder guardrail hook.

Wired in as a Claude Code PreToolUse hook by install.py. Fires when Claude tries
to call a ppt-mcp *write* tool (ppt_set_text / ppt_set_placeholder_text /
ppt_find_replace_text). Those tools flatten a shape's mixed formatting into one
style — a bold header over bullets comes out all one look, with no clean undo.

This hook DENIES the call with a reason that reroutes Claude to deck_writer.py,
which writes the careful way (capture format, insert text, re-stamp format).

Reads the PreToolUse event JSON on stdin (ignored) and emits a deny decision.
"""
import sys
import json

# Read and discard the event payload (avoids a broken pipe; we don't need it).
try:
    json.load(sys.stdin)
except Exception:
    pass

reason = (
    "Newry Deck Builder guardrail: this ppt-mcp write tool flattens a shape's "
    "mixed formatting into one style (a bold header over bullets all become one "
    "look, with no clean undo). Do not use it to change slide content. Use "
    "deck_writer.py instead: edit_text_preserve to change words and keep "
    "formatting, write_textbox / write_table to set new formatting, or build to "
    "make a new slide. The ppt-mcp tools are for reading only (preview, profile, "
    "get_text, list_shapes)."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason
    }
}))
