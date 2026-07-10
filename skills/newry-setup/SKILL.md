---
name: newry-setup
description: One-time setup for a Newry contractor machine. Installs the contractor working floor (CLAUDE.md) and the brevity/plain-language UserPromptSubmit hook, and fixes the local Python path. Trigger - "run newry-setup", "set up this machine", "install the contractor floor", "set up brevity here".
---

# Newry contractor machine setup

Goal: get a fresh Claude Code machine to Sylvan's preferred behavior — short/plain
replies, execute-don't-ask, clean work/personal boundary — with two artifacts:
a global `CLAUDE.md` and a `UserPromptSubmit` brevity hook. One-time. Idempotent —
re-running should not duplicate anything.

Work in plain language. Report each step in one line. Do NOT ask for confirmation
between steps — just do them and report at the end. Only stop if a step genuinely
can't be completed (e.g. no Python found and can't install).

## Steps

1. **Find the Claude config dir.** It is `~/.claude/` (i.e. `C:\Users\<user>\.claude\`
   on Windows). Create it if missing.

2. **Find the Python interpreter for the hook.** Run `where pythonw` then `where python`.
   Prefer `pythonw` (no console flash). Record the full path (or just `pythonw` /
   `python` if it resolves on PATH). If neither exists, stop and tell Sylvan to
   install Python from python.org, then resume.

3. **Install the working floor.** Copy this skill's `assets/CLAUDE.md` to
   `~/.claude/CLAUDE.md`. If a `CLAUDE.md` already exists there, show Sylvan a short
   diff summary and ask before overwriting (this is the one place to pause).

4. **Install the brevity hook** into `~/.claude/settings.json`:
   - If the file doesn't exist, create it from `assets/hook-snippet.json`.
   - If it exists, parse it as JSON and MERGE: add the `UserPromptSubmit` entry from
     `assets/hook-snippet.json` into `hooks.UserPromptSubmit` (create the arrays if
     absent). Do not clobber existing hooks or other settings.
   - If a UserPromptSubmit hook with the same brevity text is already present, skip
     (idempotent).
   - In the command string, replace the literal `PYTHON_EXE` placeholder with the
     interpreter path from step 2.

5. **Verify.** Confirm both files are valid: `CLAUDE.md` is in place, and
   `settings.json` parses as JSON with the new hook present. Print the resolved
   Python path used.

6. **Report.** One block: what was installed, the Python path used, and this line —
   "Restart Claude Code, then send a test message to confirm replies come back short."

## Notes
- The hook only shapes chat replies; documents/code/runbooks are exempt (the hook
  text says so).
- This machine is a standalone work context — do not wire it into any personal
  vault or coordination layer.
