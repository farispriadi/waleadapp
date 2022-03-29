
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton, QAction
from config import ASSETS_PATH
SEND_DISABLED = str(ASSETS_PATH.joinpath("send_disabled.png").resolve())
SEND = str(ASSETS_PATH.joinpath("send.png").resolve())

STOP_DISABLED = str(ASSETS_PATH.joinpath("stop_disabled.png").resolve())
STOP = str(ASSETS_PATH.joinpath("stop.png").resolve())

EMOJI_CLOSED = str(ASSETS_PATH.joinpath("emoji_closed.png").resolve())
EMOJI_OPEN = str(ASSETS_PATH.joinpath("emoji_open.png").resolve())

CLIP_CLOSED = str(ASSETS_PATH.joinpath("clip_closed.png").resolve())
CLIP_OPEN = str(ASSETS_PATH.joinpath("clip_open.png").resolve())


class SendButton(QPushButton):
    """docstring for SendButton"""
    def __init__(self,parent=None):
        super(SendButton, self).__init__(parent)
        self.setIcon(QIcon(SEND))

    def setEnabled(self, args):
        super(SendButton, self).setEnabled(args)
        if args:
            self.setIcon(QIcon(SEND))
        else:
            self.setIcon(QIcon(SEND_DISABLED))


class StopButton(QPushButton):
    """docstring for StopButton"""
    def __init__(self,parent=None):
        super(StopButton, self).__init__(parent)
        self.setIcon(QIcon(STOP))
        
    def setEnabled(self, args):
        super(StopButton, self).setEnabled(args)
        if args:
            self.setIcon(QIcon(STOP))
        else:
            self.setIcon(QIcon(STOP_DISABLED))


class EmojiButton(QPushButton):
    def __init__(self, parent=None):
        super(EmojiButton, self).__init__(parent)
        self.is_open = False
        self.setIcon(QIcon(EMOJI_CLOSED))

    def mouseReleaseEvent(self, event):
        super(EmojiButton, self).mouseReleaseEvent(event)
        self.is_open = not self.is_open
        if self.is_open:
            self.setIcon(QIcon(EMOJI_OPEN))
        else:
            self.setIcon(QIcon(EMOJI_CLOSED))

class ClipButton(QPushButton):
    def __init__(self, parent=None):
        super(ClipButton, self).__init__(parent)
        self.is_open = False
        self.setIcon(QIcon(CLIP_CLOSED))

    def mouseReleaseEvent(self, event):
        super(ClipButton, self).mouseReleaseEvent(event)
        self.is_open = not self.is_open
        if self.is_open:
            self.setIcon(QIcon(CLIP_OPEN))
        else:
            self.setIcon(QIcon(CLIP_CLOSED))
        


        
        
