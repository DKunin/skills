---
name: "your-skill-name"
description: "Explain what this skill does and when it should be used."
---

# Purpose

Use this skill when the user needs a repeatable workflow for a clearly defined task.

# Inputs

- The user goal
- Any required source material, files, or links
- Constraints such as format, tone, or deadlines

# Workflow

1. Confirm the task fits the trigger condition for this skill.
2. Identify missing information and make only the minimum necessary assumptions.
3. Follow the core task procedure in a deterministic order.
4. Use supporting references or scripts only when they improve reliability.
5. Validate the output before returning it.

# Output Contract

- State what the output must contain.
- Specify how to label uncertainty, risks, or open questions.
- Define any required formatting.

# Guardrails

- Avoid unsupported claims.
- Do not hide missing inputs or missing evidence.
- Stop and surface blockers when assumptions would materially change the result.

# References

- Read files in `references/` only when they are directly relevant.
- Use helper scripts in `scripts/` when the task is fragile or repetitive.
