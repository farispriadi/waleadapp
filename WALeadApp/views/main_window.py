import chromedriver_autoinstaller
import updater
import copy
import sys
import pathlib
import time
import pandas as pd
import math
import numpy as np
from os.path import basename
import subprocess
import yaml
from zipfile import ZipFile

from PySide2.QtWidgets import QMainWindow, QApplication, QToolBar, \
                            QAction, QFileDialog, QCompleter
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import Qt, QStringListModel

# from PySide2.QtGui import 
from WALeadApp.views import main_ui
from WALeadApp.views.progress_bar_view import SendingBar, CollectingBar, \
                            FunctionThread, LoginThread
from WALeadApp.views.dialog_view import show_dialog, show_about_dialog, show_resend_dialog, \
                                show_new_dialog, show_download_dialog, show_API_dialog
from WALeadApp.views.icons_rc import *
from config import ABOUT
from WALeadApp.models.waleadapp import send_message, login, compose_message, collect_response, \
                            check_chrome_version, get_major_version, get_browser
from WALeadApp.views.summary_window import SummaryWindow
from WALeadApp.views.action_view import SendAction, StopAction
# from WALeadApp.secret import secret

MAIN_LOGO = ":icon/logo"

def progress_download(index,chunk,size):
    percent = 100* index * chunk // size

def convert_ID(mobile_number):
    """ Covert valid mobile to ID phone code"""
    number_str = ''.join(filter(str.isdigit, str(mobile_number)))
    if number_str[:2]=='08':
        number_str = '62'+number_str[1:]
    elif number_str[:1] == '8' :
        number_str = '62'+number_str[0:]
    return number_str

class MainWindow(QMainWindow):

    def __init__(self, contact_path = None):
        super(MainWindow, self).__init__()
        self.ui = main_ui.Ui_MainWindow()
        self.current_worker = None
        self.workers = []
        self.workers2 = []
        self.results = []
        self.collect_results = []
        self.attachments = []
        self._current_file = ''
        self.is_dirty = False
        self._stop = False
        self._collect = False
        self._resend_failed = (True, 'all')
        self.login_data = {}
        
        if contact_path:
            self.contact_df = self.load_contacts(contact_path)
            self.ui.createContactsModel(self.contact_df)
        else:
            self.contact_df = pd.DataFrame()

        self.ui.setupUi(self)

        self._create_actions()
        self._create_menubars()
        self._create_toolbars()        
        self.setWindowTitle("WALeadApp "+ABOUT['version'])
        self.ui.progressBar.setVisible(False)
        self.ui.progressBarLabel.setVisible(True)
        self.ui.emojiView.mouse_released.connect(self.add_emoji)
        self.ui.templateEdit.textChanged.connect(self.edit_message)
        self.ui.templateEdit.setFocus()
        self.ui.contactsTable.dragged.connect(self.show_empty_table)
        self.ui.contactsTable.fileDropped.connect(self.load_contacts_drop)
        self.ui.emptyTable.dropped.connect(self.show_contacts_table)
        self.ui.emptyTable.fileDropped.connect(self.load_contacts_drop)
        self.ui.emptyTable.draggedLeave.connect(self.show_contacts_table)
        self.ui.attachmentsTree.fileDropped.connect(self.load_attachments_drop)
        self.setWindowIcon(QIcon(MAIN_LOGO))
        self.showMaximized()

        self.get_init_secret()

    def update_completer(self):
        header_data = list(self.ui.contactsTable.tableModel.header_data)
        if header_data:
            completer = QCompleter(self.ui.centralwidget)

            completer_model = QStringListModel(header_data)
            completer.setModel(completer_model)
            completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setWrapAround(False)
            self.ui.templateEdit.setCompleter(completer)

    def get_init_secret(self):
        # secret.secret()
        # try:
        #     print("Hai")
        #     api_url = secret.query('url_api','select')
        #     print("url_api", api_url)
        #     if api_url:
        #         api_key = secret.query(api_url,'select')
        #         print("api_key", api_key)
        #         if api_key:
        #             self.login_data["url"] = api_url
        #             self.login_data["api_key"] = api_key
        #             self.login_data["remember"] = True
        #     print("self.login_data", self.login_data)
        # except:
        #     self.login_data = {}

        self.login_data = {}

    def set_login_data(self, login_data):
        self.login_data = login_data
        # secret.secret()
        key = self.login_data["url"]
        # check =secret.check(key)
        # if check:
        #     secret.query(key,'update',self.login_data["api_key"])
        # else:
        #     secret.query('url_api','set',key)
        #     secret.query(key,'set',self.login_data["api_key"])


    def show_connect_odoo_api(self):
        show_API_dialog(self)

    def show_empty_table(self, is_empty):
        if is_empty:
            self.ui.contactsTable.hide()
            self.ui.emptyTable.show()

    def show_contacts_table(self, is_dropped_or_draggedLeave):
        if is_dropped_or_draggedLeave:
            self.ui.emptyTable.hide()
            self.ui.contactsTable.show()

    def close_thread(self):
        try:
            self.current_worker.quit()
        except Exception as e:
            print("Exception QThread ", e)

    def update_window_title(self,is_dirty=True):
        signed = ""
        self.is_dirty = is_dirty
        if is_dirty:
            # if dirty
            signed = "*"
        if self._current_file:
            filename_str = signed+str(pathlib.Path(self._current_file).name)
            self.setWindowTitle(" - ".join([filename_str,ABOUT["app_name"]+" "+ABOUT['version']]))
        else:
            self.setWindowTitle(" - ".join([signed+"Untitled",ABOUT["app_name"]+" "+ABOUT['version']]))


    def new_gui(self, PROJECT_PATH):
        save_before =False
        if self.is_dirty:
            save_before = show_new_dialog("Apakah Anda akan menyimpan project?")
            if save_before:
                if self._current_file:
                    save_before = self.save_project_gui(PROJECT_PATH, replace=True)
                else:
                    save_before = self.save_project_gui(PROJECT_PATH, replace=False)
                save_before = not save_before

        if not save_before:
            self._current_file = ''
            self.ui.projectName.setText("Untitled")
            self._current_file=""
            self.update_window_title(is_dirty=False)
            self._collect = False
            self._stop = False
            self.ui.progressBar.setVisible(False)
            self.ui.templateEdit.clear()
            contact_df = pd.DataFrame()
            self.contact_df = contact_df
            self.ui.contactsTable.reset_model()
            self.send_action.setEnabled(False)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(False)
            except:
                pass
            attachment_count = len(self.attachments)
            if attachment_count >1:
                for attach in list(range(attachment_count)).reverse():
                    self.ui.attachmentsTree.removeFile(attach)
            else:
                self.ui.attachmentsTree.removeFile(0)

    def show_about(self):
        show_about_dialog(ABOUT['app_name'], 'Version '+ABOUT['version'], 'WhatsApp '+ABOUT['whatsapp'], 'Copyright © '+ABOUT['year']+' '+ABOUT['author'], icon=MAIN_LOGO)

    def show_summary(self):
        if hasattr(self.ui.contactsTable,'tableModel'):
            self.contact_df = self.ui.contactsTable.tableModel.getContacts()
        else:
            show_dialog(message="Belum Ada Ringkasan Laporan",icon=MAIN_LOGO)
            return

        if self.contact_df.empty:
            show_dialog(message="Belum Ada Ringkasan Laporan",icon=MAIN_LOGO)
        else:
            self.summary_window = SummaryWindow(data_df=self.contact_df, icon=QIcon(MAIN_LOGO), main_window=self)
            self.summary_window.show()

    def show_resend_options(self):
        self._resend_failed = show_resend_dialog(message="Kirim pesan yang TIDAK/BELUM TERKIRIM?", icon=MAIN_LOGO)


    def load_contacts(self, file_path=None, dataframe=pd.DataFrame(), refine=True, column=None):
        """
        load from csv or excel 
        force refine mobile to ID

        return
        ------
        DataFrame object
        """        
        if not dataframe.empty:
            contact_df = dataframe
        else:
            try:
                path = pathlib.Path(file_path).suffix
                if path == ".csv":
                    contact_df = pd.read_csv(file_path, dtype=str)
                else: #if excel
                    contact_df = pd.read_excel(file_path, engine="openpyxl", dtype=str)
                    is_NaN = contact_df.isnull()
                    row_all_NaN = is_NaN.all(axis=1)
                    contact_df = contact_df[~row_all_NaN]

            except:
                contact_df = pd.DataFrame()
            
        if refine and not contact_df.empty:
            if column is not None:
                contact_df[column] = contact_df[column].apply(convert_ID)
            elif "phone" in contact_df.columns:
                contact_df["phone"] = contact_df["phone"].apply(convert_ID)
            else:    
                contact_df["mobile"] = contact_df["mobile"].apply(convert_ID)
            

            new_columns = [
                    'status', 
                    'attachment_status',
                    'saved_name',
                    'token',
                    'sent_date',
                    'replied',
                    'responses']
            if not set(contact_df.columns.tolist()).intersection(set(new_columns)):
                contact_df = self.add_contacts_columns(contact_df,new_columns)

            contact_df = contact_df.sort_values(by=[contact_df.columns[0]], ascending=[True])
            contact_df = contact_df.reset_index(drop=True)
            

        print("contact_df", contact_df)
        
        return contact_df

    def save_contacts(self, file_path=None, sortby=[-1,Qt.AscendingOrder]):
        """
        save to csv

        return
        ------
        DataFrame object
        """
        #update contacts df from current contacts table
        self.contact_df = self.ui.contactsTable.tableModel.getContacts()

        contact_df = self.ui.contactsTable.tableModel.displayed_contact_df.copy()
        column_name = contact_df.columns[sortby[0]]
        try:
            # sort by column name
            if sortby[1] == Qt.AscendingOrder:
                contact_df = contact_df.sort_values(by=[column_name], ascending=[True])
                contact_df = contact_df.reset_index(drop=True)
            else:
                contact_df = contact_df.sort_values(by=[column_name], ascending=[True])
                contact_df = contact_df.reset_index(drop=True)
        except Exception as e:
            print("No Sorting ", e)

        try:
            new_columns = [col.replace(" ","_") for col in contact_df.columns]
            contact_df.columns = new_columns
            if not file_path.endswith(".csv"):
                file_path = file_path+".csv"
            contact_df.to_csv(file_path)
        except Exception as e:
            print("error save contacts :", e)

    def load_project(self, file_path=None):
        if file_path:
            with open(file_path, 'r') as f:
                yaml_dict = yaml.load(f)

                self.ui.projectName.setText(yaml_dict['project'])
                self.ui.templateEdit.setPlainText(yaml_dict['template'])
                df = pd.read_json(yaml_dict['contacts'])
                df = df.sort_values(by=[df.columns[0]], ascending=[True])
                df = df.reset_index(drop=True)
                # implementasi fillna -- >"" 
                df.fillna('', inplace=True)
                self.contact_df = df
                self.results = self.contact_df.to_dict('records')
                self.ui.createContactsModel(self.contact_df)
                self.ui.contactsTable.update_model(self.ui.contact_model)
                if 'collect' in yaml_dict.keys():
                    self._collect = yaml_dict['collect']

                self.send_action.setEnabled(True)
                try:
                    self.ui.sendButton.setVisible(True)
                    self.ui.sendButton.setEnabled(True)
                except:
                    pass
                self.collect_action.setEnabled(self._collect)
                old_attachmets_count = len(self.ui.attachmentsTree.filenames)
                list_idx = list(range(old_attachmets_count))
                if list_idx :
                    if old_attachmets_count >=2:
                        for idx in list_idx.reverse():
                            self.ui.attachmentsTree.removeFile(idx)
                    else:
                        self.ui.attachmentsTree.removeFile(0)
                self.attachments = []
                self.ui.addAttach.setEnabled(True)
                attachments = yaml_dict['attachments']

                try:
                    # unzip attachments
                    if file_path.endswith("yaml"):
                        file_zip =file_path.replace(".yaml","_attachments.zip")
                    elif file_path.endswith("yml"):
                        file_zip =file_path.replace(".yml","_attachments.zip")
                    else:
                        file_zip =file_path+"_attachments.zip"

                    with ZipFile(file_zip, 'r') as zip_obj:
                       # zip_obj.extractall(path="/".join(file_zip.split("/")[:-1]))
                       file_zip_path = pathlib.Path(file_zip)
                       zip_obj.extractall(path=str(file_zip_path.parent))

                except Exception as e:
                    print("Error unzipping Attachments")

                for attachment in attachments:
                    # check path is exist 
                    file_attach = pathlib.Path(attachment)
                    if file_attach.exists ():
                        self.ui.attachmentsTree.addFile(attachment)
                        self.attachments.append(attachment)
                        print ("File exist")
                    else:
                        print ("File not exist")
                        print("try to local similar files")
                        file_name  = file_attach.name
                        new_attachment  = pathlib.Path(file_path).parent.joinpath(file_name) 
                        if not new_attachment.exists ():
                            print ("No folder Attachments")
                        else:
                            self.ui.attachmentsTree.addFile(str(new_attachment))
                            self.attachments.append(str(new_attachment))

                if len(self.attachments) >= 1:
                    self.ui.addAttach.setEnabled(False)
            return True
        return False
                    
    def get_attachments(self):
        return self.ui.attachmentsTree.filenames

    def save_project(self, file_path=None):
        #update contacts df from current contacts table
        self.contact_df = self.ui.contactsTable.tableModel.getContacts()

        if file_path:
            # create yaml file
            ## project : str
            ## template : str
            ## contacts : str(json pandas)
            ## attachments : 
                        # - attachments (folder)/image.jpg
                        # - attachments (folder)/doc.pdf
            # ensure file_path contains .yaml or .yml extenstion like in windows
            if not file_path.endswith(".yaml") and not file_path.endswith(".yml"):
                file_path = file_path+".yaml"

            if file_path.endswith(".yml"):
                file_zip = file_path[:-4]+"_attachments.zip"
            elif file_path.endswith(".yaml"):
                file_zip = file_path[:-5]+"_attachments.zip"
            else:
                file_zip = file_path+"_attachments.zip"
            project = self.ui.projectName.text()
            template = self.ui.templateEdit.toPlainText()
            contacts_json = self.contact_df.to_json(orient='records')
            attachments = self.attachments
            yaml_dict = {'app': 'WALeadApp',
                            'version':1.0,
                            'project': project,
                            'template': template,
                            'contacts': contacts_json,
                            'attachments': attachments,
                            'collect': self._collect,
                        }
            with open(file_path, 'w') as f:
                documents = yaml.dump(yaml_dict, f)

            try:
                with ZipFile(file_zip, 'w') as zip_obj:
                    # Add multiple files to the zip
                    for attachment in self.attachments:
                        zip_obj.write(attachment, basename(attachment))
            except Exception as e:
                print("Error Zipping Attachments :", e)
            self._current_file = file_path 
            return True            
        return False


    def add_contacts_columns(self, contact_df, new_columns=[]):
        for new_col in new_columns:
            contact_df[new_col] = ['']*len(contact_df.index)
        return contact_df

    def load_contacts_df(self, contact_df):
        contact_df = self.load_contacts(dataframe=contact_df)
        if not contact_df.empty:
            self.ui.createContactsModel(contact_df)
            self.contact_df = contact_df
            self.ui.contactsTable.update_model(self.ui.contact_model)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            message = "Contacts added successfully "
            self.ui.statusbar.showMessage(message, timeout=1000)
            self.update_window_title(is_dirty=True)
            self.update_completer()
            self._collect = False
            self._stop = False
            self.ui.progressBar.setVisible(False)
            return True

        message = "No contacts added"
        self.ui.statusbar.showMessage(message, timeout=1000)
        return False

    def load_contacts_drop(self, filename):
        if filename:
            contact_df = self.load_contacts(filename)
            self.ui.createContactsModel(contact_df)
            self.contact_df = contact_df
            self.ui.contactsTable.update_model(self.ui.contact_model)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            message = "Contacts added successfully "
            self.ui.statusbar.showMessage(message, timeout=1000)
            self.update_window_title(is_dirty=True)
            self.update_completer()
            self._collect = False
            self._stop = False
            self.ui.progressBar.setVisible(False)
            return True

        message = "No contacts added"
        self.ui.statusbar.showMessage(message, timeout=1000)
        return False

    def load_contacts_gui(self, PROJECT_PATH):
        filename = QFileDialog.getOpenFileName(self,"Load Contacts",PROJECT_PATH,"Excel or CSV files (*.xlsx *.xls *.csv)")
        if filename[0]:
            contact_df = self.load_contacts(filename[0])            
            self.ui.createContactsModel(contact_df)
            self.contact_df = contact_df
            self.ui.contactsTable.update_model(self.ui.contact_model)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            message = "Contacts added successfully "
            self.ui.statusbar.showMessage(message, timeout=1000)
            self.update_window_title(is_dirty=True)
            self.update_completer()
            self._collect = False
            self._stop = False
            self.ui.progressBar.setVisible(False)
            return True

        message = "No contacts added"
        self.ui.statusbar.showMessage(message, timeout=1000)
        return False

    def load_project_gui(self, PROJECT_PATH):
        message = ""
        try:
            filename = QFileDialog.getOpenFileName(self,"Load Project",PROJECT_PATH,"YAML (*.yaml *.yml)")
            if filename[0]:
                is_success= self.load_project(filename[0])

                if is_success:
                    message = "Project has been opened"
                    self._current_file = filename[0]
                    self.update_window_title(is_dirty=False)
                    self.update_completer()
                    self._collect = False
                    status_col = self.contact_df["status"].tolist()
                    status=list(set(status_col).intersection(set(['Sent','Failed'])))
                    if status:
                        self._collect = True
                    self._stop = False
                    self.ui.progressBar.setVisible(False)
                else:
                    message = "Failed open project"
        except:
            message = "Error open project"

        self.ui.statusbar.showMessage(message, timeout=1000)

    def save_project_gui(self, PROJECT_PATH, replace=False):
        message = ""
        try:
            if replace and self._current_file:
                if self._current_file.endswith(".yml"):
                    _current_file = self._current_file[:-4]
                else: #.yaml
                    _current_file = self._current_file[:-5]
                filename = [_current_file,None ]
            else:
                filename = QFileDialog.getSaveFileName(self,"Save Project",PROJECT_PATH,"YAML file (*.yaml *.yml)")
            is_success = self.save_project(filename[0])
            if is_success:
                message = "Project has been saved"
                self.update_window_title(is_dirty=False)
            else:
                message = "Failed  saving project"    
        except:
            message = "Error saving project"
        
        self.ui.statusbar.showMessage(message, timeout=1000)
        

    def save_contacts_gui(self, PROJECT_PATH):
        filename = QFileDialog.getSaveFileName(self,"Export Contacts Report",PROJECT_PATH,"CSV file (*.csv)")
        column_idx = self.ui.contactsTable.horizontalHeader().sortIndicatorSection()
        order = self.ui.contactsTable.horizontalHeader().sortIndicatorOrder()
        self.save_contacts(filename[0], sortby=[column_idx,order])

    def update_contacts_report(self, row_int, col_names, values):
        # force column mobile to phone while no mobile column 
        if "phone" in list(self.contact_df.columns) and "mobile" in col_names:
            col_names[col_names.index("mobile")]= "phone"

        for col_name,value in zip(col_names, values):
            self.contact_df.at[row_int, col_name] = value
        self.contact_df.fillna('', inplace=True)
        self.ui.createContactsModel(self.contact_df)
        self.ui.contactsTable.update_model(self.ui.contact_model)


    def load_attachments_gui(self, PROJECT_PATH):
        try:
            filename = QFileDialog.getOpenFileName(self,"Load Attachments",PROJECT_PATH)
            if filename[0]:
                self.attachments.append(filename[0])
                row_count = self.ui.attachmentsTree.addFile(filename[0])
                if row_count >= 1:
                    self.ui.addAttach.setEnabled(False)
                message = "Attachments added successfully "
                self.update_window_title(is_dirty=True)
                self.ui.statusbar.showMessage(message, timeout=1000)
        except:
            message = "Error adding attachment"
            self.ui.statusbar.showMessage(message, timeout=1000)

    def load_attachments_drop(self, filename):
        message = "No attachments added"
        if filename:
            self.attachments.append(filename)
            row_count = self.ui.attachmentsTree.root_node.rowCount()
            if row_count >= 1:
                self.ui.addAttach.setEnabled(False)
                message = "Attachments added successfully "
                self.update_window_title(is_dirty=True)
                self.ui.statusbar.showMessage(message, timeout=1000)
                return True
        self.ui.statusbar.showMessage(message, timeout=1000)
        return False


    def remove_attachment(self):
        try:
            self.ui.attachmentsTree.removeFile()
            self.attachments = self.ui.attachmentsTree.getFileNames()
            row_count = self.ui.attachmentsTree.getRowCount()
            if row_count < 3:
                self.ui.addAttach.setEnabled(True)
            message = "Attachment removed successfully "
            self.update_window_title(is_dirty=True)
            self.ui.statusbar.showMessage(message, timeout=1000)
        except:
            message = "Error removing attachment"
            self.ui.statusbar.showMessage(message, timeout=1000)

    def add_contacts(self):
        if not hasattr(self.ui.contactsTable,'tableModel'):
            contact_df = pd.DataFrame({'name':['Sample Name'],
                                        'phone': ['628123']
                                    })
            
            if "phone" in contact_df.columns:
                contact_df["phone"] = contact_df["phone"].apply(convert_ID)
            else:    
                contact_df["mobile"] = contact_df["mobile"].apply(convert_ID)
            

            new_columns = [
                    'status', 
                    'attachment_status',
                    'saved_name',
                    'token',
                    'sent_date',
                    'replied',
                    'responses']
            contact_df = self.add_contacts_columns(contact_df,new_columns)

            contact_df = contact_df.sort_values(by=[contact_df.columns[0]], ascending=[True])
            contact_df = contact_df.reset_index(drop=True)
            self.ui.createContactsModel(contact_df)
            self.contact_df = contact_df
            self.ui.contactsTable.update_model(self.ui.contact_model)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            message = "Contacts added successfully "
            self.ui.statusbar.showMessage(message, timeout=1000)
            self.update_window_title(is_dirty=True)
            self.update_completer()
            self._collect = False
            self._stop = False
            self.ui.progressBar.setVisible(False)
        else:
            self.ui.contactsTable.addRow()
            self.update_window_title(is_dirty=True)

    def remove_contacts(self):
        self.ui.contactsTable.removeRow()
        self.contact_df = self.ui.contactsTable.tableModel.getContacts()       

    def edit_message(self):
        self.update_window_title(is_dirty=True)

    def add_emoji(self, emoji_unicode):
        self.ui.templateEdit.insertPlainText(emoji_unicode)
        self.ui.templateEdit.setFocus()
        self.ui.templateEdit.verticalScrollBar().setValue(self.ui.templateEdit.verticalScrollBar().maximum())
        # self.update_window_title(is_dirty=True)

    def check_updates(self, PROJECT_PATH):
        print("Check updates")
        sending_status = True
        if self.is_dirty:
            save_before = show_new_dialog("Apakah Anda akan menyimpan project sebelum update?")
            if save_before:
                if self._current_file:
                    save_before = self.save_project_gui(PROJECT_PATH, replace=True)
                else:
                    save_before = self.save_project_gui(PROJECT_PATH, replace=False)
        try:
            if updater.check_updates():
                update_status = updater.show_updater()
                sending_status = update_status
                if update_status:
                    accepted = show_dialog(message="Silakan Tutup WALeadApp setelah Update", icon=MAIN_LOGO)
                    if accepted:
                        self.close()
                        return
        except:
            raise
            sending_status = False
        if not sending_status:
            show_dialog(message="Check Updates Failed", icon=MAIN_LOGO)
            return


    def send(self):
        
        #update contacts df from current contacts table
        self.contact_df = self.ui.contactsTable.tableModel.getContacts()
        # self.attachments = self.get_attachments()
        print("attachments",self.attachments)

        try:
            status, chrome_path = chromedriver_autoinstaller.webdriver_exist()
            if not status:
                chrome_path = show_download_dialog()
            
            print("Your Chrome path :", chrome_path)
            if not chrome_path:
                show_dialog(message="Download Failed", icon=MAIN_LOGO)
                return
        except Exception as e:
            err_msg = str(e)
            show_dialog(message="Periksa koneksi internet Anda{} ".format(e), icon=MAIN_LOGO)
            return
        
        message = self.ui.templateEdit.toPlainText()
        message.replace(" ","")
        message.replace("\n","")
        message.replace("\t ","")
        if self.contact_df.empty:
            show_dialog(message="Anda belum mengimppor data kontak excel atau csv.", icon=MAIN_LOGO)
            return
        else:
            if "phone" in self.contact_df.columns:
                if self.contact_df["phone"].isna().all():
                    show_dialog(message="Anda belum mengisi data kontak.", icon=MAIN_LOGO)
                    return       
            elif "mobile" in self.contact_df.columns:
                if self.contact_df["mobile"].isna().all():
                    show_dialog(message="Anda belum mengisi data kontak.", icon=MAIN_LOGO)
                    return       

        if len(message) == 0:
            show_dialog(message="Anda melupakan template pesannya.", icon=MAIN_LOGO)
            return
        if self._collect or self._stop:
            self.show_resend_options()
            if not self._resend_failed[0]:
                return
            self.ui.progressBar.setVisible(False)
            self.ui.progressBarLabel.setVisible(False)

        self.stop_action.setEnabled(True)
        try:
            self.ui.stopButton.setVisible(True)
        except:
            pass
        self.send_action.setEnabled(False)
        try:
            self.ui.sendButton.setVisible(False)
            self.ui.sendButton.setEnabled(False)
        except:
            pass
        self.collect_action.setEnabled(False)

        
        try:
            self.send_action.setEnabled(False)
            try:
                self.ui.sendButton.setVisible(False)
                self.ui.sendButton.setEnabled(False)
            except:
                pass
            
            if not self.contact_df.empty:
                phone_column='mobile'
                if 'phone' in self.contact_df.columns:
                    phone_column = 'phone'

                if phone_column in self.contact_df.columns:
                    self.results = []
                    self.workers = []

                    
                    if hasattr(self.ui, "progressBar"):
                        self.ui.progressLayout.removeWidget(self.ui.progressBar)
                        self.ui.progressBar.deleteLater()
                        self.ui.progressBar = SendingBar(self.ui.contactsWidgetContents)
                        self.ui.progressLayout.addWidget(self.ui.progressBar)
                    
                    self.ui.progressBarLabel.setText("Opening Web WhatsApp In Chrome Browser ...")
                    self.ui.progressBar.set_progress(0)
                    self.ui.progressBar.setVisible(True)
                    self.ui.progressBarLabel.setVisible(True)
                    func_obj = send_message

                    if self._resend_failed[1] == 'failed':
                        contacts_series = self.contact_df[self.contact_df['status'] != 'Sent'][phone_column]
                    else:
                        contacts_series = self.contact_df[phone_column]

                    template_message = self.ui.templateEdit.toPlainText()
                    ending_sleep = int(math.ceil(len(template_message)/ 30))
                    messages = compose_message(template_message, self.contact_df)

                    if not self._stop:
                        self.login_worker = LoginThread(login)
                        self.login_worker.login_finished.connect(self.login_finished)
                    for idx, mobile in contacts_series.items():
                        worker= FunctionThread(func_obj, ending_sleep, mobile=mobile, message=messages[idx], attachments=self.attachments, is_caption_text=True, row=idx)
                        worker.progress_started.connect(self.send_started)
                        worker.progress_finished.connect(self.send_finished)
                        worker.progress_error.connect(self.send_error)
                        self.workers.append(worker)

                    if self._stop:
                        self._stop = False
                    self.login_worker.start()
                    self.ui.progressBarLabel.setText("Login to Web WhatsApp ...")
                    self.interval = round(100/(len(self.workers)+1),2)
        except Exception as e:
            print("error send action",e )
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass

    def login_finished(self, status):
        print("Login status", status)
        self.ui.progressBar.set_progress(self.interval)        
        if status:
            self.iter_workers = iter(self.workers)
            self.current_worker = next(self.iter_workers)
            self.current_worker.start()
    def send_started(self, text):
        print("Sending to", text)
        self.ui.progressBarLabel.setText("Sending to {} ...".format(text))

    def send_finished(self, result):
        print("result ", result)

        self.results.append(result)
        try:
            index_worker = self.workers.index(self.current_worker)
        except ValueError:
            return

        if self._stop:
            self.ui.progressBar.set_stop()
            return

        if index_worker == len(self.workers)-1:
            self.ui.progressBar.set_progress(100)
            self.ui.progressBarLabel.setText("Sending Complete.")
            self.ui.progressBarLabel.setVisible(False)
            self.ui.progressBar.setVisible(False)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setVisible(True)
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            self.stop_action.setEnabled(False)
            try:
                self.ui.stopButton.setVisible(False)
            except:
                pass
            self._collect = True
            self.collect_action.setEnabled(True)
        else:    
            self.ui.progressBar.set_progress((index_worker+2)* self.interval)
        # self.update_contacts_report(index_worker,list(result.keys()), list(result.values()))
        if 'row' in result.keys():
            self.update_contacts_report(result['row'],list(result.keys()), list(result.values()))
        else:
            self.update_contacts_report(index_worker,list(result.keys()), list(result.values()))

        try:
            self.current_worker = next(self.iter_workers)
            self.current_worker.start()
        except:
            pass

        self.update_window_title(is_dirty=True)
        # get_browser().quit()

    def send_error(self, error):
        print("error", error)
        self.update_window_title(is_dirty=True)

    def stop(self):
        # stop mean pause if still progress
        self._stop = True
        self.stop_action.setEnabled(False)
        try:
            self.ui.stopButton.setVisible(False)
        except:
            pass
        self.send_action.setEnabled(not self._collect)
        try:
            self.ui.sendButton.setVisible(True)
            self.ui.sendButton.setEnabled(not self._collect)
        except:
            pass
        self.collect_action.setEnabled(self._collect)
        try:
            self.current_worker.quit()
        except:
            print("exception pausing thread")
        print("Stop successfully")
        self.update_window_title(is_dirty=True)
        get_browser().quit()
        

    def collect(self):
        if not self.contact_df.empty:
            self.stop_action.setEnabled(True)
            try:
                self.ui.stopButton.setVisible(True)
            except:
                pass
            self.send_action.setEnabled(False)
            try:
                self.ui.sendButton.setEnabled(False)
            except:
                pass
            self.collect_action.setEnabled(False)

            self.ui.progressLayout.removeWidget(self.ui.progressBar)
            self.ui.progressBar = CollectingBar(self.ui.contactsWidgetContents)
            self.ui.progressLayout.addWidget(self.ui.progressBar)
            self.ui.progressBar.setVisible(True)

            func_obj = collect_response
            if "phone" in self.contact_df.columns:
                contacts_series = self.contact_df["phone"]
            else:
                contacts_series = self.contact_df["mobile"]
            self.login_worker = LoginThread(login)
            self.login_worker.login_finished.connect(self.login_finished)
            self.workers = []
            ending_sleep = 5
            for row, mobile in contacts_series.items():
                token = ''
                if 'token' in self.results[row].keys():
                    if type(self.results[row]['token']) is dict:
                        if 'data_id' in self.results[row]['token'].keys():
                            token = self.results[row]['token']['data_id']

                worker= FunctionThread(func_obj, ending_sleep, mobile=mobile, token=token ,result=self.results[row])
                worker.progress_started.connect(self.collect_started)
                worker.progress_finished.connect(self.collect_finished)
                worker.progress_error.connect(self.collect_error)
                self.workers.append(worker)
            self.login_worker.start()
            self.interval = 100/len(self.workers)

    def collect_started(self, text):
        print("Collect ")

    def collect_finished(self, result):
        print("result ", result)

        self.collect_results.append(result)
        index_worker = self.workers.index(self.current_worker)        
        if index_worker == len(self.workers)-1:
            self.ui.progressBar.set_progress(100)
            self.ui.progressBar.setVisible(False)
            self.send_action.setEnabled(True)
            try:
                self.ui.sendButton.setEnabled(True)
            except:
                pass
            self.stop_action.setEnabled(False)
            try:
                self.ui.stopButton.setVisible(False)
            except:
                pass
            self.collect_action.setEnabled(True)
        else:    
            self.ui.progressBar.set_progress((index_worker+1)* self.interval)
        self.update_contacts_report(index_worker,['status','replied'], [result['status'], result['replied']])
        try:
            self.current_worker = next(self.iter_workers)
            self.current_worker.start()
        except:
            pass

    def collect_error(self, error):
        print("collect error", error)


    def _create_actions(self):
        self.new_action = QAction(self)
        self.new_action.setText("&New")
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.setIcon(QIcon(":icon/new"))
        self.open_action = QAction(self)
        self.open_action.setText("&Open")
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.setIcon(QIcon(":icon/open"))
        self.saveas_action = QAction(self)
        self.saveas_action.setText("&SaveAs")
        self.save_action = QAction(self)
        self.save_action.setText("&Save")
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setIcon(QIcon(":icon/save"))
        self.import_action = QAction(self)
        self.import_action.setText("&Import Contacts")
        self.import_action.setIcon(QIcon(":icon/import"))

        self.import_api_action = QAction(self)
        self.import_api_action.setText("&Import From Odoo")

        self.export_action = QAction(self)
        self.export_action.setText("&Export Contacts")
        self.quit_action = QAction(self)
        self.quit_action.setText("&Quit")

        self.send_action = SendAction(self)
        self.send_action.setText("&Send")
        self.send_action.setIcon(QIcon(":icon/send"))
        self.send_action.setEnabled(False)
        try:
            self.ui.sendButton.setVisible(True)
            self.ui.sendButton.setEnabled(False)
        except:
            pass
        self.collect_action = QAction(self)
        self.collect_action.setText("&Collect")
        self.collect_action.setVisible(False)
        self.collect_action.setEnabled(False)
        self.stop_action = StopAction(self)
        self.stop_action.setText("&Stop")
        self.stop_action.setIcon(QIcon(":icon/stop"))
        self.stop_action.setEnabled(False)
        try:
            self.ui.stopButton.setVisible(False)
        except:
            pass


        self.summary_action = QAction(self)
        self.summary_action.setText("&Summary")
        self.summary_action.setIcon(QIcon(":icon/summary"))
        # self.summary_action.setVisible(False)

        self.docs_action = QAction(self)
        self.docs_action.setText("&Docs")
        self.about_action = QAction(self)
        self.about_action.setText("&About")
        self.check_updates_action = QAction(self)
        self.check_updates_action.setText("&Check Updates")
        

    def _create_menubars(self):
        self.ui.menuFile.addAction(self.new_action)
        self.ui.menuFile.addAction(self.open_action)
        self.ui.menuFile.addAction(self.save_action)
        self.ui.menuFile.addAction(self.saveas_action)
        self.ui.menuFile.addAction(self.import_action)
        self.ui.menuFile.addAction(self.import_api_action)
        self.ui.menuFile.addAction(self.export_action)
        self.ui.menuFile.addAction(self.quit_action)

        self.ui.menuSend.addAction(self.send_action)
        self.ui.menuSend.addAction(self.collect_action)
        self.ui.menuSend.addAction(self.stop_action)

        self.ui.menuReport.addAction(self.summary_action)
        # self.ui.menuReport.setVisible(False)

        # Show / Hide QDockWidget
        self.ui.menuView.addAction(self.ui.contactsWidget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.attachmentsWidget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.emojiWidget.toggleViewAction())
        self.ui.attachmentsWidget.hide()
        self.ui.emojiWidget.hide()

        self.ui.menuHelp.addAction(self.docs_action)
        self.ui.menuHelp.addAction(self.check_updates_action)
        self.ui.menuHelp.addAction(self.about_action)


    def _create_toolbars(self):
        self.file_toolbar = QToolBar("File", self)
        self.addToolBar(self.file_toolbar)
        self.file_toolbar.addActions([self.new_action, \
                                    self.open_action, \
                                    self.save_action,
                                    self.import_action]
                                    )

        self.send_toolbar = QToolBar("Send", self)
        self.addToolBar(self.send_toolbar)
        self.send_toolbar.addActions([self.send_action, \
                                    self.collect_action, \
                                    self.stop_action]
                                    )

        self.report_toolbar = QToolBar("Report", self)
        self.addToolBar(self.report_toolbar)
        self.report_toolbar.addAction(self.summary_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
