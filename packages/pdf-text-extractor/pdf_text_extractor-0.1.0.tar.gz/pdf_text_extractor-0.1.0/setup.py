from setuptools import setup, find_packages
import os


def parse_requirements(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]


setup(
    name="pdf-text-extractor",
    version="0.1.0",
    description="Extract text and images from PDF files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/baxromov/pdf-text-extractor",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)