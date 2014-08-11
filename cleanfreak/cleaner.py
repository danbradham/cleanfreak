from abc import ABCMeta, abstractmethod
import traceback


ABC = ABCMeta(str("ABC"), (), {}) # 2n3 compatible metaclassing


class Cleaner(ABC):
    '''Abstract BaseClass for all Cleaners. All Cleaners inherit from this
    class. You must override the following attributes and methods:

    :attr full_name: The full name of the Cleaner
    :attr description: A description of the issue the Cleaner checks
    :meth setup: Runs prior to any checking should include any necessary
    including imports, and attribute defaults
    :meth check: Checks for the described issue
    :meth clean: Recipe to fix the described issue if check does not pass'''


    full_name = None
    description = None

    def __init__(self):
        self.passed = None
        self.cleaned = False
        self.msg = None

    def _check(self):
        '''This is a private method, do not override. Only CleanFreak calls
        this method.

        Calls :meth:`setup` and then checks for issues using :meth:`check` .
        :meth:`check` s return value is bound to self.passed and self.msg'''

        try:
            self.setup()
            self.passed, self.msg = self.check()
        except:
            self.msg = traceback.format_exc()
            self.passed = False
        return self.passed, self.msg

    def _clean(self):
        '''This is a private method, do not override. Only CleanFreak calls
        this method.

        Attempts to fix any issues that Cleaner.check found if it
        did not pass. Runs cleaner.check again to verify that the issues were
        actually resolved.'''

        if self.passed in [None, True]:
            return

        try:
            self.cleaned, self.msg = self.clean()
        except:
            self.msg = traceback.format_exc()
            self.cleaned = False
        return self.cleaned, self.msg

    @abstractmethod
    def setup(self):
        '''Called prior to running cleaner's check method. Includes any
        relevant imports and default values for attributes.
        ::

            import maya.cmds as cmds
            self.no_uvs = []
            self.fail_msg = "These nodes have no UVs: {0}"
            self.passed_msg = "All meshes in your scene have UVs. Congrats!!"
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
    def clean(self):
        '''Attempt to fix the issue check found.

        ::
            if self.passed:
                return

            for node in self.no_uvs:
                automatic_map(node)

            return True, self.msg
        '''
