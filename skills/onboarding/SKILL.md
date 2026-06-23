# Newry AI Tools — Onboarding Skill

**Triggers:** "set up newry", "install newry", "newry setup", "bootstrap newry", "check my setup", "verify setup", "troubleshoot ppt", "troubleshoot setup"

When triggered, first check whether this is a fresh install or a verification run:

```
dir %USERPROFILE%\.newry\skills
```

- Folder **doesn't exist** → fresh install, run Steps 1–7 below.
- Folder **exists** → skip to [Verification](#verification).

---

## Fresh install

### Step 1 — Check git

```
git --version
```

- Returns a version: continue.
- Not found: tell the user to install git from https://git-scm.com/download/win, then come back and say "set up newry" again.

### Step 2 — Check Python

```
python --version
```

- Returns a version: continue.
- Not found: install via winget:
  ```
  winget install Python.Python.3.13
  ```
  After it completes, run `python --version` in a new shell to confirm. Then continue.

### Step 3 — Clone the repo

```
git clone https://github.com/Newry-LLC/newry-ai-tools %USERPROFILE%\.newry
```

Confirm the clone succeeded before continuing.

### Step 4 — Run the installer

```
python %USERPROFILE%\.newry\install.py
```

This automatically:
1. Installs pywin32 (PowerPoint COM library)
2. Installs ppt-mcp (PowerPoint MCP server) and wires it into `~/.claude/mcp.json`
3. Wires all skills — including this one — into `~/.claude/CLAUDE.md`

Read the output. If pywin32 or ppt-mcp install failed, stop and resolve before continuing.

### Step 5 — Verify CLAUDE.md

```
type %USERPROFILE%\.claude\CLAUDE.md
```

Look for a `## Newry AI Skills` section listing Deck Builder and Onboarding. If missing, run install.py again.

### Step 6 — Restart Code

Run the restart script to kill all Claude Code and ppt-mcp processes cleanly:

```
powershell -ExecutionPolicy Bypass -File %USERPROFILE%\.newry\restart-code.ps1
```

Then reopen Claude Code manually. A new session in the same window is not enough — the app must fully relaunch for mcp.json to be read.

### Step 7 — Smoke test

Two checks — both must pass.

**Check 1: Skill loads**
Type `ppt`. Claude should recognize the trigger and read the Deck Builder skill instructions. If it gives a generic answer, the skill isn't loading — confirm the `## Newry AI Skills` block is in CLAUDE.md and restart again.

**Check 2: ppt-mcp is connected**
Ask: "Do you have any ppt_* tools available?"
- Yes → ppt-mcp is connected. Continue.
- No → run the restart script again and reopen Code. If still failing, check Code's MCP status panel (Settings → MCP or Integrations) for an error next to ppt-mcp.

**Live test**
Open any PowerPoint deck. Say: "Profile slide 1."

Claude should return a structured breakdown of the slide — shapes, text, fonts, capacity estimates. Setup is complete.

---

## Verification

Use this when already installed — to confirm setup is working, pick up updates, or troubleshoot.

**Step 1 — Pull latest and re-run installer**
```
git -C %USERPROFILE%\.newry pull
python %USERPROFILE%\.newry\install.py
```

**Step 2 — Restart Code**
```
powershell -ExecutionPolicy Bypass -File %USERPROFILE%\.newry\restart-code.ps1
```
Then reopen Code.

**Step 3 — Run the smoke test**
Same as Step 7 above — both checks must pass.

---

## Troubleshooting

**"No running PowerPoint instance found"** — PowerPoint isn't open, or no file is open in it. Open a deck first.

**"win32com not found" / ImportError** — pywin32 not installed. Run `pip install pywin32` and restart Code.

**Skill doesn't trigger on "ppt"** — Check that `~/.claude/CLAUDE.md` has the Newry AI Skills block. Restart Code after any CLAUDE.md change.

**ppt-mcp installed but not connecting** — Run the restart script. If still failing, check Code's MCP status panel for an error message. The exe must be running; check Task Manager for `ppt-mcp.exe`.

**Changes not appearing in PowerPoint** — Confirm you're looking at the right deck. The skill connects to whichever presentation is active in the running PowerPoint instance.

---

## Reference — what's installed

| Component | Location | Purpose |
|---|---|---|
| Repo | `%USERPROFILE%\.newry\` | Skill files + future updates |
| pywin32 | Python packages | PowerPoint COM connection |
| ppt-mcp | Python packages + `~/.claude/mcp.json` | PowerPoint MCP tools for Claude |
| CLAUDE.md block | `%USERPROFILE%\.claude\CLAUDE.md` | Loads skills every Code session |

To update in the future: `git -C %USERPROFILE%\.newry pull && python %USERPROFILE%\.newry\install.py`
