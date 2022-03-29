import os
import sys
import datetime
import subprocess
import urllib
import yaml
import wawebxpath
from PySide2.QtWidgets import QProgressBar, QDialog, QApplication, QVBoxLayout, \
                                QLabel, QDialogButtonBox, QPushButton
from PySide2.QtGui import QIcon, QPixmap                            
from PySide2.QtCore import QThread, Signal, Qt
from urllib import request
from zipfile import ZipFile


def get_platform():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
    elif sys.platform == 'darwin':
        platform = 'mac'
    elif sys.platform.startswith('win'):
        platform = 'win'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform

def check_latest_updates():
    platform = get_platform()
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),"manifest.yaml")

    url = "https://github.com/aladeveloper/waleadapp-updates/raw/main/updates/latest.yaml"
    local_file, headers = request.urlretrieve(url)
    with open(local_file, 'r') as lf:
        latest =yaml.load(lf)
    needs_updates = not os.path.isfile(filename)
    if not needs_updates:
        with open(filename, 'r') as f:
            manifest =yaml.load(f)
        release = manifest["released"]
        release_date = str(manifest["released"])
        release_date = datetime.datetime.strptime(release_date,'%Y.%m.%d')

        latest_date = str(latest["date"])
        latest_date = datetime.datetime.strptime(latest_date,'%Y-%m-%d')

        needs_updates = latest_date > release_date
    if needs_updates:
        return latest["release"]
    return None


class ProgressBar(QProgressBar):
    """docstring for ProgressBar"""
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent=None)
        self.setFormat(str(self.value())+"%")

    def set_progress(self,progress):
        self.setValue(progress)
        self.setFormat(str(progress)+"%")

class UpdaterDialog(QDialog):
    def __init__(self ,icon=None, parent=None):
        super(UpdaterDialog, self).__init__(parent)
        self.setFixedWidth(600)
        self._url = ""
        self.filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),"manifest.yaml")
        self.filename_zip = ""
        self.setWindowTitle("Update WALeadApp")
        if icon is not None:
            self.setWindowIcon(QIcon(icon))
        else:
            url = "https://raw.githubusercontent.com/aladeveloper/aladeveloper.github.io/master/assets/img/icons/favicon-64x64.png"   
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.setWindowIcon(QIcon(pixmap))

        self._layout = QVBoxLayout(self)
        self._label = QLabel("WALeadApp perlu Update.")
        self._label.setAlignment(Qt.AlignCenter)
        self._label_desc = QLabel("")
        self._progress_bar = ProgressBar()
        self._progress_bar.setVisible(False)
        self._buttons_box = QDialogButtonBox()
        
        self.update_button = QPushButton(self.tr("&Update"))
        self.update_button.setAutoDefault(True)
        self.close_button = QPushButton(self.tr("&Cancel"))
        self.close_button.setAutoDefault(False)
        self.submit_button = QPushButton(self.tr("&OK"))
        self.submit_button.setAutoDefault(False)

        self.update_button.clicked.connect(self.download)
        self.close_button.clicked.connect(self.reject)
        self.submit_button.clicked.connect(self.download_succeed)

        self.close_button.setEnabled(False)
        self.submit_button.setEnabled(False)

        self._layout.addWidget(self._progress_bar)
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._label_desc)
        self._buttons_box.addButton(self.update_button, QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.submit_button, QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.close_button, QDialogButtonBox.RejectRole)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

        self.update_button.setVisible(True)
        self.update_button.setEnabled(True)
        self.close_button.setVisible(True)
        self.close_button.setEnabled(True)
        self.submit_button.setVisible(False)
        self.submit_button.setEnabled(False)

        filename_update = check_latest_updates()
        if filename_update:
            self.set_url(filename=filename_update)
        else:
            self._label.setText("WALeadApp sudah Update")
            self._label_desc.setText("")
            self.update_button.setVisible(False)
            self.update_button.setEnabled(False)
            self.close_button.setVisible(False)
            self.close_button.setEnabled(False)
            self.submit_button.setVisible(True)
            self.submit_button.setEnabled(True)

    def download_succeed(self):
        self.accept()

    def on_update(self, index,chunk,size):
        print(index,chunk,size)
        percent = 100 * index * chunk // size
        
        self._progress_bar.set_progress(percent)

    def set_url(self, url=None, filename=None):
        if url is None:
            if filename is not None:
                self.filename_zip = filename
                url = "https://github.com/aladeveloper/waleadapp-updates/raw/main/updates/{}".format(filename)
            else:
                print("No File Updates")
        print("url ", url)
        self._url = url 


    def install_update(self, filename_zip):
        platform = get_platform()
        if os.path.isfile(self.filename):
            if  platform=='win':
                # In Windows
                # back up old file
                copy_process = subprocess.Popen(['copy','/Y',self.filename, self.filename+'.origin'])
                del_process = subprocess.Popen(['del','/f',self.filename])
            else:
                # In Linux/Unix
                copy_process = subprocess.Popen(['cp','-rf',self.filename, self.filename+'.origin'])
                del_process = subprocess.Popen(['rm','-rf',self.filename])
        print("extracting zip..")
        with ZipFile(filename_zip, 'r') as zip_obj:
           zip_obj.extractall(path=str(os.path.abspath(os.path.dirname(__file__))))
        if  platform=='win':
            # In Windows
            # delete zip
            del_process = subprocess.Popen(['del','/f',filename_zip])
        else:
            # In Linux/Unix
            del_process = subprocess.Popen(['rm','-rf',filename_zip])


    def download(self):
        try:
            self._progress_bar.setVisible(True)
            self._label.setText("Mengunduh update...")
            self._label_desc.setText("")
            local_zip, headers = request.urlretrieve(self._url, self.filename_zip, self.on_update)
            self._label.setText("Menginstall update...")
            self.install_update(local_zip)
            self._progress_bar.set_progress(100)
            self._label.setText("Yeay.. WALeadApp Anda sudah Update!")
            self._label_desc.setText("Tutup jendela Updater dan WALeadApp!")
            self._progress_bar.setVisible(False)
            self.update_button.setVisible(False)
            self.update_button.setEnabled(False)
            self.close_button.setVisible(False)
            self.close_button.setEnabled(False)
            self.submit_button.setVisible(True)
            self.submit_button.setEnabled(True)
        except Exception as e:
            print("error: ",e)
            self._label.setText("Update Gagal,cek koneksi internet Anda!")
            self._label_desc.setText("")
            self.update_button.setVisible(True)
            self.update_button.setEnabled(True)
            self.close_button.setVisible(True)
            self.close_button.setEnabled(True)
            self.submit_button.setVisible(False)
            self.submit_button.setEnabled(False)

        
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = UpdaterDialog()
#     dialog.show()
#     sys.exit(app.exec_())




