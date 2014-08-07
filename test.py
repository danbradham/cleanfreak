from cleanfreak import CleanFreak

app = CleanFreak("tests/config.yml")

print "Checking all"
app.check()
print app.format_grade()

print "Cleaning all"
app.clean()

print "Rechecking all"
app.check()
print app.format_grade()

print app.cleaners

print app.list_suites()

app.set_suite(app.list_suites()[1])

print app.cleaners

#app.show()
