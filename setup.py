#!/usr/bin/env python
import os

from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

    # install_requires=find_namespace_packages(include=["quotespy"]),

setup(
    name="quotespy",
    version="0.5",
    description="Python library to create quotes/lyrics graphics with PIL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ze1598/quotespy",
    author="Jose Costa",
    author_email="jose.fernando.costa.1998@gmail.com",
    packages=find_namespace_packages(include=["quotespy*"]),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    zip_safe=False
)