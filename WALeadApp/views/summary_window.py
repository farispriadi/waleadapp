import pandas as pd
from PySide2.QtWidgets import QMainWindow, QFileDialog, QAction, QToolBar
from PySide2.QtCore import Qt, QSortFilterProxyModel
from PySide2.QtGui import QIcon
from WALeadApp.views import summary_ui
from config import ROOT_PATH


class SummaryWindow(QMainWindow):
    def __init__(self, data_df = pd.DataFrame(),icon=None, main_window=None):
        super(SummaryWindow, self).__init__()
        self.main_window = main_window
        self._data_df = data_df
        self.ui = summary_ui.Ui_MainWindow()
        self.ui.createSummaryModel(data_df)
        self.ui.setupUi(self)
        self.ui.column_combo.addItems(self.ui.tableView.tableModel.header_data)
        self.ui.column_combo.setCurrentText("status")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        self.setWindowTitle("Summary Report")
        self._create_actions()
        self._create_toolbars()
        self._connect_actions()

        self.ui.filter_edit.textChanged.connect(self.filter_result)
        self.ui.column_combo.currentIndexChanged.connect(self.filter_column_changed)
        self.ui.export_button.clicked.connect(self.export_excel)

    def _create_actions(self):
        self.plot_action = QAction(self)
        self.plot_action.setText("&Dashboard")
        # self.plot_action.setIcon(QIcon(":icon/new"))
        self.table_action = QAction(self)
        self.table_action.setText("&Table")
        # self.table_action.setIcon(QIcon(":icon/new"))
    def _create_toolbars(self):
        self.summary_toolbar = QToolBar("Summary", self)
        self.addToolBar(self.summary_toolbar)
        self.summary_toolbar.addActions([self.plot_action, \
                                    self.table_action]
                                    )
        
    def _connect_actions(self):
        self.plot_action.triggered.connect(self.open_dashboard)
        self.table_action.triggered.connect(self.open_table)

    def open_dashboard(self):
        self.ui.stackedView.setCurrentIndex(0)
    def open_table(self):
        self.ui.stackedView.setCurrentIndex(1)
        

    

    def filter_column_changed(self,col):
        text = self.ui.filter_edit.text()
        self.ui.tableView.textFilterChanged(text,col)

    def filter_result(self, text):
        col_name = str(self.ui.column_combo.currentText()).lower()
        lower_cols = [str(val).lower() for val in list(self._data_df.columns)]
        col = lower_cols.index(col_name)
        self.ui.tableView.textFilterChanged(text,col)

    def get_data(self):
        return self._data_df

    def export_excel(self):
        self.main_window.save_contacts_gui(str(ROOT_PATH))

