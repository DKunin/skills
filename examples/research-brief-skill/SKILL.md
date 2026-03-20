---
name: "research-brief-skill"
description: "Build concise, decision-ready research briefs from notes and source material when the user needs a grounded summary."
---

# Purpose

Use this skill to turn scattered notes, links, transcripts, or source documents into a short research brief that is easy to act on.

# Inputs

- Raw notes or transcripts
- Source links or attached documents
- The decision, question, or audience the brief should support

# Workflow

1. Inventory the available inputs and identify the decision or question the brief must answer.
2. If the notes are messy, normalize them with `scripts/normalize_notes.sh` before drafting.
3. Extract the core claims, risks, unknowns, and source gaps.
4. Use `references/source-evaluation.md` to classify evidence quality and freshness.
5. Draft the brief with the required section order.
6. Verify that every non-obvious claim is backed by a source or labeled as inference.

# Output Contract

The brief should contain these sections in order:

1. Executive Summary
2. Key Findings
3. Risks And Unknowns
4. Open Questions
5. Source Log

# Guardrails

- Separate sourced facts from interpretation.
- Call out stale or weak evidence.
- Do not smooth over disagreements between sources.
- If the material is too thin to support a conclusion, say so plainly.

# References

- Read `references/source-evaluation.md` when weighing credibility or freshness.
- Use `scripts/normalize_notes.sh` when the input is long, noisy, or inconsistently formatted.
