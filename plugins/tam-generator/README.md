# TAM Generator

A guided, defensible TAM/SAM/SOM analysis tool for niche and industrial markets.

## What it does

This plugin walks your team through a structured, triangulated market sizing process — the kind that holds up to board and investor scrutiny. It works interactively: team members can upload research, paste call notes, and iterate on assumptions in real time.

## Skills

### `tam-analysis` — Core market sizing workflow

Trigger: "size the market for X", "help me build a TAM", "what's the TAM for [market]"

Runs a full guided analysis:
1. Defines the market precisely (including the key unit metric)
2. Inventories all existing research the user has
3. Runs up to 4 triangulation methods (top-down, bottom-up, value-theory, comparable transactions)
4. Reconciles estimates into a defensible range
5. Derives SAM and SOM with explicit filters
6. Runs a defensibility audit before finalizing
7. Outputs a structured, cited summary

### `source-evaluator` — Data source quality review

Trigger: "is this a good source", "can I cite this", "evaluate this report"

Rates any source against a 4-tier quality framework and tells you exactly what it can and can't support in an investor-grade analysis.

### `assumption-auditor` — Adversarial stress test

Trigger: "audit my assumptions", "stress test this TAM", "what would an investor push back on"

Applies an adversarial review to an existing TAM analysis — finds vulnerabilities before a skeptic does, ranked by impact.

## How to use it

1. Start with `tam-analysis` and describe the specific market you want to size
2. When asked, share everything you already have — call notes, reports, data files — by uploading or pasting directly in chat
3. Work through the analysis iteratively; you can add new data at any point
4. Use `assumption-auditor` on the finished analysis before presenting it
5. Use `source-evaluator` anytime you're unsure about a specific source

## Design principles

- **Defensibility first**: Every number needs a named source. Every estimate needs triangulation.
- **Transparent math**: Formulas and inputs are always shown explicitly.
- **Niche-market ready**: Built for industrial B2B markets where general analyst reports are sparse or unreliable. Includes source guides for aquaculture, water treatment, filtration, and other specialized verticals.
- **Iterative**: Designed for back-and-forth dialogue, not one-shot analysis.
