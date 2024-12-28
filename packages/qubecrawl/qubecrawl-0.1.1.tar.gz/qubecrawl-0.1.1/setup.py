from setuptools import setup, find_packages

setup(
    name = "qubecrawl",
    version = "0.1.1",
    packages=find_packages(where="src"),
    install_requires=[
        "beautifulsoup4",
        "html2text",
        "lxml"
    ],
    extras_require={
        "dev": [
            "twine",
        ]
    },
    author="Adhishtanaka Thiramithu Kulasooriya",
    author_email = "kulasoooriyaa@gmail.com",
    description = "qubecrawl is a lightweight and LLLM friendly Webscraper that extracts HTML content and converts it into clean, readable Markdown to reduce token.",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/adhishtanaka/qubecrawl",
    project_urls = {
        "Bug Tracker": "https://github.com/adhishtanaka/qubecrawl/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    python_requires = ">=3.8"
)