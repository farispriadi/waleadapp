# -*- mode: python -*-
app_name = 'WALeadApp'

import pathlib
import os

block_cipher = None

RELATIVE_PATH = './'
BASE_PATH = pathlib.Path(os.getcwd()).resolve()
ICON_PATH = str(BASE_PATH.joinpath("WALeadApp","assets","{}.ico".format(app_name.lower())).resolve())
MAIN_PATH = str(BASE_PATH.joinpath("main.py").resolve())

STATIC_FILES = [
  (RELATIVE_PATH + 'WALeadApp/assets/waleadapp.ico', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/waleadapp.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/emojis-24.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/dark.qss', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/send.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/stop.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/send_disabled.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/stop_disabled.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/emoji.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/clip.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/emoji_open.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/clip_open.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/emoji_closed.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/clip_closed.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/plus.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/minus.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/invalid.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/failed.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/sent.png', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'WALeadApp/assets/emojis-png-locations-24.json', 'WALeadApp/assets/'),
  (RELATIVE_PATH + 'innosetup_waleadapp.iss', 'deploy/'),
]

a = Analysis([MAIN_PATH],
             pathex= [BASE_PATH],
             binaries=[],
             datas=STATIC_FILES,
             hiddenimports=['jinja2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=app_name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon=ICON_PATH)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=app_name)
