#!/usr/bin/env bash
set -euo pipefail

input="${1:?usage: check_scad.sh path/to/model.scad}"

tmp="$(mktemp /tmp/openscad-check-XXXXXX.stl)"
trap 'rm -f "$tmp"' EXIT

openscad -o "$tmp" "$input" >/dev/null 2>&1
echo "OK: $input rendered successfully"