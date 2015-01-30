from __future__ import division
from functools import partial
import os
import random
import shutil
from .config import Config, load_yaml
from .utils import collect
from .messages import (StartChecker, FinishChecker, OnCheck, OnFix,
                       CheckFirst, SuiteSet, Started)
from .shout import shout


rel_path = partial(os.path.join, os.path.dirname(__file__))


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
    and :meth:`fix` methods based on the config file in your configuration
    root directory. Configuration root is looked up in the following order.

     * Parameter cfg_root passed to CleanFreak on instantiation
     * Environment variable CLEANFREAK_CFG
     * ~/cleanfreak

    If the directory does not exist the default config in cleanfreak/conf is
    copied to the directory. Providing you with a default configuration to
    extend. The configuration root directory is then added to your pythonpath
    allowing you to load python modules from there. This is the best place to
    keep a module containing :class:`Checker` objects.

    :param cfg_root: Optional configuration root directory.'''

    def __init__(self, context=None, cfg_root=None):

        self.config = Config()

        if cfg_root:
            os.environ['CLEANFREAK_CFG'] = cfg_root
        else:
            cfg_root = os.environ.setdefault(
            'CLEANFREAK_CFG', os.path.expanduser('~/cleanfreak'))

        if not os.path.exists(cfg_root):
            shutil.copytree(rel_path('conf'), cfg_root)

        self.config.from_env('CLEANFREAK_CFG')

        self.checkers = None
        self.suite = None
        self.ui = None
        self._grade = None
        self.checked = False

        self.ctx = self.config['CONTEXTS'][context]
        if "DEFAULT" in self.ctx.get('SUITES', []):
            suite = self.ctx['SUITES'].pop('DEFAULT')
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
            if c.enabled:
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
            if c.enabled:
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

        if not suite in self.ctx['SUITES']:
            raise KeyError('Unconfigured suite: {0}'.format(suite))

        self.suite_name = suite
        self.suite = self.ctx['SUITES'][suite]
        self.checkers = collect(self.suite)
        self.checked = False
        shout(SuiteSet)

    def list_suites(self):
        '''Returns a list suite names.'''

        return self.ctx['SUITES'].keys()

    @property
    def checker_count(self):
        i = 0
        for c in self.checkers:
            if c.enabled:
                i += 1
        return i


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
            UI = ui.get(self.ctx['UI'])
            self.ui = UI.create(self)
        self.ui.show()
