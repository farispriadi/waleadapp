import argparse
import sys
import os
import pathlib
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtWidgets import QApplication
from WALeadApp.views.main_window import MainWindow
from WALeadApp.controllers.main_controller import MainController

PROJECT_PATH = pathlib.Path(os.getcwd()).resolve()
DARK_THEME = str(PROJECT_PATH.joinpath("WALeadApp","assets","dark.qss").resolve())

def main(paid=False):
    app = QApplication(sys.argv)
    file = QFile(DARK_THEME)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    main_window = MainWindow()
    main = MainController(model=None, view=main_window)
    if paid:
        main.unlock_business()

    main.set_project_path(PROJECT_PATH)
    main.show()
    sys.exit(app.exec_())
