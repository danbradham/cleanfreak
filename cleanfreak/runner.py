'''
Runs all tests in the app
=========================
'''
from .utils import get_cleaner


class Runner(object):
    '''Cleaner running facade.'''

    def collect(self, mode):
        cleaners = {}

        for name, mod_path in mode.iteritems():
            cleaners[name] = get_cleaner(name, mod_path)()

        return cleaners

    def check(self, cleaners):
        for name, c in cleaners.iteritems():
            c._check()

    def clean(self, cleaners):
        for name, c in cleaners.iteritems():
            c._clean()
