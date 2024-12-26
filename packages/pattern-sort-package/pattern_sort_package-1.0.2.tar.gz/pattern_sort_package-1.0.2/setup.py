from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name="pattern_sort_package",  # package name
    version="1.0.2",  # Initial version
    author="Abu Awaish",
    author_email="abuawaish7@gmail.com",
    description="A Python package for pattern generation and sorting algorithms.",
    long_description=long_description,
    long_description_content_type="text/x-rst",  # Use Markdown for README
    url="https://github.com/abuawaish/awaish_pkg",  # repository URL
    packages=find_packages(),  # Automatically find sub-packages,
    license="MIT",
    keywords="funny",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the minimum Python version
    install_requires=[],  # List of dependencies (if any)
    include_package_data=True,  # Include files specified in MANIFEST.in
)
