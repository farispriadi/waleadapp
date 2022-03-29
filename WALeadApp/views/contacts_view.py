from PySide2.QtWidgets import QTableView,QAbstractItemView, QHeaderView, QPlainTextEdit
from PySide2.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QPainter, \
                        QImage, QIcon
from PySide2.QtCore import Qt, QSortFilterProxyModel, QFile, QEvent, QRect, Signal
from config import ASSETS_PATH
import pandas as pd
import numpy as np

FAILED_ICON = str(ASSETS_PATH.joinpath("failed.png").resolve())
SENT_ICON = str(ASSETS_PATH.joinpath("sent.png").resolve())
INVALID_ICON = str(ASSETS_PATH.joinpath("invalid.png").resolve())
EMOJI = str(ASSETS_PATH.joinpath("emoji.png").resolve())


class EmptyTable(QPlainTextEdit):
    dropped = Signal(bool)
    fileDropped = Signal(str)
    draggedLeave = Signal(bool)
    def __init__(self, parent=None):
        super(EmptyTable, self).__init__(parent)
        self.wasReadOnly = True

    def dropEvent(self, event):
        print('event.mimeData().hasFormat("text/uri-list")',event.mimeData().hasFormat("text/uri-list"))
        if event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()
            local_file = event.mimeData().urls()[0].toLocalFile()
            print("local_file", local_file)
            self.fileDropped.emit(local_file)
            self.dropped.emit(True)
            if self.wasReadOnly:
                self.setReadOnly(True)
                self.hide()
        else:
            self.fileDropped.emit("")
            self.dropped.emit(False)

    def dragEnterEvent(self, event):
        print("dragEnterEvent")
        if self.isReadOnly():
            self.setReadOnly(False)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        print("dragLeaveEvent")
        if self.wasReadOnly:
            self.setReadOnly(True)
        self.draggedLeave.emit(True)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        painter.save()
        col = self.palette().placeholderText().color()
        painter.setPen(col)
        fm = self.fontMetrics()
        elided_text = fm.elidedText(
            "Import Contacts dari Excel atau CSV file\n File Contacts harus berisi kolom 'phone' atau 'mobile' ", Qt.ElideRight, self.viewport().width()
        )
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        painter.drawImage(QRect(self.viewport().rect().width()//2, self.viewport().rect().height()//2 + 20, 25, 25), QImage(str(ASSETS_PATH.joinpath("import.png").resolve())))
        painter.restore()


class ModelProxy(QSortFilterProxyModel):
    def headerData(self, section, orientation, role):
        # if display role of vertical headers
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            # return the actual row number
            return section + 1
        # for other cases, rely on the base implementation
        return super(ModelProxy, self).headerData(section, orientation, role)


class ContactsModel(QStandardItemModel):
    """
        Contacts model
    """
    def __init__(self, contact_df, parent=None):
        super(ContactsModel, self).__init__(parent)
        
        self.contact_df = contact_df
        self.displayed_contact_df = contact_df.copy()
        if 'token' in self.displayed_contact_df.columns:
            self.displayed_contact_df.drop('token',inplace=True, axis=1)

        if 'row' in self.displayed_contact_df.columns:
            self.displayed_contact_df.drop('row',inplace=True, axis=1)

        if 'responses' in self.displayed_contact_df.columns:
            self.displayed_contact_df.drop('responses',inplace=True, axis=1) 

        if 'replied' in self.displayed_contact_df.columns:
            self.displayed_contact_df.drop('replied',inplace=True, axis=1) 

        self.header_data = [str(col).lower().strip().replace("_"," ") for col in self.displayed_contact_df.columns]
        self.setHorizontalHeaderLabels(self.header_data)

        for idx_row, row in contact_df.iterrows():
            for idx_col, col in enumerate(self.displayed_contact_df.columns):
                item = QStandardItem(str(row[col]))
                item.setIcon(QIcon(EMOJI))
                if col in list(self.displayed_contact_df.columns)[-4:]:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setEnabled(False)
                self.setItem(idx_row, idx_col, item)

    def data(self, index, role):
        if index.isValid():
            if role == Qt.ForegroundRole:
                if index.row() < len(self.displayed_contact_df.index):
                    value = self.displayed_contact_df.at[index.row(),'status']
                    if value == 'Sent':
                        return QBrush(QColor(0, 85, 0))
                    elif value == 'Invalid':
                        return QBrush(QColor(170, 0, 0))
                    elif value == 'Failed':
                        return QBrush(QColor(255, 85, 0))

            if role == Qt.DecorationRole:
                if index.row() < len(self.displayed_contact_df.index):

                    value = self.displayed_contact_df.at[index.row(),'status']
                    if index.column() == 0:
                        if value == 'Sent':
                            return QIcon(SENT_ICON)
                        elif value == 'Invalid':
                            return QIcon(INVALID_ICON)
                        elif value == 'Failed':
                            return QIcon(FAILED_ICON)

            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = ""
                if index.row() < len(self.displayed_contact_df.index):
                    col_name = self.displayed_contact_df.columns[index.column()]
                    value = self.displayed_contact_df[col_name][index.row()]
                    if type(value) in [float, np.float64]:
                        if str(value) in ["nan","NaN"]:
                            value = ""
                return str(value)

        # return super(ContactsModel, self).data(index, role)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            col_name = self.displayed_contact_df.columns[index.column()]
            self.displayed_contact_df[col_name][index.row()] = value
            if col_name in self.contact_df.columns:
                self.contact_df[col_name][index.row()] = value
            return True
        return False

    def getContacts(self):
        return self.contact_df

class ContactsView(QTableView):
    """
        Contacts table view
    """

    dragged = Signal(bool)
    fileDropped = Signal(str)
    def __init__(self, model, parent=None):
        super(ContactsView, self).__init__(parent)
        self.update_model(model)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            return
        # print("self.viewport()", self.viewport())
        painter = QPainter(self.viewport())
        painter.save()
        col = self.palette().placeholderText().color()
        painter.setPen(col)
        fm = self.fontMetrics()
        elided_text = fm.elidedText(
            "Drag file Excel atau CSV untuk mengimpor Contacts.\nFile harus berisi kolom 'phone' atau 'mobile'", Qt.ElideRight, self.viewport().width()
        )
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        painter.drawImage(QRect(self.viewport().rect().width()//2, self.viewport().rect().height()//2 + 20, 25, 25), QImage(str(ASSETS_PATH.joinpath("import.png").resolve())))
        painter.restore()
        

    def update_model(self, model=None):
        if model:
            self.proxyModel = ModelProxy()
            self.tableModel = model
            self.proxyModel.setSourceModel(self.tableModel)    
            self.setSortingEnabled(True)
            self.setModel(self.proxyModel)
        if self.model():
            self.setWordWrap(True)
            self.setTextElideMode(Qt.ElideNone)
            self.setSelectionMode(QAbstractItemView.SingleSelection)
            self.setSelectionBehavior(QAbstractItemView.SelectRows)

            hhdr = self.horizontalHeader()            
            for col in range(len(self.tableModel.header_data)):
                hhdr.setSectionResizeMode(col, QHeaderView.ResizeToContents)
    def reset_model(self):
        try:
            self.proxyModel.deleteLater()
        except:
            print("Error reset Table View")
    def dragEnterEvent(self, event):
        # super().dragEnterEvent(event)
        if event.mimeData().hasFormat("text/uri-list"):
            print("accepted_formats")
            event.acceptProposedAction()
        if self.model() is None:
            self.hide()
            self.dragged.emit(True)
        else:
            self.dragged.emit(False)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()
            local_file = event.mimeData().urls()[0].toLocalFile()
            self.fileDropped.emit(local_file)
        else:
            self.fileDropped.emit("")

    def removeRow(self, row_indexes=None):
        model = self.tableModel
        try:
            if row_indexes is None:
                row_indexes = self.selectionModel().selectedRows() 

            indexes = []
            for index in sorted(row_indexes, reverse=True):
                model.removeRow(index.row())
                indexes.append(index.row())
            model.contact_df = model.contact_df.drop(model.contact_df.index[indexes])
            model.displayed_contact_df = model.displayed_contact_df.drop(model.displayed_contact_df.index[indexes])
        except Exception as e:
            print("Error removing row: ", e)

    def addRow(self):
        if hasattr(self,'tableModel'):
            model = self.tableModel
            items = []
            col_number=len(self.tableModel.header_data)
            if col_number:
                for col in range(col_number):
                    item = QStandardItem(str(''))
                    if col_number - col <=4:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        item.setEnabled(False)
                    items.append(item)
                model.appendRow(items)
                new_row = pd.DataFrame([["" for col in model.contact_df.iloc[0]]],columns=model.contact_df.columns, dtype=str)
                model.contact_df = pd.concat([model.contact_df,new_row], ignore_index=True)

                new_displayed_row = pd.DataFrame([["" for col in model.displayed_contact_df.iloc[0]]],columns=model.displayed_contact_df.columns, dtype=str)
                model.displayed_contact_df = pd.concat([model.displayed_contact_df,new_displayed_row], ignore_index=True)

        
        

    

    

        




