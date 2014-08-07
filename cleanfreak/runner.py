'''
Runs all tests in the app
=========================
'''
from .utils import get_cleaner
import os

class Runner(object):
    '''Cleaner running facade.'''

    def collect(self, suite):
        cleaners = []

        for mod_path in suite:
            mod_path, name = os.path.splitext(mod_path)
            name = name.lstrip(".")
            c = get_cleaner(name, mod_path)()
            cleaners.append(c)

        return cleaners

    def check(self, cleaners):
        for c in cleaners:
            c._check()

    def clean(self, cleaners):
        for c in cleaners:
            c._clean()
