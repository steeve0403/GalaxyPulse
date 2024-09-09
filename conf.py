import os
import sys
sys.path.insert(0, os.path.abspath('./'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GalaxyPulse'
copyright = '2024, Z-Dezign'
author = 'Z-Dezign'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/.venv/**']

language = 'en'

htlm_theme = 'sphinx_rtd_theme'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
