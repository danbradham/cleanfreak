from cleanfreak.cleaner import Cleaner
import time

class A(Cleaner):

    full_name = "Cleaner A"
    description = "My awesome cleaner A!"

    def setup(self):
        print "A Setup"

    def check(self):
        print "A Check"
        time.sleep(1)
        return True, "A Check: SUCCESS!"

    def clean(self):
        print "A Clean"
        return True, "A Clean: CLEANED!"


class B(Cleaner):

    full_name = "Cleaner B"
    description = "My awesome cleaner B!"

    def setup(self):
        print "B Setup"

    def check(self):
        time.sleep(2)
        return True, "B Check: SUCCESS!"

    def clean(self):
        return True, "B Clean: CLEANED!"


class C(Cleaner):

    full_name = "Cleaner C"
    description = "My awesome cleaner C!"

    def setup(self):

        print "C Setup"

    def check(self):
        time.sleep(3)
        return False, "C Check: FAIL!"

    def clean(self):
        return True, "C Clean: CLEANED!"


class D(Cleaner):

    full_name = "Cleaner D"
    description = "My awesome cleaner D!"

    def setup(self):
        print "D Setup"

    def check(self):
        time.sleep(0.2)
        return True, "D Check: SUCCESS!"

    def clean(self):
        return False, "D Clean: CLEANED!"


class E(Cleaner):

    full_name = "Cleaner E"
    description = "My awesome cleaner E!"

    def setup(self):
        print "E Setup"

    def check(self):
        if self.cleaned:
            return True, "E Check: SUCCESS!"
        return False, "E Check: FAIL!"

    def clean(self):
        return True, "E Clean: CLEANED!"


class F(Cleaner):

    full_name = "Cleaner F"
    description = "My awesome cleaner F!"

    def setup(self):
        print "F Setup"

    def check(self):
        time.sleep(1)
        return False, "F Check: FAIL!"

    def clean(self):
        return False, "F Clean: CLEAN FAIL!"
