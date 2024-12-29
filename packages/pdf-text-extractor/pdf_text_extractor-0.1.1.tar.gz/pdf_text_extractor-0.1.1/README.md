## PDF Text Extractor

PDF Text Extractor is a Python package for extracting text and images from PDF files. It supports extracting text directly from PDFs as well as from images using OCR (Tesseract).

Features
	•	Extract text directly from PDFs using PyMuPDF.
	•	Extract images embedded in PDFs.
	•	Perform OCR on extracted images using Tesseract.
	•	Export extracted text to Markdown, XML, or dataset formats.
---
## Installation

System Requirements

Before installing, ensure you have the following system requirements met:
-  Python Version: Python 3.12 or newer is required. 
  - Tesseract OCR:
    - Install Tesseract on your system. Instructions for common operating systems:
    - Ubuntu/Debian:
    ```shell
      sudo apt update
      sudo apt install tesseract-ocr libtesseract-dev
      ```
    - macOS (using Homebrew):
    ```shell
    brew install tesseract
    ```
- Pilow Dependencies:
- PyMuPDF (fitz):
	- PyMuPDF is included in the package dependencies.

---
## Python Dependencies

The package has the following Python dependencies:
- pytesseract
- Pillow
- PyMuPDF

You can install all dependencies via pip:
```shell
pip install pdf-text-extractor
```

---
## Usage

1. Install the Package

Install the package via pip:
```shell
pip install pdf-text-extractor
```
2. Import and Use the Library
```python
from pdf_text_extractor.extractor import PDFTextExtractor

# Initialize the extractor
pdf_path = "sample.pdf"
image_dir = "extracted_images"
output_text_file = "output.md"

extractor = PDFTextExtractor(pdf_path, image_dir, output_text_file)

# Extract text and save to Markdown
extractor.extract_and_save_text()

# Convert text to XML
xml_content = extractor.convert_to_xml()
print(xml_content)
```

