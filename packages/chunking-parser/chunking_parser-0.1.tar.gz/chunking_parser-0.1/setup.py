from setuptools import setup, find_packages

setup(
    name="chunking_parser",
    version="0.1",
    packages=find_packages(),
    install_requires=["fastapi", "pymupdf", "pytesseract", "setuptools"],  # Add dependencies if any
    description="A library to get the chunks of text from file",
    author="Aashish sharma",
    author_email="aashish@oppdoor.com",
    url="https://github.com/yourusername/my_library",  # Update URL
)

