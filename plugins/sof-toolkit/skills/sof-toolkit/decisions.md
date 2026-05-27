# SoF Toolkit — Design Decisions

Decisions made, options ruled out, and why. Add an entry when a choice is made that future sessions might otherwise revisit or reverse.

---

**Don't add a rule for the SAM/SOM false-parallel miss**
During eval testing, the skill missed a headline that presented two opportunity figures as parallel when they came from different analytical levels (SAM vs. SOM). Decision: no rule added. A rule specific enough to catch this would be too narrow to generalize — it would catch SAM/SOM but not the broader class of false parallels. The right fix for subtle analytical reasoning is a more capable model, not a rule.

---

**Pyramid Principle is not restated in the skill**
The skill relies on the model's existing PP knowledge rather than defining it. Ruled out: a PP summary or doctrine section in SKILL.md. The model knows PP. Restating it adds length without adding capability.

---

**Universal-standards.md is capped at three rules**
Core claim standard, headline length, and coverage by stage. Ruled out: additional rules for specific slide patterns or formatting conventions. More rules make the skill longer without making it better. The ceiling is: only codify what's Newry-specific or requires explicit calibration.

---

**update-type-guidance.md was deleted**
Its content — how standards vary by update type — was collapsed into universal-standards.md under "coverage by stage." Ruled out: keeping it as a separate reference file. One topic belongs in one place.

---

**Non-traditional SoF formats are evaluated on their own terms**
OKR tables and module-overview structures are acknowledged and evaluated for what they are. Ruled out: penalizing deviation from traditional SoF structure. Three of five Newry test decks use non-traditional formats — they're a legitimate convention for Growth Engine and ongoing engagements, not mistakes.

---

**V1 PPTX annotation feature: designed, not built**
Spec exists in `V1-PPTX-design.md`. Decision: complete V0 eval testing before building V1. V1 annotates slides with the skill's feedback — if V0 quality isn't solid, V1 just automates flawed output.

---

**Added SCR framework reference to Draft mode**
Two blind Draft runs on the same deck (Sonnet 4.6 and Opus 4.6) both missed the technical necessity bullet — "glass is required for advanced performance" — classifying it as background context rather than a finding. The Pyramid Principle tells the model how to structure findings but not how to identify what qualifies as a finding vs. context. Minto's Situation-Complication-Resolution framework targets this: the Complication (why the transition is necessary) is a finding, not setup. Added as step 0 in Draft mode's drafting process. Considered and deferred: a set of annotated example SoFs. Best practices are cheaper to test; examples are the fallback if the SCR reference doesn't change output. Also added: when the source is a well-constructed deck, follow the slide sequence rather than re-ordering by importance.

---

**Strengthened SCR Complication → bullet rule in Draft mode**
Run 3 (Opus 4.6, blind retest after SCR addition) showed the SCR step correctly identified the technical necessity finding as the Complication, but the drafting steps still dropped it. The model identified it in analysis, then classified it as "obvious setup" during bullet ordering because it has no dollar figure attached. Fix: added explicit language to step 0 that if the Complication makes a claim about what is true, it must appear as a bullet — not just as context in the pre-draft analysis. This moves the intervention from story identification (where it was already working) to bullet selection (where it was failing). Annotated examples remain deferred as the heavier fallback.

---

**Draft mode utility: set expectations, don't over-engineer**
Four runs across two models confirmed Draft's structural gaps are stable: story structure is not reliable, the foundational "why this situation exists" claim is consistently undertreated, bullets are ordered by analytical weight rather than client story logic, and headlines often need rewriting. These gaps persisted through a targeted skill update. Conclusions: (1) closing them fully through rules alone is unlikely — they reflect narrative judgment that resists specification; (2) Draft is most valuable as an analytical first draft, with a light editorial pass expected for client deliverables. Added a "What to expect" block to Draft mode in SKILL.md so this guidance surfaces in use. Ruled out: a rule to prefer dollar figures over percentages in headlines (too specific, small sample). Ruled out: further iteration on the Glass Core deck (four runs is enough; next test must use a different deck).
