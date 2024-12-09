#!/usr/bin/env bash

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <size> <output_directory> <file1> [<file2> ...]"
  exit 1
fi

size="$1"
output_dir="$2"
shift 2

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Feed the remaining arguments (files) into xargs
# -P8 runs 8 jobs in parallel (adjust as needed)
# We use `sh -c` to properly handle expansions.
printf '%s\n' "$@" | xargs -P8 -I{} sh -c '
f="$1"
d="$2"
base=$(basename "$f")
magick "$f" -resize '"${size}x${size}"' "$d/$base"
' _ {} "$output_dir"
