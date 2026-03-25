#!/usr/bin/env bash
set -euo pipefail

input="${1:?usage: render_part.sh path/to/model.scad PART_NAME output.stl}"
part="${2:?usage: render_part.sh path/to/model.scad PART_NAME output.stl}"
output="${3:?usage: render_part.sh path/to/model.scad PART_NAME output.stl}"

openscad -D "PART=\"$part\"" -o "$output" "$input"
echo "Exported part '$part' to $output"