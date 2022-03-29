from PySide2.QtWidgets import QTreeView, QPushButton
from PySide2.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QIcon, QPainter
from PySide2.QtCore import Qt, Signal


class ControlButton(QPushButton):
    def __init__(self, parent=None):
        super(ControlButton, self).__init__(parent)
        self.is_open = False

    def mouseReleaseEvent(self, event):
        super(ControlButton, self).mouseReleaseEvent(event)
        if self.is_open:
            self.setIcon(QIcon("images/On.png"))
        else:
            self.setIcon(QIcon("images/On.png"))
        self.is_open = not self.is_open


class AttachmentsModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(AttachmentsModel, self).__init__(parent)
        self.setHorizontalHeaderLabels(["Media","Location"])

    def data(self, index, role):
        if role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QBrush(QColor(202, 204, 207))
        return super(AttachmentsModel, self).data(index, role)

class AttachmentsView(QTreeView):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super(AttachmentsView, self).__init__(parent)
        model = AttachmentsModel()
        self.root_node = model.invisibleRootItem()
        self.setModel(model)
        self.filenames = []
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)


    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            print("tree view ", self.model().rowCount())
            return
        # print("self.viewport()", self.viewport())
        painter = QPainter(self.viewport())
        painter.save()
        col = self.palette().placeholderText().color()
        painter.setPen(col)
        fm = self.fontMetrics()
        elided_text = fm.elidedText(
            "Drag file atau image", Qt.ElideRight, self.viewport().width()
        )
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        # painter.drawImage(QRect(self.viewport().rect().width()//2, self.viewport().rect().height()//2 + 20, 25, 25), QImage(str(ASSETS_PATH.joinpath("import.png").resolve())))
        painter.restore()

    def addFile(self, filename):
        if filename:
            item_media = QStandardItem(filename.split("/")[-1])
            item_media.setEditable(False)
            item_location = QStandardItem(filename)
            item_location.setEditable(False)
            self.root_node.appendRow([item_media, item_location])
            self.filenames.append(item_location)
        print("Row Count", self.root_node.rowCount())
        return self.root_node.rowCount()

    def addOrReplace(self, filename):
        if self.root_node.rowCount() ==1:
            # replace
            self.removeFile(0)
        self.addFile(filename)

    def getFileNames(self):
        return self.filenames

    def removeFile(self, row_index=None):
        try:
            if row_index is None:
                row_index = self.selectedIndexes()[0].row()
            print("Selected Index",row_index)
            row = self.root_node.takeRow(row_index)
        except Exception as e:
            print("Error removing attachment item: ", e)

        try:
            removed = self.filenames.pop(row_index)
        except Exception as e:
            print("Error removing attachment file: ", e)            
            
    def getRowCount(self):
        return self.root_node.rowCount()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        rowCount = self.root_node.rowCount()
        if event.mimeData().hasFormat("text/uri-list") and rowCount<1:
            event.acceptProposedAction()
            local_file = event.mimeData().urls()[0].toLocalFile()
            self.addOrReplace(local_file)
            self.fileDropped.emit(local_file)
        else:
            self.fileDropped.emit("")


