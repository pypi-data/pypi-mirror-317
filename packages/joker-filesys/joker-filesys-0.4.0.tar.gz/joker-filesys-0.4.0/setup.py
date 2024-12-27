#!/usr/bin/env python3
# coding: utf-8

import os
import re

from setuptools import setup, find_namespace_packages

# import joker; exit(1)
# DO NOT import your package from your setup.py

description = "Tools dealing with files and directories."


def read(filename):
    with open(filename) as f:
        return f.read()


def version_find():
    root = os.path.dirname(__file__)
    path = os.path.join(root, "joker/filesys/__init__.py")
    regex = re.compile(r"""^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)""")
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError("__version__ definition not found")


config = {
    "name": "joker-filesys",
    "version": version_find(),
    "description": description,
    "keywords": "joker",
    "url": "https://github.com/frozflame/joker-filesys",
    "author": "frozflame",
    "author_email": "frozflame@outlook.com",
    "license": "GNU General Public License (GPL)",
    "packages": find_namespace_packages(include=["joker.*"]),
    "namespace_packages": ["joker"],
    "zip_safe": False,
    "python_requires": ">=3.9",
    "install_requires": read("requirements.txt"),
    "classifiers": [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    # ensure copy static file to runtime directory
    "include_package_data": True,
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
}

setup(**config)
