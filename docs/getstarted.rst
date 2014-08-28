.. _getstarted:

===============
Getting Started
===============
This section will guide you through the most basic usage of CleanFreak.

--------------
Showing the UI
--------------

::

    from cleanfreak import CleanFreak

    app = CleanFreak("maya.yml")
    app.show()


---------------------------
Using CleanFreak without UI
---------------------------

::

    from cleanfreak import CleanFreak

    app = CleanFreak("maya.yml")
    app.set_suite("Model")

    app.run_checks()
    print app.grade.format()

    # Results:
    #
    # Grade Title
    # 50%
    # Grade Message
    #
    # Test Name Failed with an exception:
    # *STACK TRACE*
    #
    # Test Name Failed:
    # *FAIL MESSAGE*

    app.run_fixes()
    print app.grade.format()

    # Results:
    #
    # Grade Title
    # 100%
    # Grade Message
