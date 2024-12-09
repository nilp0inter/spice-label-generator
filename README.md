# Spice Label Generator

A modern Python tool to automatically generate stylish labels for your spice jars.  
Given a CSV input with Spanish and English names for each spice, this tool produces a beautifully rendered SVG label and a corresponding PNG image.

**Key Features**:
- **Clear, Modern Layout:** Each label is split into a top (Spanish) and bottom (English) section, with a bold black separator.
- **Automated Font Sizing:** Text is dynamically scaled to fit the allotted space, ensuring no overflow.
- **Flexible Sizing & Fonts:** Specify font family and canvas size from the command line.
- **Output Formats:** Generates both SVG and PNG files.
- **Simple Input Format:** Provide a CSV with columns "Spanish" and "English" for each spice.

## Quickstart

### Prerequisites

- Nix with flakes. 

OR

- Python 3.7+ with Pillow, svgwrite. 
- Imagemagick
- Inkscape

### Usage

```console
$ nix develop
$ python label_generator.py --input-csv condiments.csv --font-family "Atkinson Hyperlegible" --font-path ./fonts/Atkinson-Hyperlegible-Regular-102.ttf --size 512 --output-dir output/ --alt-font-path ./fonts/Meiryo.ttf --alt-font-family Meiryo
$ ./resize_images.sh 202 tops output/*.png
$ ls -1 tops/*.png | xargs -n5 brother_ql print -l 23x23 --no-cut
$ ./resize_images.sh 306 labels output/*.png
$ ls -1 labels/*.png | xargs -n5 brother_ql print -l 29
```

### Result


