from . import updater

def show_updater():
    dialog = updater.UpdaterDialog()
    if dialog.exec_():
        return True    
    return False

def check_updates():
    if updater.check_latest_updates():
        return True
    return False