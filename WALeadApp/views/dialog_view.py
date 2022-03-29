from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, \
                        QDialogButtonBox, QPushButton, QFormLayout, \
                        QLineEdit, QComboBox, QHBoxLayout, QSpacerItem, \
                        QSizePolicy, QGroupBox, QCheckBox

from PySide2.QtGui import QIcon, QPixmap 
from PySide2.QtCore import Qt
from WALeadApp.views import about_ui
from WALeadApp.views import progress_bar_view
import sys
import chromedriver_autoinstaller
import urllib
import jsonrpc_client
import pandas as pd
# from WALeadApp import secret


class NotifDialog(QDialog):
    def __init__(self, message ,icon=None, parent=None):
        super(NotifDialog, self).__init__(parent)
        self.message = message
        self.setWindowTitle("Hai")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        self._layout = QVBoxLayout(self)
        self._label = QLabel(self.message)
        self._buttons_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self._buttons_box.accepted.connect(self.accept)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

class ResendDialog(QDialog):
    def __init__(self, message ,icon=None, parent=None):
        super(ResendDialog, self).__init__(parent)
        self.message = message
        self._resend = None
        self.setWindowTitle("Hai")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        self._layout = QVBoxLayout(self)
        self._label = QLabel(self.message)
        self._buttons_box = QDialogButtonBox()
        self.resendFailed = QPushButton(self.tr("&Ya"))
        self.resendFailed.setDefault(False)

        self.resendAll = QPushButton(self.tr("&Kirim Semua"))
        self.resendAll.setAutoDefault(False)

        self.cancel = QPushButton(self.tr("&Batal"))
        self.cancel.setAutoDefault(True)

        self._buttons_box.addButton(self.cancel, QDialogButtonBox.RejectRole)
        self._buttons_box.addButton(self.resendFailed, QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.resendAll, QDialogButtonBox.ActionRole)        
        
        
        self._buttons_box.rejected.connect(self.reject)
        self.resendFailed.clicked.connect(self.accept_resend_failed)
        self.resendAll.clicked.connect(self.accept_resend_all)


        self._layout.addWidget(self._label)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

    def accept_resend_failed(self):
        print("Resend Failed")
        self._resend = 'failed'
        self.accept()

    def accept_resend_all(self):
        print("Resend All")
        self._resend = 'all'
        self.accept()

    def getResendMode(self):
        return self._resend

class AboutDialog(QDialog):
    def __init__(self, app_name, version, wa_version, copyright ,icon=None, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = about_ui.Ui_AboutDialog()
        self.ui.setupUi(self)
        self.app_name = app_name
        self.version  = version
        self.wa_version = wa_version
        self.copyright = copyright
        self.setWindowTitle(self.app_name)
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        self.ui.app_name.setText(self.app_name)
        self.ui.version.setText(self.version)
        self.ui.wa_version.setText(self.wa_version)
        self.ui.copyright.setText(self.copyright)
        self._layout = self.ui.verticalLayout

        self._buttons_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self._buttons_box.accepted.connect(self.accept)

        self._layout.addWidget(self._buttons_box)

class NewDialog(QDialog):
    def __init__(self, message ,icon=None, parent=None):
        super(NewDialog, self).__init__(parent)
        self.message = message
        self._is_save = False
        self.setWindowTitle("Hai")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        self._layout = QVBoxLayout(self)
        self._label = QLabel(self.message)
        self._buttons_box = QDialogButtonBox()
        self.save = QPushButton(self.tr("&Simpan"))
        self.save.setDefault(False)

        self.ignored = QPushButton(self.tr("&Abaikan"))
        self.ignored.setAutoDefault(False)

        self.cancel = QPushButton(self.tr("&Batal"))
        self.cancel.setAutoDefault(True)

        self._buttons_box.addButton(self.cancel, QDialogButtonBox.RejectRole)
        self._buttons_box.addButton(self.save, QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.ignored, QDialogButtonBox.ActionRole)        
        
        
        self._buttons_box.rejected.connect(self.reject)
        self.save.clicked.connect(self.accept_save)
        self.ignored.clicked.connect(self.accept_ignored)


        self._layout.addWidget(self._label)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

    def accept_save(self):
        print("save before closed")
        self._is_save = True
        self.accept()

    def accept_ignored(self):
        print("ignored")
        self._is_save = False
        self.accept()

    def getSaveMode(self):
        return self._is_save

class ConnectOdooAPIDialog(QDialog):
    
    # password_modified = Signal(str)
    # warning_login = Signal(str)
    def __init__(self, main_window,icon=None, parent=None):
        super(ConnectOdooAPIDialog, self).__init__(parent)
        self.setWindowTitle("Import Contacts From Odoo API")
        self.setMinimumWidth(600)
        self.setMinimumWidth(400)
        self.main_window = main_window
        self.login_data = getattr(main_window,'login_data') if hasattr(main_window,'login_data') else {}
        self.contacts_tags = ["Prospects","Customers"]
        if not hasattr(main_window,'is_api_connected'):
            self.is_connected = False
        else:
            self.is_connected = getattr(main_window,'is_api_connected')

        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        else:
            url = "https://raw.githubusercontent.com/aladeveloper/aladeveloper.github.io/master/assets/img/icons/favicon-64x64.png"   
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.setWindowIcon(QIcon(pixmap))

        self._layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()

        self.url = QLineEdit()
        self.database = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.Password)
        self.remember = QCheckBox("Remember me")

        for key, val in self.login_data.items():
            lineedit = getattr(self,key)
            if type(lineedit) is QLineEdit:
                lineedit.setText(val)
            if type(lineedit) is QCheckBox:
                print('self.login_data["remember"]',val)
                if val:
                    self.remember.setCheckState(Qt.Checked)
                else:
                    self.remember.setCheckState(Qt.Unchecked)

        self.api_label = QLabel("Odoo API Connection")
        self.url_label = QLabel("URL")
        self.database_label = QLabel("Database")
        self.username_label = QLabel("Username")
        self.password_label = QLabel("Password")
        self.api_key_label = QLabel("API Keys")
        self.connect_info_label = QLabel("Status")
        self.remember_label = QLabel("")
       

        self.warning = QLabel("")
        self.api_options = QComboBox()
        self.connect_info = QLineEdit()
        self.connect_info.setText("Connected")
        self.connect_info.setEnabled(False)
        self.connect_button = QPushButton(self.tr("&Connect API"))
        self.import_button = QPushButton(self.tr("&Import Contacts"))
        self.cancel_button = QPushButton(self.tr("&Cancel"))

        self._progress_bar = progress_bar_view.ProgressBar()
        self._progress_bar.setVisible(False)

        self.tags_group = QGroupBox(self)
        self.tags_group.setTitle("&Contacts Options")
        self.tags_options = QComboBox(self.tags_group)
        self.field_options = QComboBox(self.tags_group)
        self._outer_group_layout = QVBoxLayout(self.tags_group)
        self._group_layout = QFormLayout()
        self._group2_layout = QFormLayout()
        self.group_label = QLabel("Select Contacts By Tags")
        self.group2_label = QLabel("Select Field as Phone Column")
        self._group_layout.addRow(self.tr('Contacts Tags'),self.tags_options)
        self._group2_layout.addRow(self.tr('Phone Column'),self.field_options)
        self._outer_group_layout.addWidget(self.group_label)
        self._outer_group_layout.addLayout(self._group_layout)
        self._outer_group_layout.addWidget(self.group2_label)
        self._outer_group_layout.addLayout(self._group2_layout)

        self._buttons_box = QDialogButtonBox()
        self._buttons_box.addButton(self.import_button,QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.connect_button,QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.cancel_button, QDialogButtonBox.ActionRole)
        self.import_button.clicked.connect(self.accept_action)
        self.cancel_button.clicked.connect(self.reject)
        self.connect_button.clicked.connect(self.connect_api)

        # self._form_layout.addRow(self.tr('API Type'),self.api_options)
        self._form_layout.addRow(self.connect_info_label,self.connect_info)
        self._form_layout.addRow(self.url_label,self.url)
        self._form_layout.addRow(self.database_label,self.database)
        self._form_layout.addRow(self.username_label,self.username)
        self._form_layout.addRow(self.password_label,self.password)
        self._form_layout.addRow(self.api_key_label,self.api_key)
        self._form_layout.addRow(self.remember_label,self.remember)
        self.connect_info.setVisible(self.is_connected)
        self.tags_group.setVisible(self.is_connected)
        self.import_button.setEnabled(self.is_connected)
        self.connect_info_label.setVisible(self.is_connected)
        self.connect_info.setVisible(self.is_connected)

        self.api_options.currentIndexChanged.connect(self.select_api_type)
        self.remember.stateChanged.connect(self.stay_login)

        self.api_options.addItems(["API Keys","External API"])
        self.tags_options.addItems(self.contacts_tags)
        self.field_options.addItems(["Phone","Mobile"])

        self._vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._layout.addWidget(self.api_label)
        self._layout.addLayout(self._form_layout)
        self._layout.addWidget(self.tags_group)
        self._layout.addWidget(self._progress_bar)
        self._layout.addItem(self._vspacer)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

        if self.login_data:
            if "remember" in self.login_data.keys() and self.login_data["remember"]:
                if self.login_data["remember"]:
                    self.import_button.setEnabled(False)
                    self.connect_button.setEnabled(False)
                    status = self.connect_api()
                


    def stay_login(self, stay=True):
        stay = self.remember.isChecked()
        if stay == Qt.Checked:
            self.login_data["remember"] = True
        else:
            self.login_data["remember"] = False


    def connect_api(self):
        self.import_button.setEnabled(False)
        self.connect_button.setEnabled(False)
        idx = self.api_options.currentIndex()
        url = self.url.text()
        self.login_data["url"] = url
        if  self.remember.isChecked():
            self.login_data["remember"] = True
        else:
            self.login_data["remember"] = False

        if idx == 1:
            database = self.database.text()
            password = self.password.text()
            username = self.username.text()
            self.login_data["database"] = database
            self.login_data["password"] = password
            self.login_data["username"] = username
            if "" in [url,database, password, username]:
                return
        else:
            api_key = self.api_key.text()
            self.login_data["api_key"] = api_key
            if "" in [url,api_key]:
                return
        self.main_window.set_login_data(self.login_data)
        
        self.connecting()

    def accept_action(self):
        self.get_contacts()

    def select_api_type(self, idx):
        if idx == 1:
            self.database.setVisible(not self.is_connected)
            self.database_label.setVisible(not self.is_connected)
            self.password.setVisible(not self.is_connected)
            self.password_label.setVisible(not self.is_connected)
            self.username.setVisible(not self.is_connected)
            self.username_label.setVisible(not self.is_connected)
            self.api_key.setVisible(False)
            self.api_key_label.setVisible(False)
        else:
            self.database.setVisible(False)
            self.database_label.setVisible(False)
            self.password.setVisible(False)
            self.password_label.setVisible(False)
            self.username.setVisible(False)
            self.username_label.setVisible(False)
            self.api_key_label.setVisible(not self.is_connected)
            self.api_key.setVisible(not self.is_connected)


    def connecting(self):
        self._progress_bar.set_progress(0)
        self._progress_bar.setVisible(True)
        try:
            self.connect_info.setText("Connecting API...")
            self.connecting_thread = progress_bar_view.ConnectThread(jsonrpc_client.get_tags,url = self.url.text(),api_key=self.api_key.text())

            self.connecting_thread.connect_finished.connect(self.connect_finished)
            self.connecting_thread.start()
            return True    
        except Exception as e:
            self.connect_info.setText("Connecting Failed,check your internet connection!")
            print("error download",e)
        return False

    def get_contacts(self):
        self._progress_bar.setVisible(True)
        tag = self.get_current_tag()
        phone_col = self.get_phone_col()
        try:
            self.get_contacts_thread = progress_bar_view.ConnectThread(jsonrpc_client.get_contacts,url = self.url.text(),api_key=self.api_key.text(),tag=tag, phone_col=phone_col)

            self.get_contacts_thread.connect_finished.connect(self.get_contacts_finished)
            self.get_contacts_thread.start()
            return True    
        except Exception as e:
            self.connect_info.setText("Connecting Failed,check your internet connection!")
            print("error download",e)
        return False

    def get_current_tag(self):
        if self.contacts_tags:
            return self.contacts_tags[self.tags_options.currentIndex()]
        return None

    def get_phone_col(self):
        if self.field_options.currentIndex() == 1:
            return "mobile"
        return "phone"

    def get_contacts_finished(self, data):
        print("get contacts finished")
        status,contacts = data
        self._progress_bar.set_progress(100)
        self._progress_bar.setVisible(False)
        self._progress_bar.set_progress(0)
        if status:
            print("import contact from main window")
            print(contacts)
            contacts_df = pd.DataFrame(contacts)
            columns = ["name","company","position", self.get_phone_col()]
            contacts_df = contacts_df.reindex(columns, axis=1)
            status = self.main_window.load_contacts_df(contacts_df)
            if status:
                self.accept()
                return
        

    def connect_finished(self, data):
        print("connect finished")
        status,contacts_tags = data
        self.is_connected = status
        self.contacts_tags = contacts_tags
        if contacts_tags:
            self._progress_bar.set_progress(100)
            self._progress_bar.setVisible(False)
            self.connect_info.setText("Connected")
            self.tags_options.clear()
            self.tags_options.addItems(self.contacts_tags)
        else:
            self.connect_info.setText("Connecting Failed,check your internet connection!")
            self._progress_bar.setVisible(False)
            self.connect_info.setVisible(True)
        self._progress_bar.set_progress(0)

        self.tags_group.setVisible(self.is_connected)
        if self.is_connected:
            self.connect_button.setText("Disconnect")

        else:
            self.connect_button.setText("Connect API")
        self.api_options.setEnabled(not self.is_connected)
        self.url.setVisible(not self.is_connected)
        self.remember.setVisible(not self.is_connected)
        self.database.setVisible(not self.is_connected)
        self.username.setVisible(not self.is_connected)
        self.password.setVisible(not self.is_connected)
        self.api_key.setVisible(not self.is_connected)
        self.url_label.setVisible(not self.is_connected)
        self.database_label.setVisible(not self.is_connected)
        self.username_label.setVisible(not self.is_connected)
        self.password_label.setVisible(not self.is_connected)
        self.api_key_label.setVisible(not self.is_connected)
        self.connect_info_label.setVisible(self.is_connected)
        self.connect_info.setVisible(self.is_connected)
        self.import_button.setEnabled(self.is_connected)
        self.select_api_type(self.api_options.currentIndex())
        self.import_button.setEnabled(True)
        self.connect_button.setEnabled(True)

class DownloaderDialog(QDialog):
    
    def __init__(self ,icon=None, parent=None):
        super(DownloaderDialog, self).__init__(parent)
        self.setFixedWidth(400)
        self._url = ""
        self.filename = ""
        self.destination = ""
        self.setWindowTitle("Download Chrome Webdriver")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        else:
            url = "https://raw.githubusercontent.com/aladeveloper/aladeveloper.github.io/master/assets/img/icons/favicon-64x64.png"   
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.setWindowIcon(QIcon(pixmap))

        self._layout = QVBoxLayout(self)
        self._desc = QLabel("Anda harus mendownload webdriver dulu")
        self._desc.setAlignment(Qt.AlignCenter)
        self._label = QLabel("")
        self._progress_bar = progress_bar_view.ProgressBar()
        self._progress_bar.setVisible(False)
        self._buttons_box = QDialogButtonBox()
        
        self.update_button = QPushButton(self.tr("&Download"))
        self.update_button.setAutoDefault(True)
        self.close_button = QPushButton(self.tr("&Close"))
        self.close_button.setAutoDefault(False)

        self.update_button.clicked.connect(self.download)
        self.close_button.clicked.connect(self.close)

        self.close_button.setEnabled(False)

        self._layout.addWidget(self._desc)
        self._layout.addWidget(self._progress_bar)
        self._layout.addWidget(self._label)
        self._buttons_box.addButton(self.update_button, QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.close_button, QDialogButtonBox.ActionRole)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

    def get_platform(self):
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'linux'
        elif sys.platform == 'darwin':
            platform = 'mac'
        elif sys.platform.startswith('win'):
            platform = 'win'
        else:
            raise RuntimeError('Could not determine chromedriver download URL for this platform.')
        return platform

    def on_update(self, index,chunk,size):
        percent = 100 * index * chunk // size
        
        self._progress_bar.set_progress(percent)

    def set_url(self, url):
        self._url = url

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def download_finished(self, filename):
        self.set_filename(filename)
        if filename:
            self._progress_bar.set_progress(100)
            self._progress_bar.setVisible(False)
            self._desc.setText("Download Webdriver Selesai")
            self._label.setVisible(False)
            self._desc.setAlignment(Qt.AlignCenter)
            self.close_button.setText("Continue Send")
            self.update_button.setVisible(False)

        else:
            print("filename not found")
            self._label.setText("Download Failed,check your internet connection!")
        self.close_button.setEnabled(True)
        self.update_button.setEnabled(True)


    def download(self):
        self._progress_bar.setVisible(True)
        self.close_button.setEnabled(False)
        self.update_button.setEnabled(False)
        try:
            self._label.setText("Mendownload Webdriver...")
            self.download_thread = progress_bar_view.DownloadThread(chromedriver_autoinstaller.install, handler=self.on_update)

            # chrome_path = chromedriver_autoinstaller.install(handler=self.on_update)
            self.download_thread.download_finished.connect(self.download_finished)
            # self._progress_bar.set_progress(100)
            # self._label.setText("Download Webdriver completed")
            self.download_thread.start()
            
        except Exception as e:
            self._label.setText("Download Failed,check your internet connection!")
            print("error download",e)
            self.close_button.setEnabled(True)
            self.update_button.setEnabled(True)
        

def show_dialog(message='This is notification dialog',icon=None):
    dialog = NotifDialog(message, icon)
    if dialog.exec_():
        return True
    return False

def show_about_dialog(app_name, version, wa_version, copyright, icon=None):
    dialog = AboutDialog(app_name, version, wa_version, copyright, icon)
    dialog.exec_()

def show_resend_dialog(message='', icon=None):
    dialog = ResendDialog(message, icon)
    if dialog.exec_():
        return (True, dialog.getResendMode()) # or all
    return (False,None)

def show_new_dialog(message='', icon=None):
    dialog = NewDialog(message, icon)
    if dialog.exec_():
        return dialog.getSaveMode()
    return False

def show_download_dialog(icon=None):
    dialog = DownloaderDialog(icon)
    if dialog.exec_():
        return dialog.get_filename()
    return dialog.get_filename()

def show_API_dialog(main_window,icon=None):
    
    dialog = ConnectOdooAPIDialog(main_window,icon)
    if dialog.exec_():
        return True
    return False



