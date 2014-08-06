'''
PySide UI
=========
'''


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
        return cls(app, parent=None)
