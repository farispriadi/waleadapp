# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(AboutDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.app_name = QLabel(AboutDialog)
        self.app_name.setObjectName(u"app_name")
        font = QFont()
        font.setFamily(u"Sans Serif")
        font.setPointSize(20)
        self.app_name.setFont(font)
        self.app_name.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.verticalLayout.addWidget(self.app_name)

        self.version = QLabel(AboutDialog)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout.addWidget(self.version)

        self.wa_version = QLabel(AboutDialog)
        self.wa_version.setObjectName(u"wa_version")
        self.wa_version.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout.addWidget(self.wa_version)

        self.copyright = QLabel(AboutDialog)
        self.copyright.setObjectName(u"copyright")
        self.copyright.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout.addWidget(self.copyright)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"WALeadApp", None))
        self.app_name.setText(QCoreApplication.translate("AboutDialog", u"WALeadApp", None))
        self.version.setText(QCoreApplication.translate("AboutDialog", u"version 1.0", None))
        self.wa_version.setText(QCoreApplication.translate("AboutDialog", u"whatsapp 2.21", None))
        self.copyright.setText(QCoreApplication.translate("AboutDialog", u"Copyright \u00a9 2021 Faris Priadi", None))
    # retranslateUi

