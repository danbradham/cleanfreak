import os
import random
from functools import partial
from .config import Config
from .cleaner import Cleaner
from .runner import Runner


class CleanFreak(object):

    def __init__(self, cfg_file=None):
        self.config = Config()
        if cfg_file:
            if cfg_file.split(".")[-1] in ["yaml", "yml"]:
                self.config.from_yaml(cfg_file)
            elif cfg_file.split(".")[-1] in ["son", "json", "jsn"]:
                self.config.from_json(cfg_file)
            else:
                raise OSError("Config files can be json or yaml.")
        self.runner = Runner()
        self.cleaners = None
        self._context = None
        self._step = None
        self._ctx = None
        self._grades = []
        self._cleaner_count = None
        self._success_count = None
        self.run_count = 0

    def collect(self):
        return self.runner.collect(self.context)

    def check(self):
        self.runner.check(self.cleaners)
        self.run_count += 1

    def clean(self):
        self.runner.clean(self.cleaners)
        self.run_count += 1

    def set_context(self, application, step):
        self._context = application
        self._step = step
        self._grades = []
        self.run_count = 0
        self._cleaner_count = None
        self._success_count = None
        self.context
        self.cleaners = self.collect()

    @property
    def context(self):
        if self._ctx is None:
            self._ctx = self.config[self._context][self._step]
        return self._ctx

    @property
    def success_count(self):
        if self.run_count != len(self._grades):
            successes = [c for c in self.cleaners.itervalues() if c.passed]
            self._success_count = len(successes)
        return self._success_count

    @property
    def cleaner_count(self):
        if self._cleaner_count is None:
            self._cleaner_count = len(self.cleaners)
        return self._cleaner_count

    def format_grade(self):
        fmt = "{0} of {1} tests passed: {2}%"
        return fmt.format(self.success_count, self.cleaner_count, self.grade)

    @property
    def grade(self):
        if self.run_count != len(self._grades):
            grade = (self.success_count / float(self.cleaner_count)) * 100
            self._grades.append(grade)
            return grade
        if self._grades:
            return self._grades[-1]
        return 0

    @property
    def modes(self):
        return self.config.keys()

    def create_ui(self):
        '''Pulls in a ui context and creates the ui.'''
        from . import ui
        UI = ui.get(self._context)
        self.ui = UI.create(self)
