# -*- coding: utf-8 -*-

import sys
import os
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))
sys.path.insert(0, mod_path)
import cleanfreak


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
version = cleanfreak.__version__
release = cleanfreak.__version__
exclude_patterns = ['build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['static']
htmlhelp_basename = 'cleanfreakdoc'
intersphinx_mapping = {'http://docs.python.org/': None}
