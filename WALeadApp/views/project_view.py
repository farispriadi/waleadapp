from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Qt

class ProjectName(QLineEdit):
	"""docstring for ProjectName"""
	def __init__(self, parent=None):
		super(ProjectName, self).__init__(parent)
		self.setText("Untitled")
		self.setReadOnly(True)
		
		
	def mouseDoubleClickEvent(self, event):
		self.setReadOnly(False)
		super(ProjectName, self).mouseDoubleClickEvent(event)

	def focusOutEvent(self, event):
		# current_state = self.isReadOnly()
		self.setReadOnly(True)
		super(ProjectName, self).focusOutEvent(event)