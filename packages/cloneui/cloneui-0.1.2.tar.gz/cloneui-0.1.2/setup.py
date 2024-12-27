from setuptools import setup, find_packages
from os import path

# Read the content of README.md
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cloneui",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    description="CloneUI is a Python library designed to clone a webpage into a structured folder format effortlessly.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensure markdown is supported
    author="Dhruv Ahir",
    author_email="incnogeto@gmail.com",
    url="https://github.com/yourusername/cloneui",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
