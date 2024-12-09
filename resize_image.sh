#!/usr/bin/env nix-shell
#!nix-shell -i bash -p imagemagick

# Check if all arguments are provided
if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <input_file> <output_file> <x_offset> <y_offset>"
  exit 1
fi

input_file="$1"
output_file="$2"
x_offset="$3"
y_offset="$4"

# Resize the image to fit within 202x202
magick "$input_file" \
  -resize 202x202^ \
  -gravity northwest \
  -extent 202x202 \
  -background white \
  -crop "202x202+$x_offset+$y_offset" \
  -gravity center \
  -background white \
  -extent 202x202 \
  "$output_file"

echo "Image resized, cropped with offset, and padded with white, saved to $output_file"
