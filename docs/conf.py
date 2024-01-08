# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'vscode.py'
copyright = '2024, CodeWithSwastik'
author = 'CodeWithSwastik'
release = '2.0.0'

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

source_parsers = {'.md': 'recommonmark.parser.CommonMarkParser'}
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_logo = "../images/vscode-ext.png"
html_title = f"{project} {release}"
html_theme = 'furo'
html_favicon = "../images/vscode-ext.png"
html_static_path = ['_static']

