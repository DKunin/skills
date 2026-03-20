# Review Checklist

Use this checklist before merging a new or updated skill.

## Trigger And Scope

- Does the `description` say what the skill does and when it should be used?
- Is the trigger narrow enough to avoid accidental invocation?
- Is the scope realistic for a single skill?

## Workflow Quality

- Does `SKILL.md` contain concrete steps instead of generic advice?
- Are inputs, outputs, and validation criteria explicit?
- Are risky operations called out clearly?

## Context Efficiency

- Is `SKILL.md` concise?
- Is bulky detail moved into `references/`?
- Are optional resources referenced only when needed?

## Metadata

- Does `agents/openai.yaml` match the behavior of the skill?
- Does `default_prompt` explicitly mention `$skill-name`?
- Is the short description understandable in isolation?

## Validation

- Did `./scripts/validate-skills.sh` pass?
- Were any included helper scripts exercised at least once?
- Is there an example or clear evidence the skill can be used as written?
