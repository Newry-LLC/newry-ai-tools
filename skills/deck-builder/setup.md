# Deck Builder — Setup & Verification Guide

Load this file at the start of a setup session. Walk through each phase in order. Don't skip ahead — each phase confirms the foundation for the next.

---

## How the skill works (read this first)

The Deck Builder connects to a **running PowerPoint instance** via Windows COM. This means:
- PowerPoint must be installed on this machine
- The deck you want to work on must be **open in PowerPoint** before you run any commands
- Claude controls PowerPoint live — it doesn't read or write .pptx files directly

This is why closing the file breaks it. The file must stay open.

---

## Phase 1 — Verify prerequisites

Run each check. If any fail, jump to the fix in Phase 2.

**Check 1: Python**
```
python --version
```
Expected: `Python 3.x.x`. If not found, Python isn't in PATH.

**Check 2: pywin32 (COM library)**
```
python -c "import win32com.client; print('pywin32 OK')"
```
Expected: `pywin32 OK`. If ImportError, pywin32 isn't installed.

**Check 3: Repo is cloned**
```
dir %USERPROFILE%\.newry\skills
```
Expected: shows a `deck-builder` folder. If not found, repo isn't cloned.

**Check 4: Skill is wired into Code**
```
type %USERPROFILE%\.claude\CLAUDE.md
```
Look for a `## Newry AI Skills` section with a trigger table. If missing, installer didn't run.

---

## Phase 2 — Fix any gaps found in Phase 1

**Python not found:**
Install from python.org/downloads. Check "Add Python to PATH" during install. Then close and reopen the terminal.

**pywin32 missing:**
```
pip install pywin32
```
Then restart Claude Code.

**Repo not cloned:**
```
git clone https://github.com/Newry-LLC/newry-ai-tools %USERPROFILE%\.newry
```

**Skill block missing from CLAUDE.md:**
```
python %USERPROFILE%\.newry\install.py
```
Then restart Claude Code.

After any fix, re-run the affected check in Phase 1 to confirm it's resolved before moving on.

---

## Phase 3 — Verify PowerPoint is ready

1. Open PowerPoint
2. Open any deck (can be a blank one or any real file)
3. Leave it open — don't close it during the session

---

## Phase 4 — Test the skill

In Claude Code (any working folder), type:

```
ppt
```

Expected: Claude recognizes the trigger and asks what you'd like to build or edit.

If Claude doesn't respond to the skill (e.g. just gives a generic answer), the skill isn't loading. Check that:
- You restarted Code after install
- The CLAUDE.md block is present (Phase 1, Check 4)
- The path in the trigger table points to the right location

---

## Phase 5 — Run a real test

With a deck open in PowerPoint, run a safe read-only test first:

> "Profile slide 1"

Claude should read the slide and return a structured breakdown: shapes, text, fonts, layout role, capacity estimate. No changes made.

If that works, try a simple edit:

> "Edit the title of slide 1 to say 'Test Title'"

Claude should update it live in PowerPoint. You'll see the change immediately.

---

## Phase 6 — Build a new slide (full test)

Ask Claude to build a layout from scratch:

> "Build a new slide using the nbd_growth_levers layout. Add it to the end of the deck. Use these three levers: [lever 1], [lever 2], [lever 3]."

This exercises the full build pipeline: clones the layout from the library, fills in your content, appends to the deck.

---

## Troubleshooting

**"No running PowerPoint instance found"** — PowerPoint isn't open, or no presentation is open in it. Open a deck first.

**"win32com not found" / ImportError** — pywin32 not installed. Run `pip install pywin32` and restart Code.

**Skill doesn't trigger** — type exactly "ppt" or "build slides". Check that the `~/.claude/CLAUDE.md` has the Newry AI Skills block. Restart Code after any CLAUDE.md change.

**Changes not appearing in PowerPoint** — make sure you're looking at the right deck. The skill connects to whichever presentation is active in the running PowerPoint instance.

**"Permission denied" on a .pptx file** — the skill should never need to access the file directly. If you see this, something else is trying to read the file as a binary. Make sure the Deck Builder skill is triggering, not generic Claude file manipulation.
