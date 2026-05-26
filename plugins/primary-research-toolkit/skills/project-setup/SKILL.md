---
name: project-setup
description: >
  Shared Step 0 block for all file-writing Newry skills. Verifies the correct project
  folder is mounted, establishes project identity, and ensures the skill-specific
  subfolder exists before any work begins. Referenced by PRT, Tech Orientation,
  RMA-OA Builder, and any future file-writing skill.
---

# Project Setup & Verification (Step 0)

Run this block at the start of every session, before any other work. It is silent where possible — surface messages only when action is required.

---

## Check 0 — SharePoint log folder sync

Before any other check, verify the central log folder exists on this machine:

```python
import os
log_dir = os.path.expanduser(r"~\Newry Corp\Clients - Claude Master Working Folder\logs")
exists = os.path.exists(log_dir)
```

**If it exists:** proceed silently.

**If it does not exist:**

1. Check whether `~/.newry-sync-warned` exists. If it does, skip the message and proceed — the consultant has already been notified.
2. If not warned yet: create `~/.newry-sync-warned`, then show this message **once** and proceed with the skill run (do not block):

> "**One quick setup step:** To enable usage logging, the Claude Master Working Folder needs to be synced from SharePoint to your machine.
>
> 1. Copy this link and paste it into Microsoft Edge: `https://newrycorp.sharepoint.com/clients/SitePages/Home.aspx?RootFolder=%2Fclients%2FShared%20Documents%2FConsulting%20Ops%2FClaude%20Master%20Working%20Folder&FolderCTID=0x0120001E5A3B5DC4435348B27C9444F34FA80E&View=%7B9352A612%2DAF51%2D4D22%2D9834%2DC437D38F2209%7D`
> 2. Click **Sync** — it's in the toolbar just below where it says "Documents," between **Upload** and **Share**
> 3. Once it appears in File Explorer under `Newry Corp`, logging will work automatically
>
> You only need to do this once. Continuing with your request now."

---

## Check 1 — Working directory

Attempt to list the contents of the current working directory.

**If no working directory is accessible:** stop. Ask:

> "I don't see a working folder mounted. Before we start, how would you like to work?
>
> **Option A — SharePoint project folder (recommended):** Set up a `Claude Working Folder - [project code]` in your project on SharePoint, sync it locally, and add it as your working folder in this Cowork project. Outputs are saved to SharePoint, project identity is verified throughout the session, and your work persists and is shareable.
>
> **Option B — Informal local session:** Mount any folder on your local machine. Outputs will be saved there only — not to SharePoint, no project structure enforced, no mismatch detection. Good for quick exploration; not suitable for client deliverables.
>
> Which would you prefer?"

- If Option A: walk them through setup (create folder on SharePoint → sync → mount in Cowork → restart session). Do not proceed until mounted.
- If Option B: note the working folder path, skip Checks 2 and 3, proceed to the calling skill. Tell the consultant: "Running in informal mode — outputs will be saved to [folder path]. No project verification will run." In informal mode, the calling skill proceeds as normal for subfolder creation and file writes — using its own subfolder (e.g., `Primary Research/`, `Technical Orientation/`) within the mounted folder root, same as in full mode. Project structure enforcement and mismatch detection are off, but file paths are otherwise unchanged.

---

## Check 2 — Project identity

**If `project.md` exists at the root of the working directory:**
Read it. Extract: project code, client name, and any listed keywords or aliases.
Confirm with the consultant:

> "I can see this is [Project Code] — [Client Name]. Is that right?"

Wait for explicit confirmation before proceeding. If they say no, ask which project they're working on and whether they're in the right session. Do not continue until confirmed.

**If `project.md` does not exist:**

Check `context/` for documents.

- **If documents are present:** Read them. Generate `project.md` at the root of the working directory using the template below. Show the consultant the key fields and ask them to confirm before proceeding.

- **If `context/` is empty or missing:** Stop. Ask the consultant:

  > "I don't see any project documents in `context/`. You can either (a) add your SOW, proposal, or kickoff deck to `context/` and restart, or (b) proceed in informal mode — outputs will be saved to this folder with no project verification. Which would you prefer?"

  If they choose informal mode, proceed as in Option B above.

**`project.md` template:**
```markdown
# [Project Code] — [Client Name]

## Project
- **Code:** [project code]
- **Client:** [client name]
- **Engagement:** [brief description from SOW/proposal]
- **Newry ED:** [if known]

## Keywords
[client name variations, product names, business unit names — used for mismatch detection]

## Folders
[populated by skill on first run]
```

---

## Check 3 — Skill subfolder

Check whether the skill-specific subfolder exists in the working directory.

The calling skill specifies its subfolder name (e.g., `Primary Research` for PRT, `Technical Orientation` for Tech Orientation, `RMA` for RMA-OA Builder).

**If the subfolder does not exist:** Create it, along with any required sub-subfolders defined by the calling skill. Tell the consultant:

> "I've created the `[Subfolder Name]/` folder in your working directory. It will sync to SharePoint automatically."

After creating the subfolder, update the Folders section of `project.md` to include the new subfolder and its purpose (e.g., `Primary Research/ — PRT outputs: materials, preprocessed, outputs, logs`).

**If it exists:** proceed silently.

---

## Ongoing — Materials mismatch detection

Throughout the session, whenever the consultant shares a document, transcript, filename, or any other material, scan it for client name, project code, company names, product names, and any keywords from `project.md`.

A mismatch is triggered when a material contains a name, project code, or company identifier that (a) does not appear in `project.md` keywords, AND (b) is plausibly a different client or engagement than the confirmed project — not a known competitor, partner, or industry reference already in scope. A document mentioning a competitor by name is not a mismatch. A document with a different client's logo or project code is.

**If a mismatch is detected:**

Stop immediately. Do not read further into the material. Tell the consultant:

> "This [document/transcript/file] mentions [detected name], but we're working on [confirmed project]. Before I continue, can you confirm you have the right file?"

Do not proceed until the consultant explicitly confirms the correct material is in hand.

This check runs for every new piece of material introduced in the session — not just at the start.

---

## Graceful degradation

If this skill file is not found by a calling skill, the calling skill should:
1. Ask the consultant to confirm the project name and code before proceeding
2. Warn explicitly: "Project verification is unavailable — mismatch detection is off. Please ensure you have the correct project materials before continuing."
3. Proceed without folder structure enforcement or mismatch detection
