# Project Technical Onboarding Plugin

Guides Newry consultants through building a Technical Orientation document at the start of any new client engagement.

## Overview

The **Technical Orientation** skill runs a structured, collaborative interview with the consultant to map the client's technology, customer value, competitive position, and key open questions. It produces a formatted .docx artifact that the consultant shares with the project team during week 1.

The skill is designed to be a thinking partner — not a form-fill. It pushes back on vague answers, contributes hypotheses based on sector and competitive knowledge, and helps the consultant produce a sharper document than they would alone.

## Skills

| Skill | Trigger | Output |
|---|---|---|
| `technical-orientation` | "start technical orientation", "build tech orientation", "project technical orientation", "tech orientation doc" | .docx Technical Orientation document |

## Usage

Invoke the skill at the start of a new engagement:

> "Start a technical orientation for the [Client] engagement"

The skill will:
1. Tell you what inputs to gather before the interview starts
2. Walk through five sections via guided conversation
3. Produce a formatted .docx artifact named `[Client] Technical Orientation — [Project Code].docx`

## Artifact Sections

1. **Product/Technology** — What the product does and how it works
2. **Customer Value** — Who buys it, why, and what it costs them not to have it
3. **Technical Position** — Where the client wins technically (differentiated play) or where they win commercially (commodity play), including a table stakes checklist
4. **Competitive Landscape** — Who plays, their technical approaches, and how the client stacks up
5. **Key Open Questions** — Unresolved technical questions, how they get answered, and by whom

## Setup

No environment variables or external connectors required. The skill uses Claude's built-in file tools and Node.js (docx-js) for document generation.

Requires: `npm install -g docx`
