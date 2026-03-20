#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <skill-name> <description> [target-dir]" >&2
}

yaml_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

slugify() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | tr ' ' '-' \
    | tr -cd 'a-z0-9-_'
}

title_case() {
  printf '%s' "$1" \
    | tr '-' ' ' \
    | awk '{
        for (i = 1; i <= NF; i++) {
          $i = toupper(substr($i, 1, 1)) substr($i, 2)
        }
        print
      }'
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

raw_name="$1"
description="$2"
target_dir="${3:-$(slugify "$raw_name")}"
skill_name="$(slugify "$raw_name")"
display_name="$(title_case "$skill_name")"
short_description="$(printf '%s' "$description" | cut -c1-64)"
escaped_description="$(yaml_escape "$description")"
escaped_display_name="$(yaml_escape "$display_name")"
escaped_short_description="$(yaml_escape "$short_description")"

if [[ -e "$target_dir" ]]; then
  echo "Refusing to overwrite existing path: $target_dir" >&2
  exit 1
fi

mkdir -p "$target_dir/agents" "$target_dir/references" "$target_dir/scripts" "$target_dir/assets"

cat > "$target_dir/SKILL.md" <<EOF
---
name: "$skill_name"
description: "$escaped_description"
---

# Purpose

Use this skill when the user needs a repeatable workflow for this task.

# Inputs

- The user goal
- The required source material
- Constraints such as tone, format, or deadlines

# Workflow

1. Confirm the request matches the skill trigger.
2. Gather the minimum required context.
3. Execute the workflow in a deterministic order.
4. Validate the output before returning it.

# Output Contract

- State what the output must contain.
- Define how uncertainty should be labeled.

# Guardrails

- Avoid unsupported claims.
- Surface blockers instead of guessing when missing information changes the result.

# References

- Read files in \`references/\` only when needed.
- Add helper scripts to \`scripts/\` only for fragile or repetitive work.
EOF

cat > "$target_dir/agents/openai.yaml" <<EOF
interface:
  display_name: "$escaped_display_name"
  short_description: "$escaped_short_description"
  default_prompt: "Use \$$skill_name to complete this task."

policy:
  allow_implicit_invocation: true
EOF

echo "Created skill scaffold at $target_dir"
