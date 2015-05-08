import sys
import os
import signal

sys.path.insert(1, os.path.dirname(__file__))
signal.signal(signal.SIGINT, signal.SIG_DFL)
os.environ['CLEANFREAK_CFG'] = 'tests'


from cleanfreak import CleanFreak

cf = CleanFreak('TEST')
cf.show()
