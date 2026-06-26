---
name: workplan
description: Turn an approved issue tree into a concrete, sequenced activity list — the work breakdown for the engagement. Generates the analyses and activities needed to resolve each issue, orders them, and gives the EM guidance for placing them on the project timeline. Hands off to ownership-and-goals for assigning people.
---

# Workplan Sub-Skill

Take the approved issue tree and translate it into a sequenced activity list — the concrete work the team will do to resolve each issue. This is the **work breakdown**. Assigning people and writing their goals is a separate step, owned by the **ownership-and-goals** sub-skill, which takes this activity list as its input.

The skill produces the activity content and sequencing guidance. It does **not** draw the Gantt/timeline chart — calendar placement depends on real constraints the EM holds, so the skill guides the EM in building it rather than faking it.

## Inputs

**Required:**
- Issue tree with hypotheses (from the issue-tree sub-skill or provided directly)

**Optional:**
- Project timeline / key milestones (helps sequence and phase the activities)
- Budget / consultant days (used to flag if the activity list is too heavy or light for the team)

**Read the method first.** Before building activities, read `references/project initiation resources/2025 CLST Workplanning (Module 1 and 2).md` (the issue-tree → workplan transition and activity sequencing).

## What This Skill Does

1. **Activity list per issue** — for each issue in the tree, generate the specific analyses and activities needed to resolve it. Each must be concrete enough to place on a timeline (e.g. "conduct 8 customer pull interviews with Tier-1 OEM procurement leads," not "do primary research").
2. **Sequence** — activities run on overlapping tracks, not in a waterfall. Secondary research, interview guide design, and participant sourcing begin simultaneously at project start. Knockout analyses run immediately. Grounding interviews typically happen in weeks 1–2 alongside secondary — they don't wait for it to complete. Synthesis is iterative; begin as data comes in. Deck drafting follows sufficient synthesis, not all of it. Mark activities as early / mid / late and flag dependencies. For full sequencing guidance, follow `references/project initiation resources/2025 CLST Workplanning (Module 1 and 2).md`.
3. **Phase guidance** — group activities into rough phases and call out dependencies, so the EM can place them on the timeline.
4. **Budget flag** — if consultant days are provided, estimate rough effort and flag if the activity list looks over- or under-weight for the team.

## Output

### Activity list by issue

For each issue:
```
Issue [N]: [Issue text]
Hypothesis: [From issue tree]
Activities (sequenced):
  - [Specific analysis or task]
  - [Specific analysis or task]
Timing: [early / mid / late] — [dependency notes]
```

### Sequencing & timeline guidance

- Ordered view of activities across all issues (what comes first, what gates what)
- Suggested phases (e.g. framing & secondary research → primary research → synthesis → recommendations)
- Which analyses to front-load (knockouts, peer-review-worthy framing) and which come later

This is what the EM uses to build the Gantt/timeline page of the launch deck. The skill does not draw the Gantt — it supplies the sequenced activities and dependencies; the EM places them against the real calendar.

### Workstream summary

After the activity list, name the suggested workstreams — ownable clusters of related activities that map to the responsibility matrix in ownership-and-goals. Typically 3–5 workstreams for a standard engagement.

```
Suggested workstreams for ownership assignment:
- [Workstream name] — [one-line description of what's included]
- [Workstream name] — [one-line description]
- ...
```

These become the pre-populated rows in the ownership-and-goals responsibility matrix. The EM can rename, split, merge, or add rows freely.

→ Hand the activity list and workstream summary to **ownership-and-goals** to assign owners and set each person's value-creation and development goals.

## Design Notes

- **Activities must be concrete.** "Conduct 6–8 customer pull interviews targeting procurement leads at Tier-1 OEMs" is an activity. "Do primary research" is not.
- **One-to-one traceability.** Every activity maps to an issue. Flag any that don't — they're either scope creep or a sign the issue tree is incomplete.
- **Don't generate the Gantt.** Sequence and timing depend on real calendar constraints the EM knows. Provide the ordered activity list and dependencies; let the EM place items on the timeline.
- **Ownership is a separate step.** This skill stops at activities and sequencing. Assigning people and writing value-creation/development goals belongs to ownership-and-goals — don't reproduce the responsibility table here.
- **The output is a starting point.** EM reviews with ED before kickoff, shares with team at kickoff, revisits weekly.

## References

- `references/project initiation resources/2025 CLST Workplanning (Module 1 and 2).md` — activity sequencing, delegation, workplan elements
- `references/project initiation resources/2025 Consulting Process and Thought Leadership Onboarding.md` — issue → analysis → activities chain
- Project Initiation Template — the issue-tree-to-activities bridge page and the EM-built Gantt/timeline work plan page
