#!/usr/bin/env python
import os

from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="quotespy",
    version="1.2",
    description="Python library to create quotes/lyrics and tweet graphics with PIL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ze1598/quotespy",
    author="Jose Costa",
    author_email="jose.fernando.costa.1998@gmail.com",
    packages=find_namespace_packages(include=["quotespy*"]),
    install_requires=[
        "pillow>=7.1.2",
        "typing-extensions>=3.7.4.2"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    zip_safe=False
)
