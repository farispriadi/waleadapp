# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mockup_database.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from WALeadApp.views.summary_view import SummaryTableView, SummaryModel, SummaryChart


class Ui_MainWindow(object):
    table_model = None
    def createSummaryModel(self, data_df):
        self.table_model= SummaryModel(data_df)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)

        self.stackedView = QStackedWidget(self.centralwidget)


        # Dashboard
        self.summaryView = SummaryChart(data_df= self.table_model.contact_df,parent=self.stackedView)
        self.summaryView.setObjectName(u"summaryView")

        # Table
        self.summaryTable = QWidget(self.centralwidget)
        self.summaryTable.setObjectName(u"summaryTable")

        self.tableLayout = QVBoxLayout(self.summaryTable)
        self.tableLayout.setObjectName(u"tableLayout")

        self.export_button = QPushButton(self.centralwidget)
        self.export_button.setObjectName(u"export_button")

        self.horizontalLayout.addWidget(self.export_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.column_combo = QComboBox(self.centralwidget)
        self.column_combo.setObjectName(u"column_combo")

        self.horizontalLayout.addWidget(self.column_combo)

        self.filter_edit = QLineEdit(self.centralwidget)
        self.filter_edit.setObjectName(u"filter_edit")

        self.horizontalLayout.addWidget(self.filter_edit)
        self.tableLayout.addLayout(self.horizontalLayout)


        self.tableView = SummaryTableView(model=self.table_model, parent=self.centralwidget)
        self.tableView.setObjectName(u"summaryTableView")
        self.tableLayout.addWidget(self.tableView)

        
        self.stackedView.addWidget(self.summaryView)
        # self.line = QLineEdit(self.centralwidget)
        # self.stackedView.addWidget(self.line)
        self.stackedView.addWidget(self.summaryTable)

        self.verticalLayout.addWidget(self.stackedView)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.export_button.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.filter_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter", None))
    # retranslateUi

