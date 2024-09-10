import os
import sys

sys.path.insert(0, os.path.abspath('../'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
master_doc = 'index'

project = 'GalaxyPulse'
copyright = '2024, Z-Dezign'
author = 'Z-Dezign'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'special-members': True,
    'undoc-members': True,
    'show-inheritance': True
}

autodoc_inherit_docstrings = True

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**/.venv/**'
]

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'furo'
html_static_path = ['../_static']
html_logo = "../_static/logo.png"
html_favicon = '../_static/favicon_io/favicon.ico'

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2980b9",  # Bleu pour les titres et boutons
        "color-brand-content": "#3498db",  # Bleu clair pour le contenu
        "color-sidebar-background": "#f5f5f5",  # Couleur de fond de la barre latérale
    },
    "dark_css_variables": {
        "color-brand-primary": "#1abc9c",  # Vert pour le mode sombre
        "color-brand-content": "#2ecc71",
        "color-sidebar-background": "#333333",
    }
}
