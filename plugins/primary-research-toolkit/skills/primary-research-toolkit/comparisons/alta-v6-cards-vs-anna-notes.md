# Comparison: Alta v6 Summary Cards vs. AI-from-Anna's-notes Signal Cards

**Date:** 2026-05-04
**Project:** ALTA01 - Growth Strategy
**Purpose:** Assess whether moving from AI-synthesized consultant notes (Anna's source) to raw Otter verbatim transcripts improved summary card quality and attribution.

---

| Dimension | v6 cards (verbatim transcripts) | Anna's-notes cards (AI-synthesized notes) | Observation | Implication for design |
|-----------|--------------------------------|------------------------------------------|-------------|----------------------|
| Evidence specificity | Volumes, percentages, named customers, verbatim quotes present throughout | Findings stated in general terms; specific numbers and named entities largely absent | Denser source material directly flows into richer card evidence | Source input type is the binding constraint on evidence specificity; no prompt engineering fixes a thin source |
| Attribution reliability | 17 High / 28 Medium-High / 10 Medium; zero Low | Attribution largely Medium or lower across corpus | Verbatim transcripts produce consistently higher attribution than synthesized notes | Encourage verbatim transcripts as the default input; synthesized notes are a fallback with declared quality downgrade |
| Quote availability | Near-verbatim quotes present on most High/Medium-High cards | Quotes largely absent or paraphrased at remove | Direct transcript access is required for usable quotation | Mode 1 output quality declaration ("input quality: synthesized notes → attribution: medium") correctly sets expectations |
| Branch coverage detection | Coverage table accurately reflects what the interviewee addressed | Coverage table present but less reliable — synthesized notes may have collapsed or omitted branches | No structural difference in card format; quality difference is in the evidence behind the assessments | No SKILL.md change needed; the existing input-quality flag handles this |

---

**Overall takeaway:** Verbatim transcripts are meaningfully better than AI-synthesized notes as ICS input — not because of structural format differences, but because source density flows directly into evidence specificity and attribution confidence. The existing input-quality declaration in Mode 1 correctly signals this; no format changes needed. Encourage verbatim as default.

**Promoted to decisions.md:** Yes — "Source-material density bounds evidence specificity" entry (2026-05-04).
