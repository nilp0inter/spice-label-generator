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
- [Python 3.7+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/) for dependency management
- A suitable TTF font file on your system to use (e.g., Arial.ttf)

### Installation

```bash
# Install project dependencies
poetry install

# Activate the virtual environment
poetry shell

