# SoF Skill — Draft Run Log

⚠️ **Do not read this file before running a blind Draft test.** Load it only after the fresh run is complete, then compare against entries here.

Two Draft runs completed. Both on the same deck (different models). Pattern confirmed: technical necessity bullet missed in both. SCR framework reference added to skill as a result.

---

## Draft Run: Glass Core Cost Analysis (nosf) — 4.14.26

**Source:** 2025.12.15 Newry Glass Core Cost Analysis - Update - Final _ Revised nosf.pptx
**Objectives:** Quantify glass core's value proposition for Corning; analyze how a switch from organic to glass core would alter OSAT cost structure and unit economics; guide pricing and customer strategy
**Stage / Audience:** Final client deliverable — Corning Confidential
**Input type:** Full PPTX extraction (markitdown); objectives slide provided (Slide 2)
**Model:** Claude Sonnet 4.6

---

### Quick Take

- **Headline:** Glass core commands a 79–161% premium if it eliminates the silicon interposer, but Scenario 2 returns are marginal to negative and early manufacturing costs limit near-term pricing power (175 chars — at the top of the range)
- **Scenario structure:** Scenario 1 (interposer elimination) vs. Scenario 2 (yield improvement only) is the right organizing tension; W2P range of $295–575 vs. -$25 to $125 is the most important number pair in the deck
- **Cost ramp:** Early manufacturing cost trajectory ($5,580 → $225–280 → ~$100 incremental at maturity) captured accurately; the maturity "still adds $100" point is important for Corning's pricing floor
- **Adoption triggers:** Tipping point metrics distilled correctly; package size, glass yield, and ecosystem commitment correctly called out as most critical
- **Unknowns bullet:** Intentionally thin — reflects the deck's open-questions close; flagged appropriately
- **Overall:** Draft output is accurate to the material and importance-ordered; Scenario 1 vs. 2 distinction is the right lead; ecosystem readiness bullet could be sharpened with specific timing (Absolics 2026)

---

### Full Draft Output

**Headline:**
> Glass core commands a 79–161% premium if it eliminates the silicon interposer, but Scenario 2 returns are marginal to negative and early manufacturing costs limit near-term pricing power

**Bullets:**

- **Interposer elimination is the scenario that creates compelling OSAT value — yield improvement alone does not.** Scenario 1 generates ~$410–580 in per-device benefits against ~$225–280 in late-stage costs, supporting W2P of $295–575 (79–161% premium over the $165–220 organic substrate). Scenario 2 (yield improvement only) yields W2P of -$25 to $125, and can be negative at current H100 yields.

- **Early manufacturing costs will be steep before stabilizing, and glass will still add ~$100 per device at maturity.** At 40% yield in the first 6 months, glass core adds ~$5,580 in incremental cost per device. By late stage (9–12 months at 90% yield), that narrows to ~$225–280. Even at mature, high-volume production, glass is expected to add ~$100 per unit versus organic, driven by higher CapEx depreciation and inspection requirements.

- **Adoption will turn on a small set of observable thresholds — package size, yield, and ecosystem commitment are most critical.** Glass becomes structurally advantaged when packages exceed ~100–120mm per side (Rubin and Feynman territory), glass panel yield reaches 90–95% in production, and at least one major fab or OSAT commits to glass panel investment. Organic equipment depreciation cycles (~7–10 years) will also force the reinvestment decision.

- **Ibiden, Unimicron, and Absolics are furthest along, but ecosystem alignment gaps remain a meaningful hurdle.** No common design rules, panel formats, or reliability standards exist; tooling immaturity and yield stabilization challenges persist at both substrate manufacturers and OSATs. Full commercial alignment has not been achieved.

- **Critical unknowns — system-level yield gains, downstream W2P, and future architecture economics — should anchor the next phase of analysis.** Value allocation across chip companies and data center operators is unquantified. Rubin and Feynman packages will change both yield economics and the magnitude of the glass opportunity.

**Needs more substance:**
- *Bullet 4 (ecosystem readiness)* — accurate but could cite Absolics 2026 target to signal timing urgency
- *Bullet 5 (unknowns)* — intentionally thin; reflects the deck's open-questions close

---

### Observations on Skill Performance

- Draft mode handled a quantitatively dense deck well — scenario W2P ranges, cost ramp figures, and tipping point thresholds all surfaced correctly
- Importance ordering is sound: Scenario 1 vs. 2 distinction is the right lead, not the tipping point analysis (which is slide 4 in the deck but less central to Corning's pricing question)
- "Needs more substance" flags were appropriately conservative — both flagged bullets are accurate, not fabricated; the flags call for specificity, not correction
- First Draft run logged; no prior Draft runs to compare against

---

### Comparison Against Actual SoF (added 4.14.26)

The actual SoF slide was provided after the Draft run for comparison.

**Headline:** The actual leads with savings figures ($410–580 or $100+) and includes a timing caveat ("initial CapEx and mfrg. ramps will delay benefit"). The Draft led with W2P premium percentage and framed Scenario 2 as "marginal to negative." The actual is more balanced — both scenarios presented as legitimate outcomes rather than one clearly dominant. The timing caveat is a meaningful addition the Draft missed.

**What the actual had that the Draft missed:**
- A bullet on the technical performance case for glass (organic cores hitting thermal and density limits >800W, >3GHz, >80–100mm/side). This is a genuine SoF finding — the "why glass is necessary" argument — not just background. The Draft treated it as context and omitted it.
- The organic substrate cost baseline ($165–220, 4% of total cost) as a standalone bullet. The Draft embedded those figures in passing rather than making them explicit. Important for a client building pricing intuition.
- A constructive close with a W2P estimate (~80%+ premium). The Draft closed with an open unknowns bullet, which is less useful for a pricing strategy engagement.

**What the Draft had that the actual didn't:**
- A dedicated adoption triggers bullet (tipping point metrics — package size, yield thresholds, depreciation cycles). The actual folded a few of these into Bullet 1 as supporting detail. The tipping point framing was one of the stated engagement objectives; whether it belongs as a standalone SoF bullet is a judgment call.
- A harder Scenario 1 vs. 2 contrast. Analytically accurate but may not be the right emphasis in a client deliverable where both scenarios represent genuine value.

**Root cause:** Draft mode got the key figures right but missed the narrative structure. The actual SoF tells a story: glass is technically necessary → ecosystem is moving → here's the baseline → here's the value → here's what you can charge. The Draft prioritized the analytical contrast over that arc. The performance-necessity bullet is the most significant structural miss — skipping it weakens the setup for the value argument that follows.

**Implication for skill:** Draft mode may need guidance to distinguish between "context" and "findings that establish necessity" — in a tech-strategy engagement, the technical case for why a transition is coming is a legitimate SoF bullet, not throat-clearing. Hold this observation until a second Draft run confirms whether the pattern repeats before changing the skill.

---

## Draft Run 2: Glass Core Cost Analysis (nosf) — 4.14.26

**Source:** 2025.12.15 Newry Glass Core Cost Analysis - Update - Final _ Revised nosf.pptx (same deck as Run 1)
**Objectives:** Same as Run 1
**Stage / Audience:** Final client deliverable — Corning Confidential
**Input type:** Full PPTX extraction (python-pptx); objectives slide provided (Slide 2)
**Model:** Claude Opus 4.6
**Blind run note:** Partially compromised — memory and Session Startup.md named "technical necessity bullet" as the Run 1 miss. The Draft Run Log was not read before the run, but the label was known. Draft output still missed the bullet, so the failure is genuine; the comparison analysis may not be fully independent.

---

### Quick Take

- **Headline:** Glass core's strongest path to value is eliminating the silicon interposer, justifying a 79–161% substrate premium — but yield ramp and ecosystem alignment remain critical barriers (~168 chars)
- **Scenario structure:** Same Scenario 1 vs. 2 organizing tension as Run 1; W2P ranges correctly stated
- **Technical necessity:** Missing — same as Run 1. No bullet on organic cores hitting physical/thermal limits. Pattern confirmed.
- **Baseline anchoring:** No standalone bullet for organic substrate economics ($165–220, 4% of cost). Figures scattered into other bullets.
- **Narrative arc:** Ordered by economic impact, not by story logic. Jumped to value quantification without establishing why the transition matters.
- **Overall:** Accurate to the material, importance-ordered, quantitatively sound — but same structural gaps as Run 1 across a different model.

---

### Full Draft Output

**Headline:**
> Glass core's strongest path to value is eliminating the silicon interposer, justifying a 79–161% substrate premium — but yield ramp and ecosystem alignment remain critical barriers

**Bullets:**

- **Interposer elimination creates the clearest economic case, with OSAT willingness-to-pay of $295–575 per device versus the current $165–220 organic substrate price.** Removing the silicon interposer saves ~$330–430 in component cost and ~$80–150 in process cost per device, yielding a net benefit even after glass-specific cost adders (~$225–280 at mature production).

- **Improving yield without eliminating the interposer offers modest and uncertain value, with W2P ranging from -$25 to $125.** At certain H100 yield levels glass could have a negative cost impact under this scenario, making it an unreliable standalone value proposition for Corning.

- **Yield ramp is the most critical near-term barrier: early-stage manufacturing adds ~$5,580 per device in incremental cost, declining to ~$225–280 as processes mature over 9–12 months.** Accelerating yield stabilization above 90% is essential for glass to be cost-competitive regardless of adoption scenario.

- **Industry stakeholders broadly expect a 25–200%+ price premium for glass core substrates, with multiple experts citing 2–3x current organic costs.** This range aligns with Newry's bottom-up W2P analysis and suggests market willingness to absorb higher substrate costs where performance benefits are demonstrated.

- **Ecosystem readiness is fragmented — Ibiden, Unimicron, and Absolics appear closest to meaningful capacity, but no player has committed to high-volume glass core production.** Key hurdles include lack of common design rules, insufficient reliability and economic data, and tooling immaturity at both substrate manufacturers and OSATs.

- **Critical unknowns across yield benefit allocation, future device architecture economics, and downstream W2P should guide the next phase of analysis.** Forecasting how glass value creation shifts with Rubin, Feynman, and panel-scale architectures will be essential for Corning's pricing and customer strategy.

**Needs more substance:**
- *Industry stakeholder W2P bullet* — the 25–200% range is wide; the deck presents individual expert quotes but doesn't reconcile them into a view on where the realistic premium settles
- *Ecosystem readiness bullet* — timing of when fragmented readiness resolves is largely absent; the deck flags hurdles but doesn't estimate when they're likely overcome

---

### Comparison Against Actual SoF

**Headline:** Same pattern as Run 1. Both Draft runs led with premium percentage; actual led with dollar savings ($410–580 or $100+) and a timing caveat. The actual headline is more concrete and client-useful.

**What the actual had that the Draft missed (same as Run 1):**
- The technical necessity bullet (organic cores nearing physical/thermal limits). The foundational "why glass" claim. Both runs treated this as context.
- The organic substrate cost baseline as a standalone bullet ($165–220, 4% of total cost, core laminate $16–33). Both runs embedded these figures in passing.
- A constructive close with a W2P estimate (~80%+ premium). Run 2 closed with unknowns; Run 1 also closed with unknowns.

**What this run had that the actual didn't (different from Run 1):**
- Industry stakeholder premium quotes as a standalone bullet (Run 1 didn't have this either)
- More emphasis on ecosystem fragmentation as a standalone finding

**What Run 1 had that this run didn't:**
- A dedicated adoption triggers bullet (tipping points — package size, yield, depreciation cycles)
- The "still adds ~$100 at maturity" point, useful for Corning's pricing floor

**Pattern confirmed across two models:**
1. Technical necessity bullet missed (both runs)
2. Headline leads with percentage premium rather than dollar savings (both runs)
3. Baseline economics not anchored as standalone bullet (both runs)
4. Narrative ordered by economic impact, not story arc (both runs)
5. Quantitative accuracy is strong — figures, ranges, and scenario distinctions are correct (both runs)

---

### Observations on Skill Performance

- The technical necessity miss is now a confirmed pattern across Sonnet 4.6 and Opus 4.6. Root cause is categorization: both models treat foundational claims about market/technology shifts as background rather than findings.
- Partially compromised blind run: knowing the label of the miss didn't prevent it in the draft, but may have biased the comparison. Future Draft tests on different decks should use a cleaner protocol.
- Decision made this session: added Minto's SCR framework reference to Draft mode step 0 to address the categorization gap. The Complication in SCR maps directly to the "technical necessity" class of findings. To be tested on the next Draft run.
- Deferred: annotated example SoFs. Best practices (SCR reference) are cheaper to test first; examples are the fallback if SCR doesn't change output.

---

## Draft Run 3: Glass Core Cost Analysis (nosf) — 4.14.26

**Source:** 2025.12.15 Newry Glass Core Cost Analysis - Update - Final _ Revised nosf.pptx (same deck as Runs 1 & 2)
**Objectives:** Same as prior runs
**Stage / Audience:** Final client deliverable — Corning Confidential
**Input type:** Full PPTX extraction (markitdown); objectives slide provided (Slide 2)
**Model:** Claude Opus 4.6
**Blind run note:** Clean blind run. Session Startup.md and auto-memory were scrubbed of analysis-specific details before this session. Draft Run Log and decisions.md were not read before the run. The skill had been updated with the SCR framework reference after Runs 1 & 2.

---

### Quick Take

- **Headline:** Glass core's strongest value path is interposer elimination, justifying a 79–161% premium over organic — but near-term yield ramps and ecosystem alignment must close first (~156 chars)
- **SCR step:** Explicitly identified SCR structure before drafting. Correctly named organic cores hitting physical/thermal limits as the Complication. But the finding still didn't become a bullet.
- **Technical necessity:** Missing — third consecutive run. The SCR framework improved the analysis step (correct identification) but didn't change the output (no bullet).
- **Baseline anchoring:** No standalone bullet for organic substrate economics. Same as Runs 1 & 2.
- **Headline pattern:** Premium percentage again, not dollar savings. Third time.
- **Overall:** Quantitatively accurate, importance-ordered, same structural gaps. The SCR addition changed the thinking but not the deliverable.

---

### Full Draft Output

**Headline:**
> Glass core's strongest value path is interposer elimination, justifying a 79–161% premium over organic — but near-term yield ramps and ecosystem alignment must close first

**Bullets:**

- **Eliminating the silicon interposer is the most compelling scenario, saving ~$410–580 per device.** Interposer component ($330–430) and interposer-to-substrate attach ($80–150) costs are removed entirely, producing clear net benefits even after accounting for glass's added costs.

- **Yield improvement alone (Scenario 2) offers modest upside and could be net-negative at current H100 yields.** Without interposer elimination, glass core's W2P ranges from -$25 to $125 — meaning at some yield levels, the switch destroys value for the OSAT.

- **Near-term manufacturing costs are the primary barrier: early-stage yields (~40%) add ~$5,580 per device, but costs converge within 12 months.** As yields climb to 90% and inspection rates normalize, incremental glass costs drop to ~$225–280 — manageable against the savings in Scenario 1.

- **Ibiden, Unimicron, and Absolics are closest to meaningful glass core capacity, but full ecosystem alignment is lacking.** No common design rules, panel formats, or reliability standards exist yet; tooling immaturity and OSAT learning curves remain key hurdles.

- **Industry stakeholders broadly validate the premium: experts anticipate 25–200% over organic.** This range brackets Newry's Scenario 1 estimate (79–161%) and reflects both near-term cost uncertainty and long-term conviction in glass's enabling role.

- **Critical unknowns around future device architectures, downstream value creation, and value-chain W2P allocation should guide the next phase of analysis.** Rubin and Feynman platforms will shift economics — rising die costs and lower yields will amplify glass's value, but the magnitude depends on chiplet adoption, panel-scale manufacturing, and CPO integration.

**Needs more substance:**
- *Bullet 6 (critical unknowns)* — aggregates open questions from the deck rather than presenting a finding with quantified support. Directionally important for a final readout but thin on substance.

---

### Comparison Against Actual SoF

**Same structural gaps, third run:**

1. **Technical necessity bullet missing** — despite the SCR step correctly identifying organic cores hitting physical/thermal limits as the Complication. The issue is no longer recognition; it's that the drafting step (ordering by importance) treats it as "obvious setup" rather than a finding.

2. **Headline leads with premium percentage, not dollar savings** — "79–161% premium" vs. the actual's "$410–580 per unit" and "$100+ per unit." Three runs, three percentage-first headlines.

3. **Baseline economics not standalone** — $165–220 and 4% of total cost scattered into other bullets, not anchored as their own finding. Same as both prior runs.

4. **Story arc vs. economic impact ordering** — jumps to interposer elimination value; actual builds: why glass is needed → ecosystem → baseline → value → pricing implication.

**What Run 3 added vs. prior runs:**
- Industry stakeholder pricing validation as a standalone bullet (same as Run 2, absent from Run 1)
- Slightly tighter headline (156 chars vs. 175 and 168)

**What Run 3 didn't have that Run 1 had:**
- Adoption triggers as a standalone bullet (tipping points)
- The "still adds ~$100 at maturity" pricing floor point

---

### Observations on Skill Performance

- **The SCR framework reference improved analysis but not output.** The model correctly identified the technical necessity finding as the Complication in its pre-draft SCR step, then dropped it during bullet construction. The gap is between step 0 (story identification) and steps 1–2 (bullet selection/ordering).
- **Root cause refined:** It's not that the model can't identify what qualifies as a finding (the SCR step proves it can). It's that the drafting steps prioritize "importance to client" as economic magnitude, and the technical necessity finding has no dollar figure attached. Findings without quantified impact get classified as setup.
- **Three runs, two models, one skill update — same four structural gaps.** This is a stable pattern, not noise.
- **Next action for the skill:** The fix needs to operate at the bullet selection step, not the story identification step. Options: (a) add a rule that the SCR Complication must appear as a bullet if it's a finding, (b) add a rule that narrative-arc ordering (not just importance ordering) should be used when the source is a well-constructed deck, (c) add an annotated example. Option (a) is the most targeted. Option (b) overlaps with the existing "follow slide sequence" guidance but could be made more explicit. Option (c) is the heaviest intervention.

---

## Draft Run 4: Glass Core Cost Analysis (nosf) — 4.14.26

**Source:** 2025.12.15 Newry Glass Core Cost Analysis - Update - Final _ Revised nosf.pptx (same deck as Runs 1–3)
**Objectives:** Same as prior runs
**Stage / Audience:** Final client deliverable — Corning Confidential
**Input type:** Full PPTX extraction (markitdown); objectives slide provided (Slide 2)
**Model:** Claude Sonnet 4.6
**Skill state:** Post-Run-3 update — Complication-as-bullet rule added to step 0 ("The Complication is often a finding, not background — if it makes a claim about what is true..., it must appear as a bullet, not just as context in the pre-draft analysis.")
**Blind run note:** Clean blind run. Draft Run Log not read before the run.

---

### Quick Take

- **Headline:** "Glass core commands a 79–161% substrate premium in Scenario 1, but benefits collapse without interposer elimination; yield ramp speed is the critical variable in both cases" (171 chars — within range; premium percentage again, not dollar savings)
- **Technical necessity:** Partially present — a tipping point metrics bullet appeared (first time across all runs), but it was framed as "approaching thresholds" rather than "organic cores hitting physical limits." The SCR Complication rule appears to have moved the needle, though not to the full target.
- **SCR framing:** Misidentified the Complication — labeled it as "economic hurdles of glass adoption" rather than "organic cores hitting physical limits." This may explain why the resulting bullet was tipping-point-focused rather than limits-focused.
- **Baseline anchoring:** No standalone bullet for organic substrate economics. Same as all prior runs.
- **Narrative arc:** Still ordered by economic impact; story arc not followed. Tipping points lead (new) but interposer elimination is bullet 2 rather than preceded by a baseline anchor.
- **Overall:** First run to include a technical-necessity-adjacent bullet. SCR Complication rule appears to have partial effect. Four structural patterns from prior runs; this run may have closed one partially.

---

### Full Draft Output

**Headline:**
> Glass core commands a 79–161% substrate premium in Scenario 1, but benefits collapse without interposer elimination; yield ramp speed is the critical variable in both cases

**Bullets:**

- **Tipping point metrics are approaching for next-generation platforms.** Package sizes for Rubin and Feynman are expected to exceed 100mm per side, wiring pitch is pushing below 2μm L/S, and power density is approaching 700–800W — precisely the thresholds where organic substrate economics break down and glass core becomes enabling.

- **Eliminating the silicon interposer generates $410–580 in OSAT benefits per device, supporting a $295–575 premium over organic substrates at mature yields.** Component savings from removing the interposer ($330–430) and process savings from eliminating interposer-to-substrate attach ($80–150) substantially exceed incremental glass costs (~$225–280 at late-stage manufacturing).

- **Yield improvement alone (Scenario 2) is marginal and may be uneconomic.** Without interposer elimination, glass's warpage-reduction benefit (~$90–130 in yield savings) is nearly offset by new CapEx and inspection costs, yielding a hypothesized W2P of -$25 to +$125 — at or below current organic substrate pricing of $165–220.

- **Early-stage manufacturing costs are severe; yield ramp speed is the most critical lever.** At 40% yield in the first six months, glass adds ~$5,580 per device. This normalizes to ~$160 incremental by month 9–12 at 90%+ yield — making the pace of the ramp the decisive variable for any customer's adoption decision.

- **Substrate manufacturers are not yet ready for high-volume production; Ibiden, Unimicron, and Absolics are furthest along.** No common design rules, panel formats, or reliability standards exist across the industry; all manufacturers face tooling immaturity and yield stabilization challenges, and full ecosystem alignment remains an unresolved hurdle.

- **Significant unknowns must drive next-phase analysis before Corning can finalize pricing and customer strategy.** Downstream W2P beyond the OSAT (chip companies, system integrators), the value impact of future architectures (Rubin, Feynman, chiplets), and value allocation across the chain are all unquantified and likely shift the case for glass considerably.

**Needs more substance:**
- *Tipping point metrics bullet* — the deck lists thresholds but doesn't state how close current platforms are to each one; Rubin package size (>100mm) is noted but the other metrics lack a "current state vs. threshold" comparison
- *Substrate manufacturer readiness* — flattens significant variation; Absolics targeting HVM by 2026 vs. others still in early stages

---

### Comparison Against Actual SoF

**What changed vs. prior runs:**
- A tipping-point/necessity-adjacent bullet appeared for the first time. Not identical to the actual SoF's organic-limits bullet, but in the same category. This is a meaningful improvement.
- Headline length improved (171 chars vs. 156–175 in prior runs).

**What remained the same:**
1. **Headline leads with premium percentage, not dollar savings** — "79–161% premium" again; actual leads with "$410–580 per unit." Four runs, four percentage-first headlines.
2. **Organic substrate baseline not anchored as standalone bullet** — $165–220 and 4% of total cost embedded in passing. Same as all prior runs.
3. **Narrative arc not followed** — tipping points lead, but without an organic-limits framing; no baseline bullet; the story structure (why glass is needed → ecosystem → baseline → value → pricing) is still not reproduced.
4. **Technical necessity framing is off** — the deck's claim is that organic cores are hitting physical limits that force a transition; the Draft's bullet says metrics are "approaching" thresholds, which is softer and descriptive rather than assertive.

**Root cause update:** The Complication rule prompted inclusion of a necessity-adjacent bullet, but the SCR analysis itself misidentified the Complication (as "economic hurdles" rather than "organic hitting limits"). If step 0 produces the wrong Complication, step 1 produces the wrong bullet even with the rule in place. The fix may need to go one level deeper: either give an example of what a correctly identified Complication looks like, or add guidance that the Complication should describe what is true about the *current technology or market*, not what is hard about the transition.

---

### Observations on Skill Performance

- **The Complication-as-bullet rule had partial effect.** A technical-necessity bullet appeared for the first time, but it was framed as "approaching thresholds" rather than "organic hitting limits" — the assertive claim from the actual SoF. Partial credit.
- **The SCR analysis step is still the weak link.** If the model names the wrong Complication in step 0, the Complication rule doesn't produce the right bullet. The rule is necessary but not sufficient.
- **Three of four patterns from prior runs held.** Premium percentage headline, no baseline anchor bullet, no narrative arc ordering.
- **Persistent patterns across four runs and two models are now documented.** The headline pattern in particular (percentage vs. dollar figure) may reflect a default preference that requires an explicit rule or example to override.
- **Recommendation:** Hold on further skill updates until a new deck is tested. The Glass Core deck is now a known case (4 runs); any further improvement here could be deck-specific overfitting. The more useful test is whether the current skill — with the Complication rule — performs on an unfamiliar deck.
