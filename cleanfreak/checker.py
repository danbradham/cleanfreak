from abc import ABCMeta, abstractmethod
import traceback


ABC = ABCMeta(str("ABC"), (), {}) # 2n3 compatible metaclassing


class Checker(ABC):
    '''Abstract Base Class for all Checkers. You must override the following
    attributes and methods:

    :attr full_name: The full name of the Checker
    :attr description: A description of the issue the Checker checks
    :meth setup: Runs prior to any checking should include any necessary
    including imports, and attribute defaults
    :meth check: Checks for the described issue
    :meth fix: Recipe to fix the described issue if check does not pass'''


    full_name = None
    description = None
    fail_msg = 'Failed!'
    pass_msg = 'Passed!'
    fix_msg = 'Fixed!'

    def __init__(self):
        self.passed = None
        self.fixed = False
        self.msg = None

    def _reset(self):
        self.passed = None
        self.fixed = False
        self.msg = None

    def _check(self):
        '''This is a private method, do not override. Only :class:`CleanFreak`
        calls this method.

        Calls :meth:`setup` and then checks for issues using :meth:`check` .
        :meth:`check` s return value is bound to self.passed and self.msg'''

        try:
            self.setup()
            self.passed, msg = self.check()
            if not self.fixed:
                self.msg = msg
        except:
            self.msg = traceback.format_exc()
            self.passed = False
        return self.passed, self.msg

    def _fix(self):
        '''This is a private method, do not override. Only :class:`CleanFreak`
        calls this method.

        Attempts to fix any issues that Checker.check found if it
        did not pass. Runs Checker.check again to verify that the issues were
        actually resolved.'''

        if self.passed in [None, True]:
            return

        try:
            self.fixed, self.msg = self.fix()
        except:
            self.msg = traceback.format_exc()
            self.fixed = False
        return self.fixed, self.msg

    @abstractmethod
    def setup(self):
        '''Called prior to running Checker's check method. Includes any
        relevant imports and default values for attributes.

        ::

            import maya.cmds as cmds
            self.no_uvs = []
        '''

    @abstractmethod
    def check(self):
        '''Do your scene check here including any relevant imports
        Return (True, message) if check passes
        Return (False, message) if check fails

        ::

            nodes = cmds.ls(type='mesh')
            for node in nodes:
                if not has_uvs(node):
                    self.no_uvs.append(node)

            if self.no_uvs:
                return False, self.fail_msg.format(self.no_uvs)

            return True, self.passed_msg
        '''

    @abstractmethod
    def fix(self):
        '''Attempt to fix the issue check found.

        ::
            if self.passed:
                return

            for node in self.no_uvs:
                automatic_map(node)

            return True, self.msg
        '''
