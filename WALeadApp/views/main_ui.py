# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from WALeadApp.views.contacts_view import ContactsView, ContactsModel, EmptyTable
from WALeadApp.views.attachments_view import AttachmentsView
from WALeadApp.views.project_view import ProjectName
from WALeadApp.views.progress_bar_view import CollectingBar
from WALeadApp.views.emoji_view import EmojiView, EmojiWidget
from WALeadApp.views.template_view import TemplateView
from WALeadApp.views.button_view import SendButton, StopButton, EmojiButton, ClipButton
from WALeadApp.views.icons_rc import *
from config import ASSETS_PATH

SEND_ICON = str(ASSETS_PATH.joinpath("send.png").resolve())
STOP_ICON = str(ASSETS_PATH.joinpath("stop.png").resolve())
EMOJI_ICON = str(ASSETS_PATH.joinpath("emoji_closed.png").resolve())
CLIP_ICON = str(ASSETS_PATH.joinpath("clip_closed.png").resolve())
ADD_ICON = str(ASSETS_PATH.joinpath("plus.png").resolve())
REMOVE_ICON = str(ASSETS_PATH.joinpath("minus.png").resolve())



class Ui_MainWindow(object):

    contact_model = None
    def createContactsModel(self, contact_df):
        self.contact_model= ContactsModel(contact_df)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionSendMesage = QAction(MainWindow)
        self.actionSendMesage.setObjectName(u"actionSendMesage")
        self.actionCollectResponse = QAction(MainWindow)
        self.actionCollectResponse.setObjectName(u"actionCollectResponse")
        self.actionSummary = QAction(MainWindow)
        self.actionSummary.setObjectName(u"actionSummary")
        self.actionDocs = QAction(MainWindow)
        self.actionDocs.setObjectName(u"actionDocs")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionCheckUpdate = QAction(MainWindow)
        self.actionCheckUpdate.setObjectName(u"actionCheckUpdate")
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionShowContacts = QAction(MainWindow)
        self.actionShowContacts.setObjectName(u"actionShowContacts")
        self.actionShowAttachments = QAction(MainWindow)
        self.actionShowAttachments.setObjectName(u"actionShowAttachments")
        self.actionShowEmoji = QAction(MainWindow)
        self.actionShowEmoji.setObjectName(u"actionShowEmoji")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.templateLayout = QVBoxLayout()
        self.templateLayout.setObjectName(u"templateLayout")
        self.templateLayout.setContentsMargins(-1, 0, -1, -1)
        self.projectNameLayout = QHBoxLayout()
        self.projectNameLayout.setObjectName(u"projectNameLayout")
        self.projectNameLayout.setContentsMargins(-1, 10, -1, -1)
        self.projectLabel = QLabel(self.centralwidget)
        self.projectLabel.setObjectName(u"projectLabel")
        self.projectName = ProjectName(self.centralwidget)
        self.projectName.setObjectName(u"projectName")

        self.projectNameLayout.addWidget(self.projectLabel)
        self.projectNameLayout.addWidget(self.projectName)


        self.templateLayout.addLayout(self.projectNameLayout)
        self.projectName.setVisible(False)
        self.projectLabel.setVisible(False)

        # self.templateEdit = QPlainTextEdit(self.centralwidget)
        self.templateEdit = TemplateView(self.centralwidget)
        # completer = QCompleter(self.centralwidget)
        # completer_model = QStringListModel(["nama", "jabatan"])
        # completer.setModel(completer_model)
        # completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        # completer.setCaseSensitivity(Qt.CaseInsensitive)
        # completer.setWrapAround(False)
        # self.templateEdit.setCompleter(completer)        
        self.templateEdit.setObjectName(u"templateEdit")
        self.templateEdit.setPlaceholderText(u"Type a message")
        self.templateEdit.setTabStopDistance(QFontMetricsF(self.templateEdit.font()).horizontalAdvance(' ') * 4)

        self.templateLayout.addWidget(self.templateEdit)


        self.verticalLayout_4.addLayout(self.templateLayout)



        self.emojiButton = EmojiButton("")
        self.attachButton = ClipButton("")
        self.sendButton = SendButton("")
        self.stopButton = StopButton("")
        self.buttonSpacer = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonLayout = QHBoxLayout()

        self.buttonLayout.addWidget(self.emojiButton)
        self.buttonLayout.addWidget(self.attachButton)
        self.buttonLayout.addItem(self.buttonSpacer)
        self.buttonLayout.addWidget(self.sendButton)
        self.buttonLayout.addWidget(self.stopButton)

        self.verticalLayout_4.addLayout(self.buttonLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSend = QMenu(self.menubar)
        self.menuSend.setObjectName(u"menuSend")
        self.menuReport = QMenu(self.menubar)
        self.menuReport.setObjectName(u"menuReport")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.emojiWidget = EmojiWidget(MainWindow)
        self.emojiWidget.setObjectName(u"emojiWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.emojiLayout = QVBoxLayout()
        self.emojiLayout.setObjectName(u"emojiLayout")
        self.emojiLayout.setContentsMargins(-1, 0, -1, -1)
        self.emojiView = EmojiView(self.dockWidgetContents)
        self.emojiView.setObjectName(u"emojiView")

        self.emojiLayout.addWidget(self.emojiView)


        self.verticalLayout_2.addLayout(self.emojiLayout)

        self.emojiWidget.setWidget(self.dockWidgetContents)
        
        self.attachmentsWidget = QDockWidget(MainWindow)
        self.attachmentsWidget.setObjectName(u"attachmentsWidget")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout_6 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.buttonAttachmentLayout = QHBoxLayout()
        self.buttonAttachmentLayout.setObjectName(u"buttonAttachmentLayout")
        self.buttonAttachmentLayout.setContentsMargins(-1, 0, -1, -1)
        self.addAttach = QPushButton(self.dockWidgetContents_3)
        self.addAttach.setObjectName(u"addAttach")

        self.buttonAttachmentLayout.addWidget(self.addAttach)

        self.removeAttach = QPushButton(self.dockWidgetContents_3)
        self.removeAttach.setObjectName(u"removeAttach")

        self.buttonAttachmentLayout.addWidget(self.removeAttach)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonAttachmentLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.buttonAttachmentLayout)

        self.attachmentsTree = AttachmentsView(self.dockWidgetContents_3)
        self.attachmentsTree.setObjectName(u"attachmentsTree")

        self.verticalLayout_5.addWidget(self.attachmentsTree)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.attachmentsWidget.setWidget(self.dockWidgetContents_3)
        
        self.contactsWidget = QDockWidget(MainWindow)
        self.contactsWidget.setObjectName(u"contactsWidget")
        self.contactsWidgetContents = QWidget()
        self.contactsWidgetContents.setObjectName(u"contactsWidgetContents")
        self.verticalLayout_8 = QVBoxLayout(self.contactsWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.contactsLayout = QVBoxLayout()
        self.contactsLayout.setSpacing(3)
        self.contactsLayout.setObjectName(u"contactsLayout")
        self.contactsLayout.setContentsMargins(-1, 0, -1, -1)
        self.progressBar = CollectingBar(self.contactsWidgetContents)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.progressBarLabel = QLabel(self.contactsWidgetContents)
        self.progressBarLabel.setObjectName(u"progressBarLabel")

        # self.contactsLayout.addWidget(self.progressBar)
        self.progressLayout = QHBoxLayout()
        self.progressLayout.setObjectName(u"progressLayout")
        self.progressLayout.setContentsMargins(-1, 0, -1, -1)
        self.progressLabelLayout = QVBoxLayout()
        self.progressLabelLayout.setObjectName(u"progressLabelLayout")
        self.progressLabelLayout.setContentsMargins(-1, 0, -1, -1)
        self.progressLabelLayout.setSpacing(20)
        
        self.progressLayout.addWidget(self.progressBar)
        
        self.contactsLayout.addLayout(self.progressLayout)
        self.progressLabelLayout.addWidget(self.progressBarLabel)
        self.contactsLayout.addLayout(self.progressLabelLayout)

        ## Button add contacts
        self.addContacts = QPushButton(self.dockWidgetContents)
        self.addContacts.setObjectName(u"addContacts")

        self.removeContacts = QPushButton(self.dockWidgetContents)
        self.removeContacts.setObjectName(u"removeContacts")

        self.contactsControlLayout = QHBoxLayout()
        self.contactsControlLayout.setObjectName(u"progressLayout")
        self.contactsControlLayout.setContentsMargins(-1, 0, -1, -1)

        self.contactsControlLayout.addWidget(self.addContacts)
        self.contactsControlLayout.addWidget(self.removeContacts)
        self.horizontalSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.contactsControlLayout.addItem(self.horizontalSpacer2)

        self.contactsLayout.addLayout(self.contactsControlLayout)

        # self.contactsTable = QTableView(self.contactsWidgetContents)
        self.contactsTable = ContactsView(model=self.contact_model,parent=self.contactsWidgetContents)
        
        self.contactsTable.setObjectName(u"contactsTable")

        self.contactsLayout.addWidget(self.contactsTable)

        self.emptyTable = EmptyTable()
        self.emptyTable.setReadOnly(True)

        self.contactsLayout.addWidget(self.emptyTable)
        self.emptyTable.hide()

        self.verticalLayout_8.addLayout(self.contactsLayout)

        self.contactsWidget.setWidget(self.contactsWidgetContents)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.contactsWidget)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.emojiWidget)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.attachmentsWidget)
        # MainWindow.tabifyDockWidget(self.contactsWidget,self.emojiWidget)
        # MainWindow.tabifyDockWidget(self.emojiWidget,self.attachmentsWidget)

        MainWindow.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)
        MainWindow.setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.North)
        MainWindow.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.North)

        self.contactsWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.attachmentsWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.emojiWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSend.menuAction())
        self.menubar.addAction(self.menuReport.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"SaveAs", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionSendMesage.setText(QCoreApplication.translate("MainWindow", u"Send Mesage", None))
        self.actionCollectResponse.setText(QCoreApplication.translate("MainWindow", u"Collect Response", None))
        self.actionSummary.setText(QCoreApplication.translate("MainWindow", u"Summary", None))
        self.actionDocs.setText(QCoreApplication.translate("MainWindow", u"Docs", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionCheckUpdate.setText(QCoreApplication.translate("MainWindow", u"Check Updates", None))
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop ", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionShowContacts.setText(QCoreApplication.translate("MainWindow", u"Show Contacts", None))
        self.actionShowAttachments.setText(QCoreApplication.translate("MainWindow", u"Show Attachments", None))
        self.actionShowEmoji.setText(QCoreApplication.translate("MainWindow", u"Show Emoji", None))
        self.projectLabel.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.projectName.setText(QCoreApplication.translate("MainWindow", u"Untitled", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSend.setTitle(QCoreApplication.translate("MainWindow", u"Send", None))
        self.menuReport.setTitle(QCoreApplication.translate("MainWindow", u"Report", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.emojiWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Emoji", None))
        self.attachmentsWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Attachments", None))
        self.addAttach.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.removeAttach.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.addContacts.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.removeContacts.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.contactsWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Contacts", None))
        self.progressBarLabel.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.addAttach.setIcon(QIcon(ADD_ICON))
        self.addAttach.setFlat(True)
        self.removeAttach.setIcon(QIcon(REMOVE_ICON))
        self.removeAttach.setFlat(True)
        self.addContacts.setIcon(QIcon(ADD_ICON))
        self.addContacts.setFlat(True)
        self.removeContacts.setIcon(QIcon(REMOVE_ICON))
        self.removeContacts.setFlat(True)
        BUTTON_SIZE = QSize(100,50)
        ICON_BUTTON_SIZE =QSize(50, 25)
        self.emojiButton.setIcon(QIcon(EMOJI_ICON))
        self.emojiButton.setIconSize(ICON_BUTTON_SIZE)
        self.emojiButton.setMinimumSize(BUTTON_SIZE)
        self.attachButton.setIcon(QIcon(CLIP_ICON))
        self.attachButton.setIconSize(ICON_BUTTON_SIZE)
        self.attachButton.setMinimumSize(BUTTON_SIZE)
        self.sendButton.setIcon(QIcon(SEND_ICON))
        self.sendButton.setMinimumSize(BUTTON_SIZE)
        self.sendButton.setIconSize(ICON_BUTTON_SIZE)
        self.stopButton.setIcon(QIcon(STOP_ICON))
        self.stopButton.setIconSize(ICON_BUTTON_SIZE)
        self.stopButton.setMinimumSize(BUTTON_SIZE)
    # retranslateUi

