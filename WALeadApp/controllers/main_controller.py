import pandas as pd
import pathlib
from WALeadApp.controllers.base import BaseController
import webbrowser
from WALeadApp.models.waleadapp import browser


class MainController(BaseController):
    """Controller for main window
        view : mainwindow object
    """
    def __init__(self, *args, **kwrags):
        super(MainController, self).__init__(*args, **kwrags)
        self.project_path = ''
        self.emoji_displayed = False
        self.attach_displayed = False

    # connect slot to signal in main window
    def show(self):
        self._connect_actions()
        self._connect_buttons()
        self.view.show()

    def unlock_business(self):
        self.view.collect_action.setVisible(True)

    def set_project_path(self,PROJECT_PATH):
        self.project_path = str(PROJECT_PATH)
        
    def show_emoji(self):
        if not self.emoji_displayed:
            if self.attach_displayed:
                self.view.ui.emojiWidget.raise_()
            self.view.ui.emojiWidget.show()
        else:
            self.view.ui.emojiWidget.hide()
        self.view.ui.templateEdit.verticalScrollBar().setValue(self.view.ui.templateEdit.verticalScrollBar().maximum())
        self.emoji_displayed = not self.emoji_displayed

    def show_attach(self):
        if not self.attach_displayed:
            if self.emoji_displayed:
                self.view.ui.attachmentsWidget.raise_()    
            self.view.ui.attachmentsWidget.show()
        else:
            self.view.ui.attachmentsWidget.hide()
        self.view.ui.templateEdit.verticalScrollBar().setValue(self.view.ui.templateEdit.verticalScrollBar().maximum())
        self.attach_displayed = not self.attach_displayed




    def _connect_actions(self):
        self.view.new_action.triggered.connect(self.new)
        self.view.open_action.triggered.connect(self.open)
        self.view.send_action.triggered.connect(self.send)
        self.view.summary_action.triggered.connect(self.summary)
        self.view.collect_action.triggered.connect(self.collect)
        self.view.stop_action.triggered.connect(self.stop)
        self.view.saveas_action.triggered.connect(self.saveas)
        self.view.save_action.triggered.connect(self.save)
        self.view.import_action.triggered.connect(self.import_contacts)
        self.view.import_api_action.triggered.connect(self.import_api_contacts)
        self.view.export_action.triggered.connect(self.export_contacts)
        self.view.about_action.triggered.connect(self.about)
        self.view.docs_action.triggered.connect(self.docs)
        self.view.check_updates_action.triggered.connect(self.check_updates)
        self.view.quit_action.triggered.connect(self.quit)

    def _connect_buttons(self):
        self.view.ui.addContacts.clicked.connect(self.add_contacts)
        self.view.ui.removeContacts.clicked.connect(self.remove_contacts)
        self.view.ui.addAttach.clicked.connect(self.add_attach)
        self.view.ui.removeAttach.clicked.connect(self.remove_attach)
        self.view.ui.emojiButton.clicked.connect(self.show_emoji)
        self.view.ui.attachButton.clicked.connect(self.show_attach)
        self.view.ui.sendButton.clicked.connect(self.send)
        self.view.ui.stopButton.clicked.connect(self.stop)

    def new(self):
        # self.view.ui.templateEdit.setPlainText("This is slot of New")
        self.view.new_gui(str(self.project_path))
        # self.view.load_contacts_gui(str(self.project_path))


    def open(self):
        self.view.load_project_gui(str(self.project_path))

    def import_contacts(self):
        self.view.load_contacts_gui(str(self.project_path))

    def import_api_contacts(self):
        self.view.show_connect_odoo_api()

    def export_contacts(self):
        self.view.save_contacts_gui(str(self.project_path))


    def save(self):
        self.saveas(replace=True)

    def saveas(self, replace=False):
        self.view.save_project_gui(str(self.project_path), replace)

    def quit(self):
        try:
            browser.close()
        except Exception as e:
            print("Error close browser :",e)

        self.view.close_thread()
        self.view.close()

    def send(self):
        self.view.send()

    def collect(self):
        self.view.collect()

    def stop(self):
        self.view.stop()

    def summary(self):
        self.view.show_summary()
        
    def about(self):
        self.view.show_about()

    def docs(self):
        webbrowser.open_new_tab("http://aladeve.com/waleadapp")

    def donate(self):
        pass

    def check_updates(self):
        # webbrowser.open_new_tab("http://aladeve.com/waleadapp") 
        self.view.check_updates(str(self.project_path))       

    def add_attach(self):
        # self.view.ui.templateEdit.setPlainText("Trying add Attachment")
        self.view.load_attachments_gui(str(self.project_path))

    def remove_attach(self):
        self.view.remove_attachment()

    def add_contacts(self):
        self.view.add_contacts()

    def remove_contacts(self):
        self.view.remove_contacts()
