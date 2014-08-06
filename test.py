from cleanfreak import CleanFreak

app = CleanFreak("tests/config.yml")
app.set_context("app_b", "stage_a")

print "Checking all"
app.check()
print app.format_grade()

print "Cleaning all"
app.clean()

print "Rechecking all"
app.check()
print app.format_grade()

app.create_ui()
