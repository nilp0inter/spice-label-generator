import argparse
import csv
import os
import re
from PIL import ImageFont
import svgwrite
import cairosvg

def sanitize_filename(text):
    filename = re.sub(r'[^a-zA-Z0-9\s_-]', '', text)
    filename = filename.strip().replace(' ', '_')
    return filename

def break_line_chars(font, text, max_width):
    chars = list(text)
    lines = []
    current_line = []
    for ch in chars:
        test_line = ''.join(current_line + [ch])
        if font.getlength(test_line) <= max_width:
            current_line.append(ch)
        else:
            if not current_line:
                current_line.append(ch)
            lines.append(''.join(current_line))
            current_line = [ch]
            if font.getlength(''.join(current_line)) > max_width:
                lines.append(''.join(current_line))
                current_line = []
    if current_line:
        lines.append(''.join(current_line))
    return lines

def wrap_text_by_words(font, text, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word]) if current_line else word
        if font.getlength(test_line) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            if font.getlength(word) <= max_width:
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def ensure_no_horizontal_overflow(font, lines, max_width):
    final_lines = []
    for line in lines:
        if font.getlength(line) > max_width:
            char_lines = break_line_chars(font, line, max_width)
            final_lines.extend(char_lines)
        else:
            final_lines.append(line)
    return final_lines

def fit_text_to_area(text, font_path, max_width, max_height, max_font_size=200, min_font_size=10):
    best_font_size = min_font_size
    best_lines = [text]  # fallback lines if nothing fits

    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = ImageFont.truetype(font_path, font_size)
        ascent, descent = font.getmetrics()
        line_height = max(ascent + descent, 1)

        lines = wrap_text_by_words(font, text, max_width)
        lines = ensure_no_horizontal_overflow(font, lines, max_width)

        total_height = line_height * len(lines)
        best_font_size = font_size
        best_lines = lines

        if total_height <= max_height:
            return font_size, lines

    return best_font_size, best_lines

def draw_text_in_svg(dwg, x, y, lines, font_family, font_size, fill, line_height):
    current_y = y
    for line in lines:
        dwg.add(dwg.text(line, insert=(x, current_y), fill=fill,
                         style=f"font-family:{font_family};font-size:{font_size}px;text-anchor:middle;"))
        current_y += line_height

def main():
    parser = argparse.ArgumentParser(description="Generate labels from a CSV file.")
    parser.add_argument('--input-csv', required=True, help='Path to the input CSV file.')
    parser.add_argument('--font-family', required=True, help='Font family name (e.g., Arial).')
    parser.add_argument('--font-path', required=True, help='Path to a .ttf font file.')
    parser.add_argument('--size', type=int, required=True, help='Size of the square canvas (e.g., 512).')
    parser.add_argument('--output-dir', required=True, help='Directory to save output files.')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    canvas_size = args.size
    top_area_height = canvas_size // 2
    bottom_area_height = canvas_size // 2
    separator_height = 8
    bar_width = int(canvas_size * 0.4)

    with open(args.input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            spanish_text = row.get('Spanish', '').strip()
            english_text = row.get('English', '').strip()

            if not spanish_text or not english_text:
                continue

            filename_base = sanitize_filename(spanish_text)
            svg_filename = os.path.join(args.output_dir, f"{filename_base}.svg")
            png_filename = os.path.join(args.output_dir, f"{filename_base}.png")

            # Robust check for "identical" text: lowercased, no spaces
            spanish_norm = spanish_text.replace(" ", "").lower()
            english_norm = english_text.replace(" ", "").lower()

            if spanish_norm == english_norm:
                # Single text block for the entire canvas
                max_width_full = canvas_size - 20
                max_height_full = canvas_size - 20
                font_size, lines = fit_text_to_area(
                    spanish_text,
                    args.font_path,
                    max_width_full,
                    max_height_full
                )

                font = ImageFont.truetype(args.font_path, font_size)
                ascent, descent = font.getmetrics()
                line_height = max(ascent + descent, 1)
                total_height = line_height * len(lines)

                # Center horizontally and vertically in the full canvas
                x = canvas_size / 2
                y_start = (canvas_size - total_height) / 2 + ascent

                dwg = svgwrite.Drawing(svg_filename, size=(canvas_size, canvas_size))
                dwg.add(dwg.rect(insert=(0,0), size=(canvas_size, canvas_size), fill='white'))
                # No separator drawn
                draw_text_in_svg(dwg, x, y_start, lines, args.font_family, font_size, "black", line_height)

            else:
                # Different texts for top and bottom areas
                separator_y = top_area_height
                bar_x = (canvas_size - bar_width) / 2
                bar_y = separator_y - (separator_height / 2)

                max_width_top = canvas_size - 20
                max_height_top = top_area_height - 20
                top_font_size, top_lines = fit_text_to_area(
                    spanish_text,
                    args.font_path,
                    max_width_top,
                    max_height_top
                )

                max_width_bottom = canvas_size - 20
                max_height_bottom = bottom_area_height - 20
                bottom_font_size, bottom_lines = fit_text_to_area(
                    english_text,
                    args.font_path,
                    max_width_bottom,
                    max_height_bottom
                )

                font_top = ImageFont.truetype(args.font_path, top_font_size)
                ascent_top, descent_top = font_top.getmetrics()
                line_height_top = max(ascent_top + descent_top, 1)

                font_bottom = ImageFont.truetype(args.font_path, bottom_font_size)
                ascent_bottom, descent_bottom = font_bottom.getmetrics()
                line_height_bottom = max(ascent_bottom + descent_bottom, 1)

                top_total_height = line_height_top * len(top_lines)
                bottom_total_height = line_height_bottom * len(bottom_lines)

                top_x = canvas_size / 2
                bottom_x = canvas_size / 2

                top_of_block = (top_area_height - top_total_height) / 2
                top_y = top_of_block + ascent_top

                bottom_of_block = (bottom_area_height - bottom_total_height) / 2
                bottom_y = separator_y + separator_height + bottom_of_block + ascent_bottom

                dwg = svgwrite.Drawing(svg_filename, size=(canvas_size, canvas_size))
                dwg.add(dwg.rect(insert=(0,0), size=(canvas_size, canvas_size), fill='white'))
                # Draw separator
                dwg.add(dwg.rect(insert=(bar_x, bar_y), size=(bar_width, separator_height), fill='black'))

                draw_text_in_svg(dwg, top_x, top_y, top_lines, args.font_family, top_font_size, "black", line_height_top)
                draw_text_in_svg(dwg, bottom_x, bottom_y, bottom_lines, args.font_family, bottom_font_size, "black", line_height_bottom)

            dwg.save()
            cairosvg.svg2png(url=svg_filename, write_to=png_filename)
            print(f"Generated: {svg_filename} and {png_filename}")

if __name__ == '__main__':
    main()
