__title__ = 'cleanfreak'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com'
__url__ = 'http://github.com/danbradham/cleanfreak'
__version__ = '0.1.8'
__license__ = 'MIT'
__description__ = 'Sanity checks and grades for CG production.'


import os
from functools import partial

# Package relative path joining
package_path = partial(os.path.join, os.path.dirname(__file__))
os.environ.setdefault('CLEANFREAK_CFG', os.path.expanduser('~/cleanfreak'))


from .app import CleanFreak
from .checker import Checker
