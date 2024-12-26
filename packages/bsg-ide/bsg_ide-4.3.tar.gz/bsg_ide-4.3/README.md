# Beamer Slide Generator IDE

A customizable IDE for creating Beamer presentations with multimedia support.

## Installation

You can install BSG-IDE directly from PyPI:

```bash
pip install bsg-ide
```

Or install from source:

```bash
git clone https://github.com/sajeethphilip/Beamer-Slide-Generator.git
cd Beamer-Slide-Generator
pip install -e .
```

## Prerequisites

- Python 3.7 or higher
- LaTeX distribution (TeXLive/MikTeX)
- For video presentations: pympress

## Usage

After installation, you can launch BSG-IDE in two ways:

1. From command line:
```bash
bsg-ide
```

2. Import and run programmatically:
```python
from bsg_ide import BeamerSlideEditor
editor = BeamerSlideEditor()
editor.mainloop()
```

## Features

- WYSIWYG Beamer slide editing
- Multimedia support (images, videos, URLs)
- Syntax highlighting
- Live preview
- Presenter notes support
- Export to PDF/Overleaf

## License

This project is licensed under Creative Commons - see the LICENSE file for details.

## Author

Ninan Sajeeth Philip (nsp@airis4d.com)
