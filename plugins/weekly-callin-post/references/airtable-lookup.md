# Airtable lookup — active projects for a person

Base: **Newry Knowledge Management** `appRawPuacfAvVH2Z`

All IDs below are confirmed live. Always operate on record/field IDs, never user-facing names.

## Tables

| Table | ID |
|---|---|
| Staff | `tblAeAug2APoy0Jgf` |
| Project Roles | `tblYG4PfBYTnsv0WC` |
| Projects | `tbl3FaAcnmFWjRwqr` |

## Step 1 — Find the person's Staff record

`list_records_for_table` on Staff (`tblAeAug2APoy0Jgf`), filter Full Name (`fldMWoJwEEujuf82V`) contains the person's name. Confirm via their Newry email (`fldSp1YgJ9TWfHDaa`) if there's any ambiguity. Keep the returned record ID (e.g. Erin Ross = `recHzoqVYkTFuHYK1`).

## Step 2 — Find their EM roles on in-progress projects

`list_records_for_table` on Project Roles (`tblYG4PfBYTnsv0WC`) with an AND filter:
- Staff (`fldjnWTwVjYv926Yf`) `hasAnyOf` [their Staff record ID]
- Type (`fldRgACuXbe7SOonv`) `=` `selchiHG3ThvhSWMk` (the "EM" choice)

Request these fields to read the result without extra calls:
- `fldMHFHFX3R7RtUK1` — Project (linked record: id + name, where name = project code)
- `fldRgACuXbe7SOonv` — Type
- `fldSuODm0x67u1LrS` — Project Status (lookup; filter/verify = In Progress `selkVIFGOzjF1HWWA`)
- `fldQreA9EQZ4svb1g` — Project Name (lookup)

Type choices on Project Roles: ED `seltrFAkd8XIGRXZl` · **EM `selchiHG3ThvhSWMk`** · Team Member `sel8P4z2faCqffDG5` · Editor `selTT9l6qGaGmScs3`.

Keep only rows where Project Status = In Progress (`selkVIFGOzjF1HWWA`). That linked-project set is the **baseline candidate list**.

## Step 3 — Pull per-project metadata (for the post's static fields)

For each candidate project, `list_records_for_table` on Projects (`tbl3FaAcnmFWjRwqr`) by record ID. Useful fields:

| Field | ID | Use |
|---|---|---|
| Project Name | `fldU9JlF5KzJUw1G3` | header |
| Project Code | `fldlCZtRzO8hORE9V` | internal matching key (see below) |
| Status | `fldJtAz4FzU3U3P6S` | confirm In Progress |
| Project Description | `fldhAgARKAFCQ5THV` | source for Purpose |
| Client Goals | `fldDc5Xp5reOkAmTP` | source for Purpose |
| Firm Goals | `fldLz6Jz9sXI4P3Hz` | source for Purpose |
| SharePoint Project Folder Url | `fldbEfKoq99a16y8X` | entry point for step 3 SharePoint gathering |
| SharePoint Folder Name | `fldxyhKxcytbdHzGs` | SharePoint search fallback |

To get the full team for the *Team* field, query all Project Roles for that project (filter Project `fldMHFHFX3R7RtUK1` `hasAnyOf` [project id]) and read Staff (`fldjnWTwVjYv926Yf`) across the returned roles.

## Project-code matching (the "IN02" vs "INGEV02" problem — confirmed real)

Airtable's Project Code will often NOT match the string the person types in Slack:
- Erin posts **"IN02"** → Airtable **"INGEV02"** (Ingevity)
- Erin posts **"DUP038"** → Airtable **"DUP38"** (DuPont Tyvek)
- Others post free-form: "COR770 Thin Triple Q2 2026", "ALTA, ALTA01", "Sequoia Financial – SEQ01"

Rules:
- **Match on the client/company + fuzzy code**, not exact code string. Normalize (uppercase, strip spaces/leading zeros) and compare prefixes; use the project/client *name* as the strong key when codes disagree. Fuzzy matching is only for *identifying* which Airtable project a Slack post refers to.
- **For the draft output, always use Airtable's Project Code — that is THE project code.** Any different string a person has used in Slack (IN02, DUP038, free-form) was improvised; normalize it to the Airtable code for display: "IN02" → **INGEV02**, "DUP038" → **DUP38**. This standardizes the channel on the canonical code.
- When you genuinely can't tell whether a Slack project maps to an Airtable candidate, ask in the step-2 checkpoint rather than guessing.

## Known data-quality flags to expect (do not auto-fix)

- **Wrong/stale EM:** e.g. INGEV02 lists Amy Fritz as EM and Erin Ross as Team Member, though Erin runs it week to week. If the person clearly runs a project they're not EM-of-record on, surface it in the checkpoint; don't silently include or exclude.
- **Not closed out:** projects left "In Progress" after they've actually ended. Surface via the Slack "Done!"/staleness check in SKILL step 2.
- No write-back in v1 — flag only.
