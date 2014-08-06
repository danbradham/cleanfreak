import sys


def import_module(name):
    '''Like importlib.import_module, but without support for relative imports
    from packages.'''
    __import__(name)
    return sys.modules[name]


def get_cleaner(name, mod_path):
    '''Return module from dotted path'''
    from .cleaner import Cleaner
    import_module(mod_path)
    all_cleaners = Cleaner.__subclasses__()

    for cleaner in all_cleaners:
        if cleaner.__name__ == name:
            return cleaner

    raise ImportError("Cleaner {0} not found in {1}!".format(name, mod_path))
