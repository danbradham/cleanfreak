import sys
import os


def import_module(name):
    '''Like importlib.import_module, but without support for relative imports
    from packages.'''
    __import__(name)
    return sys.modules[name]


def get_cleaner(name, mod_path):
    '''Return module from dotted path'''
    from cleanfreak.cleaner import Cleaner

    m = sys.modules.get(mod_path, import_module(mod_path))

    try:
        c = getattr(m, name)
    except AttributeError:
        raise AttributeError(
            "Cleaner {0} not found in {1}!".format(name, mod_path))

    if issubclass(c, Cleaner):
        return c

    raise TypeError("Cleaners must be a subclass of cleaner: {0}".format(c))


def collect(suite):
    cleaners = []

    for mod_path in suite:
        mod_path, name = os.path.splitext(mod_path)
        name = name.lstrip(".")
        c = get_cleaner(name, mod_path)()
        cleaners.append(c)

    return cleaners
