import sys
from abc import ABCMeta, abstractmethod
from .utils import import_module


ABC = ABCMeta(str("ABC"), (), {}) # 2n3 compatible metaclassing


class Cleaner(ABC):

    name = None
    description = None

    def _check(self):
        self.setup()
        try:
            self.passed, self.msg = self.check()
            return self.passed, self.msg
        except:
            return False, sys.exc_info()[2]

    def _clean(self):
        try:
            self.clean()
            return True, "Cleaned it up!"
        except:
            return False, sys.exc_info()[2]

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
        '''


def get_cleaners(mod_path):
    '''Return module from dotted path'''
    m = import_module(mod_path)
    all_cleaners = Cleaner.__subclasses__()

    cleaners = {}

    for name in dir(m):
        obj = getattr(m, name)
        if obj in all_cleaners:
            cleaners[name] = obj

    return cleaners
