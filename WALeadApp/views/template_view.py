from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *



class TemplateView(QPlainTextEdit):
    def __init__(self, parent=None):
        super(TemplateView, self).__init__(parent)
        self.completer = None
        self.last_char = ""

    def setCompleter(self, completer):
        if self.completer:
            self.completer.disconnect(self)

        self.completer = completer
        if not self.completer:
            return

        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def getCompleter(self):
        return self.completer

    def insertCompletion(self, completion):
        if self.completer.widget() != self:
            return
        tc = self.textCursor()
        extra = " {"+completion+"}"
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(extra)
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        super().focusInEvent(event)

    def keyPressEvent(self,event):

        super().keyPressEvent(event)
        if self.completer and self.completer.popup().isVisible():
                if event.key() in [Qt.Key_Enter,Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]:
                    event.ignore()
                    return
        isShortcut = (event.modifiers()==Qt.ControlModifier) and (event.key() == Qt.Key_Space)
        
        if isShortcut:
            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0)+ self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
