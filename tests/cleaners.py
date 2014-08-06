from cleanfreak.cleaner import Cleaner


class A(Cleaner):

    description = "My awesome cleaner A!"

    def setup(self):
        print "A Setup"

    def check(self):
        return True, "A Check: SUCCESS!"

    def clean(self):
        return True, "A Clean: CLEANED!"


class B(Cleaner):

    description = "My awesome cleaner B!"

    def setup(self):
        print "B Setup"

    def check(self):
        return True, "B Check: SUCCESS!"

    def clean(self):
        return True, "B Clean: CLEANED!"


class C(Cleaner):

    description = "My awesome cleaner C!"

    def setup(self):
        print "C Setup"

    def check(self):
        return False, "C Check: FAIL!"

    def clean(self):
        return True, "C Clean: CLEANED!"


class D(Cleaner):

    description = "My awesome cleaner D!"

    def setup(self):
        print "D Setup"

    def check(self):
        return True, "D Check: SUCCESS!"

    def clean(self):
        return False, "D Clean: CLEANED!"


class E(Cleaner):

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

    description = "My awesome cleaner F!"

    def setup(self):
        print "F Setup"

    def check(self):
        return False, "F Check: FAIL!"

    def clean(self):
        return False, "F Clean: CLEAN FAIL!"
