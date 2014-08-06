'''
PySide UI
=========
'''
from PySide import QtGui
import sys



class UI(QtGui.QDockWidget):

    def __init__(self, app, parent=None):
        super(UI, self).__init__(parent)

        self.app = app

        self.widget = QtGui.QWidget(self)
        self.layout = QtGui.QGridLayout(self.widget)
        self.widget.setLayout(self.layout)

        self.setWidget(self.widget)
        self.setWindowTitle("CleanFreak - Clean your shit up!")

    @classmethod
    def create(cls, app):
        '''Overwrite in custom application context passing parent ui.'''
        qtapp = QtGui.QApplication(sys.argv)
        ui = cls(app, parent=None)
        ui.show()
        sys.exit(qtapp.exec_())
