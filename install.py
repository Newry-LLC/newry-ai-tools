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


def _find_claude_bin():
    """Find the claude CLI binary (not reliably on PATH)."""
    import shutil
    import glob as _glob
    claude_bin = shutil.which("claude")
    if claude_bin:
        return claude_bin
    appdata = os.environ.get("APPDATA", "")
    pattern = os.path.join(appdata, "Claude", "claude-code", "*", "claude.exe")
    matches = _glob.glob(pattern)
    return matches[0] if matches else None


def _resolve_ppt_mcp_exe():
    """
    Locate ppt-mcp.exe using multiple strategies, in order:
      1. shutil.which (works when Scripts is on PATH)
      2. sysconfig default-scheme Scripts dir
      3. sysconfig user-scheme Scripts dir  (common on winget/Store Python)
      4. Derive from pip's reported 'Location' (most reliable on Store Python)

    Returns an absolute path to the exe, or None if not found.
    """
    import shutil, sysconfig, subprocess

    candidate = shutil.which("ppt-mcp")
    if candidate and os.path.isfile(candidate):
        return candidate

    for scheme in (None, "nt_user"):
        kwargs = {"scheme": scheme} if scheme else {}
        scripts = sysconfig.get_path("scripts", **kwargs)
        if scripts:
            candidate = os.path.join(scripts, "ppt-mcp.exe")
            if os.path.isfile(candidate):
                return candidate

    # Derive from pip show: Location is .../site-packages → Scripts is a sibling
    r = subprocess.run(
        [sys.executable, "-m", "pip", "show", "ppt-mcp"],
        capture_output=True, text=True
    )
    for line in r.stdout.splitlines():
        if line.startswith("Location:"):
            location = line.split(":", 1)[1].strip()
            scripts_dir = os.path.join(os.path.dirname(location), "Scripts")
            candidate = os.path.join(scripts_dir, "ppt-mcp.exe")
            if os.path.isfile(candidate):
                return candidate

    return None


def _get_registered_ppt_mcp_cmd():
    """
    Read ~/.claude.json and return the registered ppt-mcp command string,
    or None if ppt-mcp is not registered at all.
    """
    claude_json = os.path.expanduser(os.path.join("~", ".claude.json"))
    if not os.path.isfile(claude_json):
        return None
    try:
        with open(claude_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        entry = data.get("mcpServers", {}).get("ppt-mcp")
        if entry is None:
            return None
        return entry.get("command")
    except Exception:
        return None


def _registration_is_valid(cmd):
    """Return True if cmd is an absolute path that exists on disk."""
    if not cmd:
        return False
    return os.path.isabs(cmd) and os.path.isfile(cmd)


def ensure_ppt_mcp():
    """Install ppt-mcp and wire it into ~/.claude.json via claude mcp add."""
    import subprocess
    import importlib.metadata

    # --- 1. Detect installation via metadata (not exe presence) ---
    try:
        importlib.metadata.version("ppt-mcp")
        print("ppt-mcp: already installed")
    except importlib.metadata.PackageNotFoundError:
        print("ppt-mcp: not found — installing...")
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "ppt-mcp", "--prefer-binary"],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print(f"ppt-mcp: install failed — {r.stderr.strip()}")
            print("Run manually: pip install ppt-mcp --prefer-binary")
            return

    # --- 2. Resolve exe path robustly ---
    exe = _resolve_ppt_mcp_exe()
    if not exe:
        print("ppt-mcp: could not locate ppt-mcp.exe after installation")
        print("  On winget/Store Python, the exe is typically at:")
        print(r"  %LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0"
              r"\LocalCache\local-packages\Python313\Scripts\ppt-mcp.exe")
        print("  Run manually: claude mcp add ppt-mcp <full-path> --scope user")
        return

    # --- 3. Find the claude CLI ---
    claude_bin = _find_claude_bin()
    if not claude_bin:
        print("ppt-mcp: could not find claude CLI — skipping MCP registration")
        print(f'  Run manually: claude mcp add ppt-mcp "{exe}" --scope user')
        print(r"  (claude.exe is usually at %APPDATA%\Claude\claude-code\<version>\claude.exe)")
        return

    # --- 4. Validate existing registration; re-register if stale ---
    registered_cmd = _get_registered_ppt_mcp_cmd()
    needs_register = True

    if registered_cmd is not None:
        if _registration_is_valid(registered_cmd):
            if registered_cmd == exe:
                print(f"ppt-mcp: registration is valid ({exe})")
                needs_register = False
            else:
                # Valid path but pointing to a different exe (e.g. old Python env) — update it
                print(f"ppt-mcp: updating registration ({registered_cmd!r} -> {exe})")
                subprocess.run(
                    [claude_bin, "mcp", "remove", "ppt-mcp", "--scope", "user"],
                    capture_output=True, text=True
                )
        else:
            # Bare name or missing path — re-register
            print(f"ppt-mcp: existing registration is broken ({registered_cmd!r}) — re-registering...")
            subprocess.run(
                [claude_bin, "mcp", "remove", "ppt-mcp", "--scope", "user"],
                capture_output=True, text=True
            )
    else:
        needs_register = True  # not registered at all

    if needs_register or (registered_cmd is not None and not _registration_is_valid(registered_cmd)) \
            or (registered_cmd is not None and registered_cmd != exe):
        add_r = subprocess.run(
            [claude_bin, "mcp", "add", "ppt-mcp", exe, "--scope", "user"],
            capture_output=True, text=True
        )
        if add_r.returncode == 0:
            print(f"ppt-mcp: registered → {exe}")
        else:
            print(f"ppt-mcp: claude mcp add failed — {add_r.stderr.strip()}")
            print(f'  Run manually: claude mcp add ppt-mcp "{exe}" --scope user')
            return

    # --- 5. Connectivity check ---
    list_r = subprocess.run([claude_bin, "mcp", "list"], capture_output=True, text=True)
    ppt_line = next((l for l in list_r.stdout.splitlines() if "ppt-mcp" in l), None)
    if ppt_line and "✔" in ppt_line:
        print("ppt-mcp: ✔ Connected")
    elif ppt_line:
        print(f"ppt-mcp: registered but not yet connected — restart Claude Code for MCP to activate")
        print(f"  ({ppt_line.strip()})")
    else:
        print("ppt-mcp: WARNING — not showing in `claude mcp list` after registration")
        print("  Restart Claude Code and re-run install.py to verify")


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
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
