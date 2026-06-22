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


def ensure_pywin32():
    """Install pywin32 if not present (required for PowerPoint COM)."""
    try:
        import win32com.client  # noqa
        print("pywin32: already installed")
    except ImportError:
        print("pywin32: not found — installing...")
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], capture_output=True, text=True)
        if result.returncode == 0:
            print("pywin32: installed OK")
        else:
            print(f"pywin32: install failed — {result.stderr.strip()}")
            print("Run manually: pip install pywin32")


def main():
    ensure_pywin32()

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
