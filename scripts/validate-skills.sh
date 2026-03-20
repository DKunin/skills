#!/usr/bin/env bash

set -euo pipefail

status=0
found=0

fail() {
  echo "ERROR: $1" >&2
  status=1
}

validate_frontmatter() {
  local file="$1"

  awk '
    NR == 1 {
      if ($0 != "---") {
        exit 1
      }
      in_frontmatter = 1
      next
    }
    in_frontmatter == 1 && /^name:[[:space:]]*[^[:space:]].*/ {
      name_found = 1
    }
    in_frontmatter == 1 && /^description:[[:space:]]*[^[:space:]].*/ {
      description_found = 1
    }
    in_frontmatter == 1 && /^---$/ {
      closed = 1
      exit !(name_found && description_found)
    }
    END {
      if (NR == 0 || !closed) {
        exit 1
      }
    }
  ' "$file"
}

while IFS= read -r skill_file; do
  found=1
  skill_dir="$(dirname "$skill_file")"
  meta_file="$skill_dir/agents/openai.yaml"
  line_count="$(wc -l < "$skill_file" | tr -d ' ')"
  skill_name="$(awk '
    NR == 1 && $0 == "---" {
      in_frontmatter = 1
      next
    }
    in_frontmatter == 1 && /^name:[[:space:]]*/ {
      sub(/^name:[[:space:]]*/, "", $0)
      gsub(/^"/, "", $0)
      gsub(/"$/, "", $0)
      print
      exit
    }
    in_frontmatter == 1 && /^---$/ {
      exit
    }
  ' "$skill_file")"

  echo "Validating $skill_dir"

  if ! validate_frontmatter "$skill_file"; then
    fail "$skill_file is missing valid frontmatter with name and description"
  fi

  if ! grep -q '^# ' "$skill_file"; then
    fail "$skill_file must contain at least one top-level heading"
  fi

  if (( line_count > 500 )); then
    fail "$skill_file exceeds 500 lines; move bulk detail into references/"
  fi

  if [[ ! -f "$meta_file" ]]; then
    fail "$meta_file is missing"
    continue
  fi

  if ! grep -q 'display_name:' "$meta_file"; then
    fail "$meta_file is missing interface.display_name"
  fi

  if ! grep -q 'short_description:' "$meta_file"; then
    fail "$meta_file is missing interface.short_description"
  fi

  if ! grep -q 'default_prompt:' "$meta_file"; then
    fail "$meta_file is missing interface.default_prompt"
  elif [[ -n "$skill_name" ]] && ! grep -Fq "\$$skill_name" "$meta_file"; then
    fail "$meta_file default_prompt must explicitly reference \$$skill_name"
  fi
done < <(find . -path '*/.git' -prune -o -name 'SKILL.md' -print | sort)

if [[ "$found" -eq 0 ]]; then
  fail "No skills were found"
fi

if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

echo "Skill validation passed"
