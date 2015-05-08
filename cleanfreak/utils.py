import sys
import os
from types import ModuleType


def load_module(mod_path):
    '''Find and compile module from its module path'''

    module_file_path = None
    source_file = mod_path + '.py'
    for path in sys.path:

        if os.path.exists(path) and not path[-3:] in ['egg', 'zip']:
            if source_file in os.listdir(path):
                module_file_path = os.path.join(path, source_file)

    if not module_file_path:
        raise ImportError('{0} not found'.format(mod_path))

    with open(module_file_path, 'r') as f:
        c = compile(f.read(), '', 'exec')

    m = ModuleType(mod_path)
    m.__file__ = module_file_path
    exec(c, m.__dict__)
    sys.modules[mod_path] = m

    return m


def get_checker(name, mod_path, mod_cache):
    '''Return module from dotted path'''

    from cleanfreak.checker import Checker

    if mod_path in mod_cache:
        m = mod_cache[mod_path]
    else:
        mod_cache[mod_path] = load_module(mod_path)
        m = sys.modules.get(mod_path)

    try:
        checker = getattr(m, name)
    except AttributeError:
        raise AttributeError(
            'Checker {0} not found in {1}!'.format(name, mod_path))

    if issubclass(checker, Checker):
        return checker

    errstr = 'Checkers must be a subclass of checker: {0}'
    raise TypeError(errstr.format(checker))


def collect(suite):
    '''Collect all cleanfreak checkers from a suite'''

    checkers = []
    mod_cache = {}

    for mod_path in suite:
        mod_path, name = os.path.splitext(mod_path)
        name = name.lstrip('.')
        c = get_checker(name, mod_path, mod_cache)()
        checkers.append(c)

    return checkers
