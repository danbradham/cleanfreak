from cleanfreak.checker import Checker

class A(Checker):

    full_name = "Checker A"
    description = "My awesome Checker A!"

    def setup(self):
        print "A Setup"

    def check(self):
        return True, "A Check: SUCCESS!"

    def fix(self):
        print "A fix"
        return True, "A Fix: FIXED!"


class B(Checker):

    full_name = "Checker B"
    description = "My awesome Checker B!"

    def setup(self):
        print "B Setup"

    def check(self):
        return True, "B Check: SUCCESS!"

    def fix(self):
        return True, "B Fix: FIXED!"


class C(Checker):

    full_name = "Checker C"
    description = "My awesome Checker C!"

    def setup(self):

        print "C Setup"

    def check(self):
        raise Exception("Crazy super exception")
        return False, "Super ultra mega long failing message what does it do."

    def fix(self):
        return True, "C Fix: FIXED!"


class D(Checker):

    full_name = "Checker D"
    description = "My awesome Checker D!"

    def setup(self):
        print "D Setup"

    def check(self):
        return True, "D Check: SUCCESS!"

    def fix(self):
        return False, "D Fix: FIXED!"


class E(Checker):

    full_name = "Checker E"
    description = "My awesome Checker E!"

    def setup(self):
        print "E Setup"

    def check(self):
        if self.fixed:
            return True, "E Check: SUCCESS!"
        return False, "E Check: FAIL!"

    def fix(self):
        return True, "E Fix: FIXED!"


class F(Checker):

    full_name = "Checker F"
    description = "My awesome Checker F!"

    def setup(self):
        print "F Setup"

    def check(self):
        return False, "F Check: FAIL!"

    def fix(self):
        return False, "F Fix: FIX FAIL!"


class G(Checker):

    full_name = "Checker G"
    description = "My awesome Checker G!"

    def setup(self):

        print "G Setup"

    def check(self):
        return False, "G Check: FAIL!"

    def fix(self):
        return True, "G Fix: FIXED!"


class H(Checker):

    full_name = "Checker H"
    description = "My awesome Checker H!"

    def setup(self):
        print "H Setup"

    def check(self):
        return True, "H Check: SUCCESS!"

    def fix(self):
        return False, "H Fix: FIXED!"


class I(Checker):

    full_name = "Checker I"
    description = "My awesome Checker I!"

    def setup(self):
        print "I Setup"

    def check(self):
        if self.fixed:
            return True, "I Check: SUCCESS!"
        return False, "I Check: FAIL!"

    def fix(self):
        return True, "I Fix: FIXED!"


class J(Checker):

    full_name = "Checker J"
    description = "My awesome Checker J!"

    def setup(self):
        print "J Setup"

    def check(self):
        return True, "J Check: SUCCESS!"

    def fix(self):
        return False, "J Fix: FIX FAIL!"

