from __future__ import division
from .config import Config
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
        self.suite = None
        self.cleaner_count = 0
        if "DEFAULT" in self.config.get("SUITES", []):
            self.set_suite("DEFAULT")

    def collect(self):
        return self.runner.collect(self.suite)

    def check(self):
        self.runner.check(self.cleaners)

    def clean(self):
        self.runner.clean(self.cleaners)

    def set_suite(self, suite):
        self.suite = self.config["SUITES"][suite]
        self.cleaners = self.collect()
        self.cleaner_count = len(self.cleaners)

    def list_suites(self):
        return self.config["SUITES"].keys()

    @property
    def success_count(self):
        successes = [c for c in self.cleaners if c.passed]
        return len(successes)

    def format_grade(self):
        fmt = "{0} of {1} tests passed: {2}%"
        return fmt.format(self.success_count, self.cleaner_count, self.grade)

    @property
    def grade(self):
        return (self.success_count / self.cleaner_count) * 100

    def show(self):
        '''Pulls in a ui context and creates the ui.'''
        from . import ui
        UI = ui.get(self.config["UI_CONTEXT"])
        self.ui = UI.create(self)
