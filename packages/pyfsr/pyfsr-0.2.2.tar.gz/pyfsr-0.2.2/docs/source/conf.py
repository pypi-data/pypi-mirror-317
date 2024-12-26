import os
import sys

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
project = 'pyfsr'
copyright = '2024, Dylan Spille'
author = 'Dylan Spille'
release = '0.2.2'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'autoapi.extension',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://docs.python-requests.org/en/latest/', None),
}

# AutoAPI configuration
autoapi_type = 'python'
autoapi_dirs = ['../../src/pyfsr']  # Relative path to the Python package
autoapi_keep_files = True  # Keep intermediate files for debugging
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

# HTML Theme
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navbar_end": ["theme-switcher"],  # Adds the toggle to the navigation bar
}
templates_path = ['_templates']
html_static_path = ['_static']

# Custom static files
html_css_files = [
    'custom.css',  # Example custom CSS
]

# Exclude patterns
exclude_patterns = ['build']
