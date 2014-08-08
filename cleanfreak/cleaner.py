from abc import ABCMeta, abstractmethod


ABC = ABCMeta(str("ABC"), (), {}) # 2n3 compatible metaclassing


class Cleaner(ABC):

    full_name = None
    description = None

    def __init__(self):
        self.passed = None
        self.cleaned = False
        self.msg = None

    def _check(self):
        self.setup()
        self.passed, self.msg = self.check()
        return self.passed, self.msg

    def _clean(self):
        if not self.passed:
            self.cleaned, self.msg = self.clean()
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
        '''Attempt to fix any issue found.

        ::
            if self.passed:
                return

            for node in self.no_uvs:
                automatic_map(node)

            return True, self.msg
        '''
