# AI Skills Starter Repository

This repository is a clean starting point for building reusable AI skills.

A skill is a self-contained folder that teaches an AI agent how to handle a repeatable task. Each skill combines concise instructions, optional reference material, optional helper scripts, and lightweight UI metadata.

## What This Repository Includes

- A documented skill authoring standard
- A reusable skill template
- A worked example skill
- Bootstrap and validation scripts
- Basic GitHub project hygiene files

## Quick Start

1. Create a new skill scaffold:

   ```bash
   ./scripts/new-skill.sh customer-support-triage "Handle incoming support requests and turn them into clear triage summaries."
   ```

2. Edit the generated `SKILL.md` and `agents/openai.yaml`.
3. Add references or scripts only when they materially improve reliability.
4. Validate every skill in the repository:

   ```bash
   ./scripts/validate-skills.sh
   ```

## Skill Anatomy

Every skill should follow this shape:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
└── assets/
```

### Required Files

- `SKILL.md`: Trigger description, workflow, output contract, and guardrails
- `agents/openai.yaml`: User-facing metadata and default invocation prompt

### Optional Directories

- `references/`: Supporting material that should be loaded only when needed
- `scripts/`: Deterministic helpers for fragile or repetitive work
- `assets/`: Non-context resources used in outputs

## Repository Layout

- `docs/authoring-guide.md`: Writing guidance and quality bar
- `docs/review-checklist.md`: Review checklist before merge
- `templates/skill-template/`: Starting point for new skills
- `examples/research-brief-skill/`: Concrete example of a production-quality skill
- `scripts/new-skill.sh`: Bootstrap a new skill folder
- `scripts/validate-skills.sh`: Validate basic repository conventions

## Доступные навыки

- `editorial-feedback`: приоритетный редакторский разбор текста по полноте, ясности, точности, устойчивости, доступности и соответствию цели.
- `spt-team-stats`: сбор статистики SPT-багов команды за период, построение графиков и публикация отчёта в Confluence.

## Quality Bar

- Trigger descriptions are specific enough that the skill does not misfire.
- Instructions are procedural, not essay-style.
- References stay outside `SKILL.md` unless they are core to execution.
- Scripts exist only when determinism or repetition justifies them.
- Outputs clearly separate facts, assumptions, and open questions.

## Contribution Flow

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Authoring guidance lives in [docs/authoring-guide.md](docs/authoring-guide.md), and the review checklist lives in [docs/review-checklist.md](docs/review-checklist.md).

## License

MIT. See [LICENSE](LICENSE).
