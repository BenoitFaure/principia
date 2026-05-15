import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "Principia"
copyright = "2025, Benoit"
author = "Benoit"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

autodoc_member_order = "bysource"
autodoc_typehints = "description"
always_document_param_types = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

html_theme = "furo"
html_title = "Principia"
html_theme_options = {
    "sidebar_hide_name": False,
}

exclude_patterns = ["_build"]
templates_path = ["_templates"]
