import chromedriver_autoinstaller
from PySide2.QtWidgets import QProgressBar
from PySide2.QtCore import QThread, Signal, Qt
        

class ProgressBar(QProgressBar):
    """docstring for ProgressBar"""
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent=None)
        self.setFormat(str(round(self.value()))+"%")

    def set_progress(self,progress):
        self.setValue(progress)
        self.setFormat(str(progress)+"%")
        
    def stop(self):
        self.setVisible(False)


class FunctionThread(QThread):
    """docstring for FunctionThread
    untuk function_obj ada 2 tipe
    - send_message(mobile, message, attachments=None)
    - collect_response(mobile, token_id)
    - result: dict of report

    """
    progress_started = Signal(str)
    progress_finished = Signal(dict)
    progress_error = Signal(str)
    def __init__(self,function_obj=None,ending_sleep=10, *args, **kwargs):
        super(FunctionThread, self).__init__()
        self.function = function_obj
        self.args = args
        self.kwargs = kwargs
        self.result = {}
        self.ending_sleep = ending_sleep

    def run(self):
        self.sleep(5)
        print("start sending")
        if 'mobile' in self.kwargs:
            self.progress_started.emit(str(self.kwargs['mobile']))
        else:
            self.progress_started.emit('') 

        if 'result' in self.kwargs:
            pass

        if 'token' in self.kwargs:
            print("token ", self.kwargs['token'])

        if 'qthread' in self.kwargs:
            self.kwargs['qthread'] = self
        try:
            self.result = self.function(*self.args, **self.kwargs)
            self.progress_finished.emit(self.result)
        except Exception as e:
            print("exception ", e)            
            self.progress_finished.emit({})
            self.progress_error.emit(e)
        self.sleep(self.ending_sleep)


class LoginThread(QThread):
    """docstring for FunctionThread
    untuk function_obj ada 2 tipe
    - send_message(mobile, message, attachments=None)
    - collect_response(mobile, token_id)
    - result: dict of report

    """
    login_finished = Signal(bool)
    def __init__(self,function_obj=None, *args, **kwargs):
        super(LoginThread, self).__init__()
        self.function = function_obj
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print("start login")
        self.function()
        self.sleep(10)
        print("Login ended")
        self.login_finished.emit(True)


class DownloadThread(QThread):
    """docstring for FunctionThread
    untuk function_obj ada 2 tipe
    - send_message(mobile, message, attachments=None)
    - collect_response(mobile, token_id)
    - result: dict of report

    """
    download_finished = Signal(str)
    download_report = Signal(str)
    def __init__(self,function_obj=None, *args, **kwargs):
        super(DownloadThread, self).__init__()
        self.function = function_obj
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print("start download")
        try:
            if 'handler' in self.kwargs:
                local_file = self.function(handler=self.kwargs['handler'])
            else:
                local_file = self.function()
            msg = "Download succeed"
        except Exception as e:
            local_file = ""
            msg = str(e)
        self.sleep(5)
        self.download_finished.emit(local_file)
        self.download_report.emit(msg)

class ConnectThread(QThread):
    """docstring for FunctionThread
    untuk function_obj ada 2 tipe
    - send_message(mobile, message, attachments=None)
    - collect_response(mobile, token_id)
    - result: dict of report

    """
    connect_finished = Signal(list)
    connect_report = Signal(str)
    def __init__(self,function_obj=None, *args, **kwargs):
        super(ConnectThread, self).__init__()
        self.function = function_obj
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if "tag" in self.kwargs:
            print("start getting contacts...")    
        else:
            print("start connecting...")
        try:
            data = self.function(**self.kwargs)
            msg = "Connected"
            status = True
        except Exception as e:
            data = {}
            local_file = ""
            msg = str(e)
            status = False
        self.sleep(1)
        emit_data = [status,data]
        self.connect_finished.emit(emit_data)
        self.connect_report.emit(msg)

class SendingBar(ProgressBar):
    """docstring for SendingBar"""
    def __init__(self, parent=None):
        super(SendingBar, self).__init__(parent=None)
        self.setValue(0)
        self.setFormat("Sending Messages : "+str(round(self.value()))+"%")

        
    def set_progress(self,progress):
        self.setValue(progress)
        self.setFormat("Sending Messages : "+str(round(progress))+"%")

    def set_stop(self):
        progress= self.value()
        self.setFormat("(Stoped) Sending Messages : "+str(round(progress))+"%")

    def set_resume(self):
        progress= self.value()
        self.setFormat("Sending Messages : "+str(round(progress))+"%")


class CollectingBar(ProgressBar):
    """docstring for CollectingBar"""
    def __init__(self, parent=None):
        super(CollectingBar, self).__init__(parent=None)
        self.setValue(0)
        self.setFormat("Collecting Responses : "+str(round(self.value()))+"%")
    
    def set_progress(self,progress):
        self.setValue(progress)
        self.setFormat("Collecting Responses : "+str(round(progress))+"%")

    def set_stop(self):
        progress= self.value()
        self.setFormat("(Stoped) Collecting Messages : "+str(round(progress))+"%")

    def set_resume(self):
        progress= self.value()
        self.setFormat("Collecting Messages : "+str(round(progress))+"%")


        

        




        
        


