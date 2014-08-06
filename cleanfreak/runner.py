'''
Runs all tests in the app
=========================
'''
from .utils import get_cleaner


class Runner(object):
    '''Cleaner running facade.'''

    def __init__(self, app):
        self.app = app

    def collect(self):
        cleaners = {}

        mods_dict = self.app.mode
        for name, mod_path in mods_dict.iteritems():
            cleaners[name] = get_cleaner(name, mod_path)()

        return cleaners

    def check_all(self):
        for name, c in self.cleaners.iteritems():
            c._check()

    def clean_all(self):
        for name, c in self.cleaners.iteritems():
            c._clean()
