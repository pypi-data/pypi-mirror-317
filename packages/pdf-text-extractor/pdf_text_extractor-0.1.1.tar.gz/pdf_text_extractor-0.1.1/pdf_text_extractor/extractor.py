import concurrent.futures
import io
import os
import xml.etree.ElementTree as ET

import fitz
import pytesseract
from PIL import Image


class PDFTextExtractor:
    def __init__(self, pdf_path, image_dir, output_text_file: str = 'output.md'):
        """Initialize with PDF path, image directory, and output file."""
        self.pdf_path = pdf_path
        self.image_dir = image_dir
        self.output_text_file = output_text_file
        self.pdf_text = ""
        self.image_texts = []

    def extract_images_from_pdf(self):
        """Extract images from the PDF and save them as PNG files."""
        doc = fitz.open(self.pdf_path)
        image_paths = []

        # Loop through each page in the PDF
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            img_list = page.get_images(full=True)

            # Extract and save images from the current page
            for img_index, img in enumerate(img_list):
                xref = img[0]
                image = doc.extract_image(xref)
                image_bytes = image["image"]

                img = Image.open(io.BytesIO(image_bytes))

                img_filename = f"image_{page_num + 1}_{img_index + 1}.png"
                img_path = os.path.join(self.image_dir, img_filename)
                img.save(img_path)

                image_paths.append(img_path)

        return image_paths

    def extract_text_from_image(self, image_path):
        """Extract text from an image using Tesseract OCR."""
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text

    def extract_text_from_images_parallel(self, image_paths):
        """Extract text from a list of images in parallel."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            texts = list(executor.map(self.extract_text_from_image, image_paths))
        return texts

    def extract_text_from_pdf(self):
        """Extract text directly from the PDF using PyMuPDF."""
        doc = fitz.open(self.pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        self.pdf_text = text

    def save_text_to_markdown(self):
        """Save the extracted text to a markdown file."""
        with open(self.output_text_file, 'w') as f:
            if self.pdf_text.strip():
                f.write("### PDF Text\n")
                f.write(self.pdf_text + "\n\n")

            for text in self.image_texts:
                if text.strip():
                    f.write("### Image Text\n")
                    f.write(text + "\n\n")
                else:
                    f.write("### Image Text\n")
                    f.write("\n\n")

    def convert_to_dict(self):
        extracted_data = []

        if self.pdf_text.strip():
            extracted_data.append({"text": self.pdf_text.strip()})

        for text in self.image_texts:
            if text.strip():
                extracted_data.append({"image_text": text.strip()})

        return extracted_data

    def convert_to_markdown(self):
        """Convert the extracted text to a markdown string."""
        markdown_str = ""

        if self.pdf_text.strip():
            markdown_str += "### PDF Text\n"
            markdown_str += self.pdf_text + "\n\n"

        for text in self.image_texts:
            if text.strip():
                markdown_str += "### Image Text\n"
                markdown_str += text + "\n\n"
            else:
                markdown_str += "### Image Text\n"
                markdown_str += "\n\n"

        return markdown_str

    def convert_to_dataset(self):
        """Convert the extracted text to a dataset (list of dictionaries)."""
        dataset = []

        if self.pdf_text.strip():
            dataset.append({
                "text_type": "pdf",
                "text_content": self.pdf_text.strip()
            })

        for text in self.image_texts:
            if text.strip():
                dataset.append({
                    "text_type": "image",
                    "text_content": text.strip()
                })

        return dataset

    def convert_to_xml(self):
        """Convert the extracted text to XML format."""
        root = ET.Element("extracted_text")

        if self.pdf_text.strip():
            pdf_element = ET.SubElement(root, "pdf_text")
            pdf_element.text = self.pdf_text.strip()

        for text in self.image_texts:
            if text.strip():
                image_element = ET.SubElement(root, "image_text")
                image_element.text = text.strip()

        tree = ET.ElementTree(root)
        xml_str = ET.tostring(root, encoding="unicode", method="xml")

        return xml_str

    def extract_and_save_text(self):
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        image_paths = self.extract_images_from_pdf()

        self.image_texts = self.extract_text_from_images_parallel(image_paths)

        self.extract_text_from_pdf()

        self.save_text_to_markdown()

        print(f"Text extraction complete. Output saved to {self.output_text_file}")
