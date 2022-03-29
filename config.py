import os
import pathlib
import datetime
import wawebxpath

ROOT_PATH = pathlib.Path(os.getcwd()).resolve()
BASE_PATH = ROOT_PATH.joinpath("WALeadApp").resolve()
ASSETS_PATH = BASE_PATH.joinpath("assets").resolve()
VIEWS_PATH = BASE_PATH.joinpath("views").resolve()
CONTROLLERS_PATH = BASE_PATH.joinpath("controllers").resolve()
REPORTS_PATH = BASE_PATH.joinpath("reports").resolve()
CONTACTS_PATH = BASE_PATH.joinpath("contacts").resolve()
MEDIA_PATH = BASE_PATH.joinpath("media").resolve()
MODEL_PATH = BASE_PATH.joinpath("models").resolve()


ABOUT = {'app_name': 'WALeadApp',
            'version': '2.1.2021.12.22',#'1.0.yyyy.mmdd',
            'whatsapp': wawebxpath.WAXPATH["version"],
            'year': '2021',
            'author': 'Faris Priadi',
            'email': 'farispriadi@gmail.com',
            'publisher': 'Aladeve Inovasi Desa'
        }

