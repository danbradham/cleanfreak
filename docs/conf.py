# -*- coding: utf-8 -*-

import sys
import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'cleanfreak'
copyright = u'2014, Dan Bradham'
version = '0.1.0'
release = '0.1.0'
exclude_patterns = ['build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['static']
htmlhelp_basename = 'cleanfreakdoc'
intersphinx_mapping = {'http://docs.python.org/': None}
