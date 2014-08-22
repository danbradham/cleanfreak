import sys
import os


def import_module(name):
    '''Like importlib.import_module, but without support for relative imports
    from packages.'''
    __import__(name)
    return sys.modules[name]


def get_checker(name, mod_path):
    '''Return module from dotted path'''
    from cleanfreak.checker import Checker

    m = sys.modules.get(mod_path, import_module(mod_path))

    try:
        c = getattr(m, name)
    except AttributeError:
        raise AttributeError(
            "Checker {0} not found in {1}!".format(name, mod_path))

    if issubclass(c, Checker):
        return c

    raise TypeError("Checkers must be a subclass of checker: {0}".format(c))


def collect(suite):
    checkers = []

    for mod_path in suite:
        mod_path, name = os.path.splitext(mod_path)
        name = name.lstrip(".")
        c = get_checker(name, mod_path)()
        checkers.append(c)

    return checkers
