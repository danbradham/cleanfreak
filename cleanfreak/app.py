from __future__ import division
from functools import partial
import os
import random
from .config import Config, load_yaml
from .utils import collect
from .messages import (StartChecker, FinishChecker, OnCheck, OnFix,
                       CheckFirst, SuiteSet, Started)
from .shout import shout


REL = partial(os.path.join, os.path.dirname(__file__))


class Grade(object):
    '''Grade data container.

    :attr title: Grade title
    :attr message: Grade message
    :attr color: Grade color (rgb tuple)
    :attr value: Grade value (float 0-1)
    :attr percent: Grade percent (float 0-100)'''

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
        '''Calculates a Grade based on the number of successes and total
        checkers. Uses CleanFreaks config to get a title, message and color.

        :param app: A CleanFreak instance'''

        num_grades = len(app.config['GRADES']['ORD'])
        value = app.successes / app.checker_count
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
    ''':class:`CleanFreak` collects and runs :class:`Checker` :meth:`check`
    and :meth:`fix` methods based on the configuration file passed in
    instantiation.'''

    def __init__(self, cfg_file=None):

        defaults = load_yaml(REL('conf', 'defaults.yml'))
        self.config = Config(defaults)
        if cfg_file:
            rel_path = REL('conf', cfg_file)
            cfg_file = rel_path if os.path.exists(rel_path) else cfg_file
            self.config.from_file(cfg_file)

        self.checkers = None
        self.suite = None
        self.checker_count = 0
        self.ui = None
        self._grade = None
        self.checked = False

        if "DEFAULT" in self.config.get('SUITES', []):
            suite = self.config['SUITES'].pop('DEFAULT')
            self.set_suite(suite)

        shout(Started, self)

    def run_checks(self):
        '''Executes :meth:`check` for each :class:`Checker` in the current
        suite. Emits three :class:`Message` s.

         - :class:`StartChecker` is emitted prior to running checks.
         - :class:`OnCheck` is emitted after each check with the checker and a
         - grade objects.
         - :class:`FinishChecker` is emitted after all checks are completed
        with the final grade object.'''

        self._grade = None
        shout(StartChecker, 'Running Checks...')

        for c in self.checkers:
            c._check()
            grade = Grade.create(self)
            shout(OnCheck, c, grade)

        self._grade = Grade.create(self)
        self.checked = True
        shout(FinishChecker, self._grade)

    def run_fixes(self):
        '''Executes :meth:`fix` for each :class:`Checker` in the current
        suite. Emits three :class:`Message` s.

         - :class:`StartChecker` is emitted prior to running checks.
         - :class:`OnFix` is emitted after each check with the checker and a
         - grade objects.
         - :class:`FinishChecker` is emitted after all checks are completed
        with the final grade object.'''

        if not self.checked:
            shout(CheckFirst, "You've got to run checks first!")
            return

        shout(StartChecker, 'Running Fixes...')

        for c in self.checkers:
            c._fix()
            grade = Grade.create(self)
            shout(OnFix, c, grade)

        self._grade = Grade.create(self)
        shout(FinishChecker, self._grade)
        self.run_checks()

    def set_suite(self, suite):
        '''Sets the suite to the specified value. Collects all checkers listed
        in the suites configuration. Raises a KeyError if the squite is not in
        your configuration.

        :param suite: The key of your suite in config['SUITES']'''

        if not suite in self.config['SUITES']:
            raise KeyError('Unconfigured suite: {0}'.format(suite))

        self.suite_name = suite
        self.suite = self.config['SUITES'][suite]
        self.checkers = collect(self.suite)
        self.checker_count = len(self.checkers)
        self.checked = False
        shout(SuiteSet)

    def list_suites(self):
        '''Returns a list suite names.'''

        return self.config['SUITES'].keys()

    @property
    def successes(self):
        '''Returns the number of successful checks.'''

        if not self._grade:
            self._successes = len([c for c in self.checkers if c.passed])
        return self._successes

    @property
    def grade(self):
        '''Returns a :class:`Grade` with data based on the number of successful
        checks.'''

        if self._grade is None:
            self._grade = Grade.create(self)
        return self._grade

    def show(self):
        '''Shows a PySide UI to control the app. Parenting of the UI is handled
        by different subclasses of :class:`UI`. You can set the context using
        the "CONTEXT" key of your configuration.'''

        if not self.ui:
            from . import ui
            UI = ui.get(self.config['CONTEXT'])
            self.ui = UI.create(self)
        self.ui.show()
