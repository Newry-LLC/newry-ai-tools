# Newry AI Tools — Bootstrap Skill

**Trigger:** "set up newry", "install newry", "newry setup", "bootstrap newry"

When triggered, run through the steps below in order. Check each thing, fix it if needed, confirm it before moving on. Tell the user what you're doing at each step and what you found. Don't skip ahead.

---

## Step 1 — Check git

Run:
```
git --version
```

- If it returns a version: git is installed. Continue.
- If not found: tell the user to download and install git from https://git-scm.com/download/win, then come back and say "set up newry" again to continue.

---

## Step 2 — Check Python

Run:
```
python --version
```

- If it returns a version: Python is installed. Continue.
- If not found: install it via winget:
  ```
  winget install Python.Python.3.13
  ```
  After it completes, tell the user: "Python installed. Close this terminal window, open a fresh one, navigate back to this session, and say 'set up newry' again to continue." Stop here — the PATH update requires a new terminal.

---

## Step 3 — Check if repo is already cloned

Run:
```
dir %USERPROFILE%\.newry\skills
```

- If it shows a `deck-builder` folder: already cloned. Skip to Step 4.
- If the folder doesn't exist: clone it:
  ```
  git clone https://github.com/Newry-LLC/newry-ai-tools %USERPROFILE%\.newry
  ```
  Confirm the clone succeeded before continuing.

---

## Step 4 — Run the installer

Run:
```
python %USERPROFILE%\.newry\install.py
```

This does three things automatically:
1. Installs pywin32 (the PowerPoint COM library) if missing
2. Wires all skills into `~/.claude/CLAUDE.md` so they load every session
3. Confirms what was installed

Read the output. If pywin32 install failed, tell the user and stop — they'll need to resolve it before continuing.

---

## Step 5 — Verify CLAUDE.md was updated

Run:
```
type %USERPROFILE%\.claude\CLAUDE.md
```

Look for a `## Newry AI Skills` section with a trigger table listing Deck Builder. If it's there, the wiring is correct. If missing, something went wrong with Step 4 — run install.py again.

---

## Step 6 — Restart Claude Code

Tell the user: "Everything is installed. Close Claude Code completely and reopen it. Then open PowerPoint with any deck, come back to Code, and type 'ppt' to confirm the skill is working."

---

## Step 7 — Smoke test (after restart)

When the user says the skill triggered on "ppt":

Ask them to run a live test:
> "Open any PowerPoint deck. Then tell me: profile slide 1."

Run a profile operation on slide 1. If it returns a structured breakdown of the slide (shapes, text, fonts), setup is complete. Tell the user they're good to go.

If the skill doesn't trigger on "ppt" after restart, check:
- Is the `## Newry AI Skills` block in `%USERPROFILE%\.claude\CLAUDE.md`?
- Did Code fully close and reopen (not just a new session in the same window)?
- Run `python %USERPROFILE%\.newry\install.py` again, then restart once more.

---

## Reference — what was installed

| Component | Location | Purpose |
|---|---|---|
| Repo | `%USERPROFILE%\.newry\` | Skill files + future updates |
| pywin32 | Python packages | PowerPoint COM connection |
| CLAUDE.md block | `%USERPROFILE%\.claude\CLAUDE.md` | Loads skills every Code session |

To update skills in the future: `cd %USERPROFILE%\.newry && git pull && python install.py`
