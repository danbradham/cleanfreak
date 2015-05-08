from .shout import Message


class ConfigChanged(Message):
    '''Shouted when a Config file is changed.'''


class ContextChanged(Message):
    '''Shouted when an apps context changes'''


class StartChecker(Message):
    '''Shouted prior to running checks or cleans.'''


class FinishChecker(Message):
    '''Shouted after running checks or cleans.'''


class OnCheck(Message):
    '''Shouted for each Checker.check(). Passes Checker and a Grade object.'''


class OnFix(Message):
    '''Shouted for each Checker.check(). Passes Checker and a Grade object.'''


class CheckFirst(Message):
    '''Shouted when trying to clean before running checks.'''


class SuiteSet(Message):
    '''Shouted when suite changed.'''


class Started(Message):
    '''Emitted on instancing CleanFreak'''
