'''
PySide UI
=========
'''
from __future__ import division
from PySide import QtGui, QtCore
import sys
import os
from functools import partial
from ..messages import (
    StartChecker, FinishChecker, OnCheck, OnFix, CheckFirst, SuiteSet)
from ..shout import has_ears, hears


# py_ver = sys.version
REL = partial(os.path.join, os.path.dirname(__file__))

BAR = '''
QProgressBar {{
    border-radius: 5px;
    text-align: center;
    font-size: 24;
    background-color: rgb(45, 45, 45);
    color: rgb(255, 255, 255);
    padding: 2px;
}}
QProgressBar::chunk {{
    background-color: rgb({0}, {1}, {2});
    width:1px;
}}
'''
UNCHECKED = '''
QWidget#CheckerListItem{background-color: rgb(50, 50, 50);}
QWidget#CheckerListItem:hover{background-color: rgb(60, 60, 60);}
'''
PASSED = '''
QLabel#CheckerLabel{color: rgb(51, 190, 51);}
QLabel#CheckerLabel:hover{color: rgb(56, 200, 56);}
'''
FAILED = '''
QLabel#CheckerLabel{color: rgb(198, 53, 34);}
QLabel#CheckerLabel:hover{color: rgb(208, 58, 39);}
'''

class TopAlignedList(QtGui.QVBoxLayout):

    def __init__(self, *args, **kwargs):
        super(TopAlignedList, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setSpacing(0)
        self.setContentsMargins(0, 10, 0, 0)

    def addWidget(self, widget):
        super(TopAlignedList, self).addWidget(widget)
        self.setAlignment(widget, QtCore.Qt.AlignTop)


class CheckerList(QtGui.QScrollArea):

    def __init__(self, parent=None):
        super(CheckerList, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setEnabled(True)

        self.scrollWidget = QtGui.QWidget()
        self.setWidget(self.scrollWidget)

        self.layout = TopAlignedList()
        self.scrollWidget.setLayout(self.layout)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vScrollBar = self.verticalScrollBar()
        self.button = None

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def mousePressEvent(self, event):
        if event.button() in (1, 4):
            self.lastPoint = event.pos()
            self.button = 4

    def mouseReleaseEvent(self, event):
        self.button = None

    def mouseMoveEvent(self, event):
        if self.button:
            self.vScrollBar = self.verticalScrollBar()
            if not self.vScrollBar:
                return
            currentPoint = event.pos()
            scroll_vector = (currentPoint - self.lastPoint)
            yValue = self.vScrollBar.value()
            self.vScrollBar.setValue(yValue + (-1 * scroll_vector.y()))
            self.lastPoint = currentPoint


class ClickableLabel(QtGui.QLabel):

    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)
        self.hold = 0

    def mousePressEvent(self, event):
        self.hold = 0
        super(ClickableLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.hold > 3:
            super(ClickableLabel, self).mouseMoveEvent(event)
            return
        self.hold += 1

    def mouseReleaseEvent(self, event):
        super(ClickableLabel, self).mouseReleaseEvent(event)
        if self.hold < 3:
            self.clicked.emit()
        if self.hold > 3:
            self.hold = 0
            return


class CheckerListItem(QtGui.QWidget):

    def __init__(self, checker, *args, **kwargs):
        super(CheckerListItem, self).__init__(*args, **kwargs)

        self.checker = checker

        self.setObjectName("CheckerListItem")

        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.label = ClickableLabel()
        self.label.setObjectName("CheckerLabel")
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.clicked.connect(self.toggle_message)
        self.label.setFixedHeight(24)
        self.desc = ClickableLabel()
        self.desc.setObjectName("CheckerDesc")
        self.desc.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self.desc.clicked.connect(self.toggle_message)
        self.desc.setFixedHeight(18)
        self.message = QtGui.QLabel()
        self.message.setObjectName("CheckerMessage")
        self.message.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.message.setWordWrap(True)
        self.message.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.message.hide()

        self.grid.addWidget(self.label, 0, 0)
        self.grid.addWidget(self.desc, 1, 0)
        self.grid.addWidget(self.message, 2, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def toggle_message(self):
        '''Show message if there is one, else hide.'''
        msg_visible = self.message.isVisible()
        if self.checker.msg:
            if msg_visible:
                self.message.hide()
            else:
                self.message.show()

    def refr(self):
        '''Refresh item from checker.'''
        # self.status.set(self.checker.passed)
        if self.checker.passed is not None:
            style = PASSED if self.checker.passed else FAILED
            self.setStyleSheet(style)
        self.label.setText(self.checker.full_name)
        self.desc.setText(self.checker.description)
        self.message.setText(self.checker.msg)

class Toolbar(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)

        self.setObjectName("Toolbar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.layout = QtGui.QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(5, 1)
        self.setLayout(self.layout)
        self.setFixedHeight(50)

    def addWidget(self, *args, **kwargs):
        self.layout.addWidget(*args, **kwargs)

@has_ears
class UI(QtGui.QDockWidget):

    def __init__(self, app, parent=None):
        super(UI, self).__init__(parent)

        self.app = app

        self.setFeatures(
            QtGui.QDockWidget.DockWidgetClosable|
            QtGui.QDockWidget.DockWidgetFloatable|
            QtGui.QDockWidget.DockWidgetMovable)
        self.setFloating(True)
        self.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea|
            QtCore.Qt.RightDockWidgetArea)
        self.setWindowTitle("cleanfreak: Clean your shit up!")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.widget = QtGui.QWidget(self)
        self.widget.setObjectName("Main")
        self.widget.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setWidget(self.widget)

        self.top_grid = QtGui.QGridLayout()
        self.top_grid.setContentsMargins(0, 0, 0, 0)
        self.top_grid.setRowStretch(0, 1)
        self.widget.setLayout(self.top_grid)

        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setRowStretch(3, 1)
        self.grid.setSpacing(10)

        self.toolbar = Toolbar(self.widget)
        self.top_grid.addWidget(self.toolbar, 0, 0)
        self.top_grid.addLayout(self.grid, 1, 0)

        self.suite_label = QtGui.QLabel("Suite:")
        self.suite_label.setObjectName("Basic")
        self.context_opts = QtGui.QComboBox()

        self.check_button = QtGui.QPushButton()
        self.check_button.setText("Run Checks")
        self.check_button.clicked.connect(self.app.run_checks)
        self.check_button.setObjectName("CheckButton")

        self.fix_button = QtGui.QPushButton()
        self.fix_button.setText("Clean it up!")
        self.fix_button.clicked.connect(self.app.run_fixes)
        self.fix_button.setObjectName("FixButton")

        #self.toolbar.addWidget(self.suite_label, 0, 1)
        self.toolbar.addWidget(self.context_opts, 0, 2)
        self.toolbar.addWidget(self.check_button, 0, 3)
        self.toolbar.addWidget(self.fix_button, 0, 4)

        self.checker_list = CheckerList()
        self.checker_list.scrollWidget.setAttribute(
            QtCore.Qt.WA_StyledBackground, True)
        self.checker_list.scrollWidget.setObjectName('Main')

        self.progress_grd = QtGui.QLabel("Run Your Checks!")
        self.progress_grd.setAlignment(QtCore.Qt.AlignHCenter)
        self.progress_grd.setObjectName("Grade")

        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.progress_msg = QtGui.QLabel("Run Your Checks!")
        self.progress_msg.setAlignment(QtCore.Qt.AlignHCenter)
        self.progress_msg.setObjectName("GradeMessage")

        self.grid.addWidget(self.progress_grd, 0, 0)
        self.grid.addWidget(self.progress_bar, 1, 0)
        self.grid.addWidget(self.progress_msg, 2, 0)
        self.grid.addWidget(self.checker_list, 3, 0)


        self.checker_items = {}
        self.context_opts.addItems(self.app.config["SUITES"].keys())
        self.context_opts.currentIndexChanged.connect(self.set_context)
        self.load_context()

        with open(REL("style.css")) as f:
            self.setStyleSheet(f.read())

    @hears(SuiteSet)
    def load_context(self):
        if self.checker_items:
            for ci in self.checker_items.values():
                ci.setParent(None)
                del(ci)
            self.checker_items = {}

        for c in self.app.checkers:
            checker_item = CheckerListItem(c)
            self.checker_list.addWidget(checker_item)
            self.checker_items[c.full_name] = checker_item

        suite_index = self.context_opts.findText(self.app.suite_name)
        self.context_opts.setCurrentIndex(suite_index)

        self.progress_grd.setText("Run Your Checks!")
        self.progress_bar.hide()
        self.progress_msg.hide()

        self.refr()

    def set_context(self):
        self.app.set_suite(self.context_opts.currentText())

    @hears(StartChecker)
    def start_checker(self, message):
        self.progress_bar.show()
        self.progress_msg.show()
        self.progress_grd.setText("Running Checkers...")
        self.progress_bar.setValue(0)
        self.progress_msg.setText("Starting Checks...")

    @hears(FinishChecker)
    def finish_checker(self, grade):
        self.progress_grd.setText(grade.title)
        self.progress_bar.setValue(grade.percent)
        self.progress_msg.setText(grade.message)

    @hears(OnCheck)
    def check(self, c, grade):
        self.progress_msg.setText("{0} checking".format(c.full_name))
        self.checker_items[c.full_name].refr()
        self.progress_bar.setStyleSheet(BAR.format(*grade.color))
        self.progress_bar.setValue(grade.percent)

    @hears(OnFix)
    def fix(self, c, grade):
        self.progress_msg.setText("{0} fixing".format(c.full_name))
        self.checker_items[c.full_name].refr()
        self.progress_bar.setStyleSheet(BAR.format(*grade.color))
        self.progress_bar.setValue(grade.percent)

    @hears(CheckFirst)
    def check_first(self, message):
        self.progress_grd.setText("Check First!")
        self.progress_msg.setText(message)

    def refr(self):
        for ci in self.checker_items.values():
            ci.refr()

    @classmethod
    def create(cls, app):
        '''Overwrite in custom application context passing parent ui.'''
        qtapp = QtGui.QApplication(sys.argv)
        ui = cls(app, parent=None)
        ui.show()
        sys.exit(qtapp.exec_())
