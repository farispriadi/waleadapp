
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton, QAction
from config import ASSETS_PATH
SEND_DISABLED = str(ASSETS_PATH.joinpath("send_disabled.png").resolve())
SEND = str(ASSETS_PATH.joinpath("send.png").resolve())

STOP_DISABLED = str(ASSETS_PATH.joinpath("stop_disabled.png").resolve())
STOP = str(ASSETS_PATH.joinpath("stop.png").resolve())

class SendAction(QAction):
    """docstring for SendAction"""
    def __init__(self,parent=None):
        super(SendAction, self).__init__(parent)
        self.setIcon(QIcon(SEND))

    def setEnabled(self, args):
        super(SendAction, self).setEnabled(args)
        if args:
            self.setIcon(QIcon(SEND))
        else:
            self.setIcon(QIcon(SEND_DISABLED))


class StopAction(QAction):
    """docstring for StopAction"""
    def __init__(self,parent=None):
        super(StopAction, self).__init__(parent)
        self.setIcon(QIcon(STOP))
        
    def setEnabled(self, args):
        super(StopAction, self).setEnabled(args)
        if args:
            self.setIcon(QIcon(STOP))
        else:
            self.setIcon(QIcon(STOP_DISABLED))


        
        
