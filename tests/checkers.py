from cleanfreak.checker import Checker


class TestChecker(Checker):

    def select(self):
        print 'selection'


class A(TestChecker):

    full_name = "Checker A"
    description = "My awesome Checker A!"


    def check(self):
        return True, "A Check: SUCCESS!"

    def fix(self):
        return True, "A Fix: FIXED!"


class B(TestChecker):

    full_name = "Checker B"
    description = "My awesome Checker B!"


    def check(self):
        return True, "B Check: SUCCESS!"

    def fix(self):
        return True, "B Fix: FIXED!"


class C(TestChecker):

    full_name = "Checker C"
    description = "My awesome Checker C!"

    def check(self):
        raise Exception("Crazy super exception")
        return False, "Super ultra mega long failing message what does it do."

    def fix(self):
        return True, "C Fix: FIXED!"


class D(TestChecker):

    full_name = "Checker D"
    description = "My awesome Checker D!"


    def check(self):
        return True, "D Check: SUCCESS!"

    def fix(self):
        return False, "D Fix: FIXED!"


class E(TestChecker):

    full_name = "Checker E"
    description = "My awesome Checker E!"


    def check(self):
        if self.fixed:
            return True, "E Check: SUCCESS!"
        return False, "E Check: FAIL!"

    def fix(self):
        return True, "E Fix: FIXED!"


class F(TestChecker):

    full_name = "Checker F"
    description = "My awesome Checker F!"


    def check(self):
        return False, "F Check: FAIL!"

    def fix(self):
        return False, "F Fix: FIX FAIL!"


class G(TestChecker):

    full_name = "Checker G"
    description = "My awesome Checker G!"

    def check(self):
        return False, "G Check: FAIL!"

    def fix(self):
        return True, "G Fix: FIXED!"


class H(TestChecker):

    full_name = "Checker H"
    description = "My awesome Checker H!"


    def check(self):
        return True, "H Check: SUCCESS!"

    def fix(self):
        return False, "H Fix: FIXED!"


class I(TestChecker):

    full_name = "Checker I"
    description = "My awesome Checker I!"


    def check(self):
        if self.fixed:
            return True, "I Check: SUCCESS!"
        return False, "I Check: FAIL!"

    def fix(self):
        return True, "I Fix: FIXED!"


class J(TestChecker):

    full_name = "Checker J"
    description = "My awesome Checker J!"


    def check(self):
        return True, "J Check: SUCCESS!"

    def fix(self):
        return False, "J Fix: FIX FAIL!"

