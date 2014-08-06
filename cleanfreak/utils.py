import sys


def import_module(name):
    '''Like importlib.import_module, but without support for relative imports
    from packages.'''
    __import__(name)
    return sys.modules[name]
