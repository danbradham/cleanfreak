import os
import random
from functools import partial
from .config import Config
from .cleaner import Cleaner
from .runner import Runner


class CleanFreak(object):

    defaults = {
        "maya": {
            "model": {
                "A": "tests.cleaners",
                "B": "tests.cleaners",
                "C": "tests.cleaners",
                "D": "tests.cleaners",
                "E": "tests.cleaners",
            },
            "shade": {
                "A": "tests.cleaners",
                "C": "tests.cleaners",
                "D": "tests.cleaners",
            },
            "rig": {
                "A": "tests.cleaners",
                "C": "tests.cleaners",
                "D": "tests.cleaners",
                "E": "tests.cleaners",
            },
            "animate": {
                "A": "tests.cleaners",
                "B": "tests.cleaners",
                "D": "tests.cleaners",
                "E": "tests.cleaners",
            },
            "light": {
                "B": "tests.cleaners",
                "C": "tests.cleaners",
                "D": "tests.cleaners",
            }
        }
    }

    def __init__(self, context, mode=None):
        self.config = Config(defaults=self.defaults)
        self.set_context(context)
        self.set_mode(mode or random.choice(self.context.keys()))
        self.runner = Runner(self)
        self.cleaners = self.collect()

    def collect(self):
        return self.runner.collect()

    def check_all(self):
        self.runner.check_all()

    def clean_all(self):
        self.runner.clean_all()

    def set_context(self, key):
        self.context = self.config[key]

    def set_mode(self, key):
        self.mode = self.context[key]

    @property
    def modes(self):
        return self.config.keys()

    def show(self):
        '''Pulls in a ui context and creates the ui.'''
        from . import ui
        UI = ui.get(self.context)
        self.ui = UI.create(self)
