#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 [notes-file]" >&2
  echo "Reads from stdin when no file is provided." >&2
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -gt 1 ]]; then
  usage
  exit 1
fi

input="${1:-/dev/stdin}"

awk '
  BEGIN {
    print "# Normalized Notes"
    print ""
  }
  /^[[:space:]]*$/ {
    next
  }
  {
    line = $0
    sub(/^[[:space:]]*[-*0-9.)]+[[:space:]]*/, "", line)
    gsub(/[[:space:]]+/, " ", line)
    print "- " line
  }
' "$input"
