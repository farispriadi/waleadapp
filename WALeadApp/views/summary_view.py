from PySide2.QtWidgets import QWidget,QTableView,QAbstractItemView, QHeaderView, QPlainTextEdit, \
                            QVBoxLayout
from PySide2.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QPainter, \
                        QImage, QIcon
from PySide2.QtCore import Qt, QSortFilterProxyModel, QFile, QEvent, QRect, Signal, QRegExp
from config import ASSETS_PATH
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

FAILED_ICON = str(ASSETS_PATH.joinpath("failed.png").resolve())
SENT_ICON = str(ASSETS_PATH.joinpath("sent.png").resolve())
INVALID_ICON = str(ASSETS_PATH.joinpath("invalid.png").resolve())
EMOJI = str(ASSETS_PATH.joinpath("emoji.png").resolve())

COLORS = {'Sent': "#87de87",
            'Failed': "#ffdd55",
            'Invalid': "#de8787",
            'Unsent': "#d8d8d8"
        }

class SummaryChart(QWidget):
    """docstring for SummaryChart"""
    def __init__(self, data_df=pd.DataFrame(),parent=None):
        super(SummaryChart, self).__init__(parent)
        self._data_df = data_df
        
        self._x,self._y,self._xaxis,self._yaxis =self.get_chart_data("status")
        self.create_chart()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self._canvas)

    def create_chart(self):
        matplotlib.rcParams['text.color'] = COLORS["Unsent"]
        matplotlib.rcParams['axes.labelcolor'] = COLORS["Unsent"]
        matplotlib.rcParams['xtick.color'] = COLORS["Unsent"]
        matplotlib.rcParams['ytick.color'] = COLORS["Unsent"]


        self._figure = Figure()
        self._canvas = FigureCanvas(self._figure)
        self._canvas.setParent(self)
        
        self._figure.set_facecolor("none")
        self.setStyleSheet("background-color:#1a1a1a;")

        width = 0.35  # the width of the bars
        x = np.arange(len(self._x))  # the label locations
        self._axes = self._figure.add_subplot(111)
        
        status_reacts = self._axes.bar(x, self._y, width, label='Status')

        self._axes.text(0, self._y[0]+ (0.1*self._y[0]) , "{} {}{} of \nTotal {} contacts".format(self._x[0], self._y[0]/sum(self._y)*100,"%", sum(self._y)), fontsize= 'x-large')

        for idx,x_tick in enumerate(self._x):
            if x_tick not in ["Sent", "Failed","Invalid"]:
                status_reacts[idx].set_color(COLORS["Unsent"])
            else:
                status_reacts[idx].set_color(COLORS[x_tick])

        # Add some text for labels, title and custom x-axis tick labels, etc.
        # self._axes.set_ylabel('Jumlah')

        self._axes.set_facecolor("#1a1a1a")
        self._axes.tick_params(axis='x', colors=COLORS["Unsent"])
        self._axes.set_xticks(x, ["Unsent" if xtick =="" else xtick for xtick in self._x ])
        
        
        # self._axes.bar_label(status_reacts, padding=3) # untuk matplotlib versi 3.5.1
        def autolabel(rects, xpos='center',ax=self._axes):
            """
            Attach a text label above each bar in *rects*, displaying its height.

            *xpos* indicates which side to place the text w.r.t. the center of
            the bar. It can be one of the following {'center', 'right', 'left'}.
            """

            xpos = xpos.lower()  # normalize the case of the parameter
            ha = {'center': 'center', 'right': 'left', 'left': 'right'}
            offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                        '{}'.format(height), ha=ha[xpos], va='bottom')

        
        autolabel(status_reacts)

        self._figure.patch.set_visible(False)
        self._axes.yaxis.set_visible(False)
        self._axes.yaxis.set_ticks([])
        self._axes.xaxis.set_ticks([])


        self._axes.spines["right"].set_visible(False)
        self._axes.spines["top"].set_visible(False)
        self._axes.spines["left"].set_visible(False)
        self._axes.spines["bottom"].set_color(COLORS["Unsent"])        



    def get_chart_data(self,column):
        _data_df = self._data_df.copy()
        #_data_df[column] = _data_df[column].str.replace("","Unsent")
        self.values_count = _data_df[column].value_counts()

        self.values_count = self.values_count.reset_index()
        new_col = []
        for val in self.values_count["index"].tolist():
            if val == "Sent":
                new_col.append(3)
            elif val == "Failed":
                new_col.append(2)
            elif val == "Invalid":
                new_col.append(1)
            else:
                new_col.append(0)

        self.values_count["nilai"] = new_col
        self.values_count = self.values_count.sort_values(by = ['nilai'], ascending = False)

        x= self.values_count["index"].tolist()
        y= self.values_count["status"].tolist()
        xlabel = "Status"
        ylabel = "Jumlah"
        return [x,y,xlabel,ylabel]

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
            "Belum Ada Ringkasan Laporan", Qt.ElideRight, self.viewport().width()
        )
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        painter.restore()


class ModelProxy(QSortFilterProxyModel):
    def headerData(self, section, orientation, role):
        # if display role of vertical headers
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            # return the actual row number
            return section + 1
        # for other cases, rely on the base implementation
        return super(ModelProxy, self).headerData(section, orientation, role)


class SummaryModel(QStandardItemModel):
    """
        Summary model
    """
    def __init__(self, contact_df, parent=None):
        super(SummaryModel, self).__init__(parent)
        
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

        # return super(SummaryModel, self).data(index, role)

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

class SummaryTableView(QTableView):
    """
        Summary table view
    """

    dragged = Signal(bool)
    fileDropped = Signal(str)
    def __init__(self, model, parent=None):
        super(SummaryTableView, self).__init__(parent)
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
            "Drag file Excel atau CSV untuk mengimpor Contacts", Qt.ElideRight, self.viewport().width()
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

    def textFilterChanged(self, filter_text, col):
        search = QRegExp(filter_text,Qt.CaseInsensitive,QRegExp.RegExp)
        self.proxyModel.setFilterRegExp(search)
        self.proxyModel.setFilterKeyColumn(int(col))