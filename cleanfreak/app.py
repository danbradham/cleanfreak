from __future__ import division
from .config import Config
from .runner import Runner
from .utils import collect
import random


class Grade(object):

    def __init__(self, title, message, color, value):
        self.title = title
        self.message = message
        self.color = color
        self.value = value
        self._percent = None

    @property
    def percent(self):
        if self._percent is None:
            self._percent = self.value * 100
        return self._percent

    @classmethod
    def create(cls, app):
        num_grades = len(app.config['GRADES']['ORD'])
        value = app.successes / app.cleaner_count
        grade_index = int(value * (num_grades - 1))
        grade_key = app.config['GRADES']['ORD'][grade_index]
        grade_info = app.config['GRADES'][grade_key]
        grade = Grade(
            title=grade_key,
            message=random.choice(grade_info['MESSAGES']),
            color=grade_info['COLOR'],
            value=value)
        return grade


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
        self.ui = None
        self._grade = None

        if "DEFAULT" in self.config.get("SUITES", []):
            self.set_suite("DEFAULT")

    def check_all(self):
        '''Generator that runs all checks, yields a cleaner and grade'''
        for c in self.cleaners:
            c._check()
            grade = Grade.create(self)
            yield c, grade
        self._grade = grade

    def clean_all(self):
        '''Generator that runs all cleans, yields a cleaner and grade'''
        for c in self.cleaners:
            c._clean()
            grade = Grade.create(self)
            yield c, grade
        self._grade = grade

    def set_suite(self, suite):
        self.suite = self.config["SUITES"][suite]
        self.cleaners = collect(self.suite)
        self.cleaner_count = len(self.cleaners)

    def list_suites(self):
        return self.config["SUITES"].keys()

    @property
    def successes(self):
        if not self._grade:
            self._successes = len([c for c in self.cleaners if c.passed])
        return self._successes

    @property
    def grade(self):
        if self._grade is None:
            self._grade = Grade.create(self)
        return self._grade

    def show(self):
        '''Pulls in a ui context and creates the ui.'''
        if not self.ui:
            from . import ui
            UI = ui.get(self.config["UI_CONTEXT"])
            self.ui = UI.create(self)
        self.ui.show()
