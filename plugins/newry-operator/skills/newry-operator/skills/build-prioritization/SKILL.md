---
name: build-prioritization
description: >
  Advise on what to build next in the Newry AI program. Reads current program status,
  principles, and the decision log to produce a ranked recommendation with rationale.
---

# Build Prioritization

Reads the current program state and applies program principles to advise on what to build
or prioritize next.

**Audience:** Program builders. Use when the backlog has multiple options and you need a
reasoned recommendation.

---

## What to load before advising

- `references/principles.md`
- Decision log — check for prior prioritization decisions or held items. Read from
  `~\Newry Corp\Clients - Claude Master Working Folder\logs\newry-operator\decision-log.md`
  (live canonical snapshot). Fall back to bundled `references/decision-log.md` if not synced.
- `strategy/program-status.md` — current plugin versions, active development, next priorities,
  backlog. Read from the Cowork working folder. Fall back to asking the operator to describe
  current state if the file is not found.

---

## How to prioritize

Assess each backlog item against four criteria:

1. **Consultant impact** — hours saved × breadth of use × quality delta
2. **Build feasibility** — complexity, dependencies, required infrastructure already in place
3. **Program principles** — does it advance the north star? does it compound on what's built?
   (Principles 4, 7, 9, 11 are most relevant here)
4. **Urgency / sequencing** — is there a forcing function, dependency, or time constraint
   that makes order matter?

Cross-check the decision log for any prior prioritization calls or items explicitly held.

---

## Output format

- **Current state summary:** 2–3 sentences on where the program is
- **Recommended next 3:** ranked, each with a one-sentence rationale
- **Held / waiting:** items that are blocked or time-sensitive but not actionable now
- **One flag:** anything in the backlog that looks misaligned with principles or the north star

Keep it short. This is a recommendation, not a full analysis.

---

## Close

After prioritizing, ask:

> "Want to log the prioritization decision?"

If yes, hand off to `decision-capture` with the recommendation and rationale pre-filled
as context — the operator should only need to confirm, not re-enter.
