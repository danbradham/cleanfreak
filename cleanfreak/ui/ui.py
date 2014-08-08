'''
PySide UI
=========
'''
from __future__ import division
from PySide import QtGui, QtCore
import sys
import os
from functools import partial


REL = partial(os.path.join, os.path.dirname(__file__))


class CleanerList(QtGui.QVBoxLayout):

    def __init__(self, *args, **kwargs):
        super(CleanerList, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignTop)

    def addWidget(self, widget):
        super(CleanerList, self).addWidget(widget)
        self.setAlignment(widget, QtCore.Qt.AlignTop)


class CleanerStatus(QtGui.QWidget):

    colors = {
        True: (0, 255, 0),
        False: (255, 0, 0),
        None: (55, 55, 55)
    }

    def __init__(self, *args, **kwargs):
        super(CleanerStatus, self).__init__(*args, **kwargs)
        self.setFixedSize(36, 36)
        self.status = False

    def set(self, value):
        self.status = value
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtGui.QColor(*self.colors[self.status]))
        painter.setBrush(QtGui.QColor(*self.colors[self.status]))
        painter.drawEllipse(10, 10, 16, 16)
        painter.end()


class CleanerListItem(QtGui.QWidget):

    def __init__(self, cleaner, *args, **kwargs):
        super(CleanerListItem, self).__init__(*args, **kwargs)

        self.cleaner = cleaner

        self.setObjectName("CleanerListItem")
        self.setFixedHeight(36)

        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.status = CleanerStatus()
        self.status.mousePressEvent = self.mousePressEvent
        self.label = QtGui.QLabel()
        self.label.setObjectName("CleanerLabel")
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.mousePressEvent = self.mousePressEvent
        self.desc = QtGui.QLabel()
        self.desc.setObjectName("CleanerDesc")
        self.desc.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)
        self.desc.mousePressEvent = self.mousePressEvent
        self.message = QtGui.QLabel()
        self.message.setObjectName("CleanerMessage")
        self.message.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.message.setFixedHeight(40)
        self.message.hide()
        self.fill = QtGui.QLabel()
        self.fill.setObjectName("fill")
        self.fill.setFixedHeight(40)
        self.fill.hide()

        self.grid.addWidget(self.status, 0, 0, 2, 1)
        self.grid.addWidget(self.label, 0, 1)
        self.grid.addWidget(self.desc, 1, 1)
        self.grid.addWidget(self.fill, 2, 0)
        self.grid.addWidget(self.message, 2, 1)


    def mousePressEvent(self, event):
        '''Show message if there is one, else hide.'''
        msg_visible = self.message.isVisible()
        print self.cleaner.msg
        if self.cleaner.msg:
            if msg_visible:
                self.setFixedHeight(36)
                self.message.hide()
                self.fill.hide()
            else:
                self.setFixedHeight(76)
                self.message.show()
                self.fill.show()

    def refr(self):
        '''Refresh item from cleaner.'''

        self.status.set(self.cleaner.passed)
        self.label.setText(self.cleaner.full_name)
        self.desc.setText(self.cleaner.description)
        self.message.setText(self.cleaner.msg)


class UI(QtGui.QDockWidget):

    def __init__(self, app, parent=None):
        super(UI, self).__init__(parent)

        self.app = app

        self.widget = QtGui.QWidget(self)
        self.grid = QtGui.QGridLayout(self.widget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setRowStretch(3, 1)
        self.grid.setColumnStretch(0, 1)
        self.widget.setLayout(self.grid)

        self.cleaner_list = CleanerList()

        self.progress_msg = QtGui.QLabel("Run your tests!")
        self.progress_msg.setAlignment(QtCore.Qt.AlignHCenter)

        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.check_button = QtGui.QPushButton()
        self.check_button.setText("Run Checks")
        self.check_button.clicked.connect(self.check)

        self.clean_button = QtGui.QPushButton()
        self.clean_button.setText("Fix Failures")


        self.grid.addWidget(self.progress_msg, 0, 0, 1, 3)
        self.grid.addWidget(self.progress_bar, 1, 0, 1, 3)
        self.grid.addLayout(self.cleaner_list, 2, 0, 1, 3)
        self.grid.addWidget(self.check_button, 4, 1)
        self.grid.addWidget(self.clean_button, 4, 2)


        self.setWidget(self.widget)
        self.setWindowTitle("CleanFreak - Clean your shit up!")

        self.cleaner_items = []
        self.load_context()

        with open(REL("style.css")) as f:
            self.setStyleSheet(f.read())

    def load_context(self):
        if self.cleaner_items:
            for ci in self.cleaner_items:
                ci.setParent(None)
                del(ci)
            self.cleaner_items = []

        for c in self.app.cleaners:
            cleaner_item = CleanerListItem(c)
            self.cleaner_list.addWidget(cleaner_item)
            self.cleaner_items.append(cleaner_item)

        self.refr()

    def check(self):
        self.progress_msg.setText("Running Cleaners...")
        self.progress_bar.setValue(0)
        value_step = 1 / len(self.cleaner_items)

        value = 0
        for c, ci in zip(self.app.cleaners, self.cleaner_items):
            self.progress_msg.setText("{0} checking...".format(c.full_name))
            c._check()
            ci.refr()
            if c.passed:
                value += value_step
            self.progress_bar.setValue(value * 100)

        self.progress_msg.setText(self.app.format_grade())

    def refr(self):
        for ci in self.cleaner_items:
            ci.refr()

    @classmethod
    def create(cls, app):
        '''Overwrite in custom application context passing parent ui.'''
        qtapp = QtGui.QApplication(sys.argv)
        ui = cls(app, parent=None)
        ui.show()
        sys.exit(qtapp.exec_())
