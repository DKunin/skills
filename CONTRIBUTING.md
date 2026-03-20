# Contributing

## Scope

Use this repository for reusable AI skills and the tooling required to maintain them. Keep the repository focused on authoring quality, reviewability, and repeatable execution.

## Before You Start

- Read [docs/authoring-guide.md](docs/authoring-guide.md).
- Start from `templates/skill-template/` or use `./scripts/new-skill.sh`.
- Prefer editing one skill or one repo concern per pull request.

## Authoring Rules

- Keep `SKILL.md` concise and procedural.
- Put detailed material in `references/` instead of bloating the main skill file.
- Add scripts only when a manual process is fragile or repeated often.
- Document output format and validation steps inside the skill.
- Keep examples realistic and safe to run in a normal developer environment.

## Pull Request Expectations

- Explain what the new or updated skill is for.
- Describe the trigger condition clearly.
- Summarize validation you ran.
- Call out risks, assumptions, or intentionally deferred work.

## Definition Of Done

- The skill has a clear `name` and `description` in frontmatter.
- `agents/openai.yaml` matches the behavior of the skill.
- The skill contains a usable workflow, output contract, and guardrails.
- Validation passes:

  ```bash
  ./scripts/validate-skills.sh
  ```

- Documentation changes are included when repository-level conventions change.

## Review Standard

Reviewers should reject changes that are vague, overly long, unsafe, or impossible to validate from the repository contents.
