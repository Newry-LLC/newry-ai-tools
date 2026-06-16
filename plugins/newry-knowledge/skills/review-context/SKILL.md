---
name: review-context
description: >
  Reviews the pending context queue: low-confidence facts held back from the
  context library for human approval. Surfaces each fact, lets the consultant
  approve, edit-then-approve, or reject it. Run when you want to clear the
  review queue or check what's waiting.
---

# Review Context — Pending Fact Queue

Low-confidence facts extracted from Slack and Otter sweeps are held in a
review queue rather than written directly to the context index. This skill
walks you through them.

**Context library location (Sylvan):**
`C:\Users\sshank\OneDrive - Newry Corp\Desktop\Newry non-project and backup\AI Tool Building\Building Tools for Newry\newry-context-library`

**Python executable:** `C:/Users/sshank/AppData/Local/Programs/Python/Python314/python.exe`

---

## Step 1 — Check the queue

Run from the context-library directory:

```
cd "C:\Users\sshank\OneDrive - Newry Corp\Desktop\Newry non-project and backup\AI Tool Building\Building Tools for Newry\newry-context-library"
python scripts/manage_pending.py stats
```

If output is "No pending facts." → tell the user and stop.

---

## Step 2 — List pending facts

```
python scripts/manage_pending.py list
```

Show the output to the user. Each fact has:
- **ID** (8-char hex, used for approve/reject)
- **kind**: `fact` (objective) or `color` (sentiment/opinion)
- **bucket**: where it will be written if approved
- **fact text**: the distilled fact
- **citation**: source URL (slack:// or otter://)

---

## Step 3 — Walk through each fact

For each pending fact, present it clearly:

```
[ID: abc12345] [kind: fact] [bucket: internal]
Fact: "..."
Source: slack://C08.../...
Approve (A) / Edit then approve (E) / Reject (R)?
```

Wait for the user's response before moving to the next fact. Do not batch
decisions without explicit confirmation.

**Approve:**
```
python scripts/manage_pending.py approve abc12345
```

**Edit then approve** (user provides corrected text):
```
python scripts/manage_pending.py approve abc12345 --fact "corrected fact text here"
```

**Reject:**
```
python scripts/manage_pending.py reject abc12345
```

---

## Step 4 — Confirm and summarize

After each decision, confirm the action taken ("Approved and written to internal",
"Rejected"). When all facts are reviewed (or the user says stop), show a brief
summary: N approved, M rejected, K remaining.

If there are many facts (>10) and the user wants to batch-approve a bucket,
offer: "Approve all remaining in [bucket]?" — only proceed if confirmed.

---

## Notes

- Approved facts go directly into the relevant bucket index (same as high-confidence facts).
- Rejected facts are deleted — they will not reappear unless that source is re-swept.
- The citation is preserved so you can look up the original message if needed.
- `add-context` entries (manually written via the add-context skill) bypass this queue —
  they are always written directly.
