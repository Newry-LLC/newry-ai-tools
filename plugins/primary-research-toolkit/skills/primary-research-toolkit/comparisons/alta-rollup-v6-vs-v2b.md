# Comparison: Alta Roll-up v6 vs. v2b

**Date:** 2026-05-04
**Project:** ALTA01 - Growth Strategy
**Purpose:** Understand why v2b produced sharper pyramid headlines than v6 despite v6 having denser source material and more complete coverage.

---

| Dimension | v6 Roll-up (55 cards, single-pass) | v2b Roll-up (~10 cards, earlier run) | Observation | Implication for design |
|-----------|-----------------------------------|--------------------------------------|-------------|----------------------|
| Headline sharpness | Headlines describe topics ("Commercial execution challenges") | Headlines deliver structural verdicts ("execution-constrained, not demand-constrained"; "Phase 2 pricing as deal thesis") | v2b headlines pass the pyramid test; v6 headlines are largely topic labels | Mode 2 synthesis quality is a prompt/process problem, not a source problem — both runs were AI-throughout |
| Narrative arc | Comprehensive but reads as an aggregation; main messages feel like a list | Tighter narrative with a discernible argument across main messages | Single-pass synthesis over 55 cards loses the consultant-narrative arc that v2b preserved | Multi-pass architecture (per-branch extraction → branch synthesis → summary synthesis) should recover this |
| Evidence comprehensiveness | High — volumes, percentages, contradictions, named entities throughout | Lower — findings stated with less specific backing | v6 is clearly richer in evidence; trade-off is that comprehensiveness came at the cost of narrative tightness | Evidence richness and narrative tightness are separable — the goal is to achieve both via decomposed synthesis |
| Contradictions surfaced | Explicit Contradictions subsections in each branch | Fewer contradictions surfaced; some tensions implicit only | v6's full-corpus scale surfaces more genuine disagreement | No change needed here; contradiction surfacing improves with corpus size |
| Bullet discipline | 8–10 bullets per branch in several sections; violated the 4–6 cap | Closer to 4–6 bullets per section | Bullet count drifts up under context pressure — model enumerates rather than synthesizes | Harden "4–6 dense bullets" to a hard cap in SKILL.md; add calibration examples |

---

**Overall takeaway:** v6's quality gap vs. v2b is explained by two factors: (1) context-window pressure from synthesizing 55 cards in a single pass, causing enumeration over synthesis and topic headlines over verdicts; (2) insufficiently enforced bullet cap allowing drift to 8–10 per section. Fix: decompose Mode 2 into a 4-pass pipeline (route → extract → branch synthesis → summary synthesis) and harden the bullet cap. Source quality is not the issue — both runs used AI-generated inputs.

**Promoted to decisions.md:** Pending — will add "Mode 2 decomposed into 4-pass pipeline" entry when the SKILL.md change ships.
