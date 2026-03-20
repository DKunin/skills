# Skill Authoring Guide

## Design Goal

A good skill narrows ambiguity. It should help an agent take the right path faster without overwhelming the context window.

## Recommended Skill Structure

### `SKILL.md`

Keep this file lean and practical. It should usually contain:

1. Purpose
2. When to use the skill
3. Expected inputs
4. Workflow
5. Output contract
6. Guardrails or safety constraints
7. Pointers to `references/` or `scripts/`

### `agents/openai.yaml`

Use this file for user-facing metadata:

- `display_name`: Human-readable name
- `short_description`: Short UI blurb
- `default_prompt`: One-sentence example prompt that explicitly names the skill as `$skill-name`

### Optional Resources

- `references/`: For detailed schemas, policies, or domain rules
- `scripts/`: For deterministic helpers or repetitive transforms
- `assets/`: For templates or files used in generated outputs

## Writing Rules

- Write the trigger condition as narrowly as possible.
- Prefer imperative steps over general advice.
- State what the output must contain.
- Mark any requirement that is mandatory versus best effort.
- Separate facts from inference when the skill produces analysis.

## Context Discipline

- Keep `SKILL.md` under roughly 500 lines unless there is a strong reason not to.
- Move long examples and domain reference material into `references/`.
- Avoid repeating the same information in multiple files.

## When To Add A Script

Add a helper script when:

- The same transformation would otherwise be rewritten often
- Small implementation differences would create risk
- The task benefits from a stable input/output contract

Do not add scripts just to look complete.

## Common Failure Modes

- Trigger text is so broad that the skill becomes noisy
- The workflow reads like a blog post instead of an operator checklist
- Output requirements are implied rather than stated
- The skill assumes information that may not exist in the user prompt
- Helper scripts are included but never referenced from the workflow
