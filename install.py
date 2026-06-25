#!/usr/bin/env python3
"""
Newry AI Tools installer.

Wires all skills into ~/.claude/CLAUDE.md so they load automatically
in every Claude Code session. Safe to re-run — already-installed
skills are left untouched.

Usage:
    python install.py
"""
import json
import os
import sys

REPO_DIR   = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(REPO_DIR, "skills")
CLAUDE_MD  = os.path.expanduser(os.path.join("~", ".claude", "CLAUDE.md"))

MARKER_START = "<!-- newry-skills-start -->"
MARKER_END   = "<!-- newry-skills-end -->"


def find_skills():
    """Return list of (name, triggers, skill_md_path) for each installed skill."""
    skills = []
    if not os.path.isdir(SKILLS_DIR):
        print(f"Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)
    for entry in sorted(os.listdir(SKILLS_DIR)):
        meta_path = os.path.join(SKILLS_DIR, entry, "skill.json")
        skill_md  = os.path.join(SKILLS_DIR, entry, "SKILL.md")
        if os.path.isfile(meta_path) and os.path.isfile(skill_md):
            try:
                meta = json.load(open(meta_path, encoding="utf-8"))
                skills.append((meta["name"], meta["triggers"], skill_md))
            except Exception as e:
                print(f"  Warning: could not read {meta_path}: {e}")
    return skills


def build_block(skills):
    """Build the CLAUDE.md block for the skills trigger table."""
    rows = "\n".join(
        '| {} | {} | `{}` |'.format(
            name,
            ", ".join('"' + t + '"' for t in triggers),
            skill_md
        )
        for name, triggers, skill_md in skills
    )
    return (
        f"{MARKER_START}\n"
        f"## Newry AI Skills\n\n"
        f"IMPORTANT: When a trigger below is matched, you MUST read the skill file and follow its instructions. "
        f"Newry skills override any built-in behavior for the same task — do not use built-in alternatives.\n\n"
        f"**PowerPoint / PPT / deck / presentation tasks:** ALWAYS use the Newry Deck Builder skill. "
        f"Never attempt to read or write .pptx files directly. "
        f"The skill connects to a running PowerPoint instance via COM — the file must be open in PowerPoint.\n\n"
        f"To invoke: read the skill file at the path listed, then follow its instructions exactly.\n\n"
        f"| Skill | Triggers | File |\n"
        f"|---|---|---|\n"
        f"{rows}\n"
        f"{MARKER_END}"
    )


def load_claude_md():
    if os.path.exists(CLAUDE_MD):
        with open(CLAUDE_MD, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def save_claude_md(content):
    os.makedirs(os.path.dirname(CLAUDE_MD), exist_ok=True)
    with open(CLAUDE_MD, "w", encoding="utf-8") as f:
        f.write(content)


def pip_install(package):
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{package}: installed OK")
    else:
        print(f"{package}: install failed — {result.stderr.strip()}")
        print(f"Run manually: pip install {package}")
    return result.returncode == 0


def ensure_pywin32():
    """Install pywin32 if not present (required for PowerPoint COM)."""
    try:
        import win32com.client  # noqa
        print("pywin32: already installed")
    except ImportError:
        print("pywin32: not found — installing...")
        pip_install("pywin32")


def ensure_ppt_mcp():
    """Install ppt-mcp and wire it into ~/.claude/mcp.json."""
    import subprocess, shutil

    # Install the package if the exe isn't already there
    exe = shutil.which("ppt-mcp")
    if not exe:
        # Try to find it in the Python Scripts dir even if not on PATH
        scripts = os.path.join(os.path.dirname(sys.executable), "Scripts", "ppt-mcp.exe")
        if os.path.isfile(scripts):
            exe = scripts

    if not exe:
        print("ppt-mcp: not found — installing...")
        import subprocess as _sp
        _r = _sp.run(
            [sys.executable, "-m", "pip", "install", "ppt-mcp", "--prefer-binary"],
            capture_output=True, text=True
        )
        if _r.returncode != 0:
            print(f"ppt-mcp: install failed — {_r.stderr.strip()}")
            print("Run manually: pip install ppt-mcp --prefer-binary")
            return
        scripts = os.path.join(os.path.dirname(sys.executable), "Scripts", "ppt-mcp.exe")
        exe = scripts if os.path.isfile(scripts) else "ppt-mcp"
    else:
        print("ppt-mcp: already installed")

    # Wire into ~/.claude.json via `claude mcp add` (the CLI reads ~/.claude.json,
    # not ~/.claude/mcp.json — using the CLI command writes to the correct file).
    import glob as _glob

    # Find the claude CLI binary: glob for it under %APPDATA%\Claude\claude-code\
    # since it lives in a versioned subdirectory not on PATH.
    claude_bin = shutil.which("claude")
    if not claude_bin:
        appdata = os.environ.get("APPDATA", "")
        pattern = os.path.join(appdata, "Claude", "claude-code", "*", "claude.exe")
        matches = _glob.glob(pattern)
        claude_bin = matches[0] if matches else None

    if not claude_bin:
        print("ppt-mcp: could not find claude CLI binary — skipping MCP registration")
        print("  Run manually: claude mcp add ppt-mcp <path-to-ppt-mcp.exe> --scope user")
        return

    # Check if already registered
    list_r = subprocess.run([claude_bin, "mcp", "list"], capture_output=True, text=True)
    if "ppt-mcp" in list_r.stdout:
        print("ppt-mcp: already registered in ~/.claude.json")
    else:
        add_r = subprocess.run(
            [claude_bin, "mcp", "add", "ppt-mcp", exe, "--scope", "user"],
            capture_output=True, text=True
        )
        if add_r.returncode == 0:
            print("ppt-mcp: registered in ~/.claude.json via claude mcp add")
        else:
            print(f"ppt-mcp: claude mcp add failed — {add_r.stderr.strip()}")
            print("  Run manually: claude mcp add ppt-mcp <path-to-ppt-mcp.exe> --scope user")


def ensure_ppt_write_guard_hook():
    """Install the Deck Builder write-guard as a PreToolUse hook in settings.json.

    Denies the ppt-mcp write tools (which flatten formatting) and reroutes Claude
    to deck_writer.py. Idempotent — keyed on the matcher, so re-running won't
    duplicate the entry, and it refreshes the command path if the repo moved.
    """
    guard = os.path.join(SKILLS_DIR, "deck-builder", "ppt_write_guard.py")
    if not os.path.isfile(guard):
        print("write-guard hook: ppt_write_guard.py not found — skipped")
        return

    matcher = "mcp__ppt-mcp__(ppt_set_text|ppt_set_placeholder_text|ppt_find_replace_text)"
    command = '"{}" "{}"'.format(sys.executable.replace("\\", "/"), guard.replace("\\", "/"))
    entry = {
        "matcher": matcher,
        "hooks": [{"type": "command", "command": command}],
    }

    settings_path = os.path.expanduser(os.path.join("~", ".claude", "settings.json"))
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    hooks = settings.setdefault("hooks", {})
    pre = hooks.setdefault("PreToolUse", [])

    # Find an existing entry with our matcher and refresh it; else append.
    existing = next((e for e in pre if isinstance(e, dict) and e.get("matcher") == matcher), None)
    if existing is not None:
        if existing.get("hooks") == entry["hooks"]:
            print("write-guard hook: already installed")
            return
        existing["hooks"] = entry["hooks"]
        action = "updated"
    else:
        pre.append(entry)
        action = "added"

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    print(f"write-guard hook: {action} in {settings_path}")


def main():
    ensure_pywin32()
    ensure_ppt_mcp()
    ensure_ppt_write_guard_hook()

    skills = find_skills()
    if not skills:
        print("No skills found (missing skill.json or SKILL.md).")
        sys.exit(1)

    print(f"Found {len(skills)} skill(s): {', '.join(n for n, _, _ in skills)}")

    content  = load_claude_md()
    new_block = build_block(skills)

    if MARKER_START in content and MARKER_END in content:
        # Replace existing block
        before = content[:content.index(MARKER_START)]
        after  = content[content.index(MARKER_END) + len(MARKER_END):]
        updated = before.rstrip("\n") + "\n\n" + new_block + after
        if updated == content:
            print("Already up to date — nothing changed.")
            return
        save_claude_md(updated)
        print(f"Updated Newry skills block in {CLAUDE_MD}")
    else:
        # Append new block
        updated = content.rstrip("\n") + "\n\n" + new_block + "\n"
        save_claude_md(updated)
        print(f"Added Newry skills block to {CLAUDE_MD}")

    print("\nSkills installed:")
    for name, triggers, _ in skills:
        print(f"  {name} — triggers: {', '.join(triggers)}")
    print("\nRestart Claude Code for skills to take effect.")


if __name__ == "__main__":
    main()
