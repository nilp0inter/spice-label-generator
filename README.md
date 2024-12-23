# Spice Label Generator

A Python tool to automatically generate stylish labels for your spice jars.  
Given a CSV input with Spanish and English names for each spice, this tool produces a beautifully rendered SVG label and a corresponding PNG image.

**Key Features**:
- **Clear, Modern Layout:** Each label is split into a top (Spanish) and bottom (English) section, with a bold black separator.
- **Automated Font Sizing:** Text is dynamically scaled to fit the allotted space, ensuring no overflow.
- **Flexible Sizing & Fonts:** Specify font family and canvas size from the command line.
- **Output Formats:** Generates both SVG and PNG files.
- **Simple Input Format:** Provide a CSV with columns "Spanish" and "English" for each spice.

## Quickstart

### Prerequisites

#### Software

- Nix with flakes. 

OR

- Python 3.7+ with Pillow, svgwrite. 
- Imagemagick
- Inkscape

#### Hardware

- [Spice rack](https://www.amazon.es/Relaxdays-Especiero-Giratorio-especias-herm%C3%A9tico/dp/B07KCR9D4B/ref=sr_1_1_sspa?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=12QJTY9ZQKDFS&dib=eyJ2IjoiMSJ9.e4XiYGwkBhDkwrF2zPtMo6dmXcWIIciaWpqbOmMUioo0WUeh_LhcCFyXkb0GnODCepyHba3YfpI8MbVLs6gDnz9owVlK4rXRSTrghK5mBIv4Quf3HKz68L4JmF-TMAm-maZslgAmT_4cgSryoUB_CCqrfLhexYFyE0FR9w1YH8_WVbicIn02swNPelQVGZAsjMc2opQsxMmtnTgwyWMpZf116s_5_7sowjxdziPw3WJvwaE9KodgP0zgeYkORfT3HPYaAyeyMq0UvzkIEpUYmgidc2ebT_5iP5SEXbXTFwU._o13sOINFA-MG62Ian9oNyjpfV8yMpfElqCkdH0xu4I&dib_tag=se&keywords=relaxdays+especiero+xxl&nsdOptOutParam=true&qid=1733785910&sprefix=relaxdays+especiero+xxl%2Caps%2C85&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)
- [Brother QL-800](https://www.brother.es/impresoras-etiquetas-y-recibos/ql-800)

### Usage

#### Label generation

```console
$ nix develop
$ python label_generator.py --input-csv condiments.csv --font-family "Atkinson Hyperlegible" --font-path ./fonts/Atkinson-Hyperlegible-Regular-102.ttf --size 512 --output-dir condiments/ --alt-font-path ./fonts/Meiryo.ttf --alt-font-family Meiryo
$ ./resize_images.sh 202 condiments_top condiments/*.png
$ ./resize_images.sh 306 condiments_front condiments/*.png
$ python label_generator.py --input-csv ingredients.csv --font-family "Atkinson Hyperlegible" --font-path ./fonts/Atkinson-Hyperlegible-Regular-102.ttf --size 696 --output-dir ingredients_label/ --alt-font-path ./fonts/Meiryo.ttf --alt-font-family Meiryo
```

#### Printing

For this step you'll need [brother-ql](https://github.com/pklaus/brother_ql) installed and configured.

**Condiments:**

* Top label: 23x23mm die-cut
* Front label: 29mm endless

**Ingredients:**

* Label: 62mm endless

```console
$ ls -1 condiments_top/*.png | xargs -n5 brother_ql print -l 23x23 --no-cut
$ ls -1 condiments_front/*.png | xargs -n5 brother_ql print -l 29
$ ls -1 ingredients_label/*.png | xargs -n5 brother_ql print -l 62
```

### Result

![preview](./assets/preview.gif)
