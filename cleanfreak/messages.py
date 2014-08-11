from .shout import Message


class StartCleaner(Message):
    '''Shouted prior to running checks or cleans.'''


class FinishCleaner(Message):
    '''Shouted after running checks or cleans.'''


class OnCheck(Message):
    '''Shouted for each Cleaner.check(). Passes cleaner and a Grade object.'''


class OnClean(Message):
    '''Shouted for each Cleaner.check(). Passes cleaner and a Grade object.'''


class CheckFirst(Message):
    '''Shouted when trying to clean before running checks.'''


class SuiteSet(Message):
    '''Shouted when suite changed.'''

