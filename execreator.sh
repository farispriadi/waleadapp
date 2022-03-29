#!/bin/bash
echo "======================="
echo "Welcome to Aladeve Executable Creator"
echo "======================="
echo "Easy creating exe from python code on the cloud"
echo "Clean previous dist.."
sudo rm -rf $PWD/dist
echo "PyInstaller : Creating exe file..."
# docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows
docker run --rm -v "$(pwd):/src/" farispriadi/execreator
# docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows -c "sudo apt-get update -y && sudo apt-get install -y winetricks && sudo winetricks -v -q vcrun2015 && pip install --upgrade setuptools  && /entrypoint-windows.sh"
# docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows -c "$W_DRIVE_C=/wine/drive_c && $W_WINDIR_UNIX=$W_DRIVE_C/windows && $W_SYSTEM64_DLLS=$W_WINDIR_UNIX/system32 && $W_TMP=$W_DRIVE_C/windows/temp/_$0 && rm -f $W_TMP/* && wget -P $W_TMP https://download.microsoft.com/download/0/6/4/064F84EA-D1DB-4EAA-9A5C-CC2F0FF6A638/vc_redist.x64.exe && cabextract -q --directory='$W_TMP' '$W_TMP'/vc_redist.x64.exe && cabextract -q --directory='$W_TMP' '$W_TMP/a10' && cabextract -q --directory='$W_TMP' '$W_TMP/a11' && cd $W_TMP rename 's/_/\-/g' *.dll && cp $W_TMP/*.dll $W_SYSTEM64_DLLS/ && /entrypoint.sh"

echo "PyInstaller : Exe file created successfully"
echo "Wine : Test exe file..."
# TODO : Agar tidak muncul GUI
# Kode :
# Xvfb :0 -screen 0 1024x768x24 & 
# di Entry point docker
# install wine on docker
OUTPUT=$(wine $(pwd)/dist/windows/WALeadApp/WALeadApp.exe 2>&1)
IS_OUTERR=false
if [[ $OUTPUT == *"WinError"* ]]
then
	IS_OUTERR=true
	echo "Find Error in Exe File based on OUTPUT"
elif [[ $OUTPUT == *"wine:"* ]]
then
	IS_OUTERR=true
	echo "Find Error in Exe File based on OUTPUT"
elif [[ $ERR == *"exit status 1"* ]]
then
	IS_OUTERR=true
	echo "Find Error in Exe File based on OUTPUT"
elif [[ $OUTPUT == *"err:ntoskrnl:ZwLoadDriver"* ]]
then
	echo "Exe File Seems Good based on OUTPUT"
elif [[ $OUTPUT == *"err:"* ]]
then
	IS_OUTERR=true
	echo "Find Error in Exe File based on OUTPUT"
else
	echo "Exe File Seems Good based on OUTPUT"
fi
echo "Detail OUTPUT : $OUTPUT"

ERR=$(wine $(pwd)/dist/windows/WALeadApp/WALeadApp.exe 2>&1)?
IS_ERR=false

if [[ $ERR == *"WinError"* ]]
then
	IS_ERR=true
	echo "Find Error in Exe File based on ERROR"
elif [[ $ERR == *"wine:"* ]]
then
	IS_ERR=true
	echo "Find Error in Exe File based on ERROR"
elif [[ $ERR == *"exit status 1"* ]]
then
	IS_ERR=true
	echo "Find Error in Exe File based on ERROR"
elif [[ $ERR == *"err:ntoskrnl:ZwLoadDriver"* ]]
then
	echo "Exe File Seems Good based on ERROR"
else
	echo "Exe File Seems Good based on ERROR"
fi
echo "Detail ERROR : $ERR"
echo $(date -u) $IS_ERR >> err.log
echo $IS_ERR 
echo $(date -u) $IS_OUTERR >> output_err.log
echo $IS_OUTERR


if $IS_OUTERR || $IS_ERR
then
	echo "ABORT Prepare innosetup script..."
else
	echo "Preparing innosetup script..."
	cp $PWD/innosetup_waleadapp.iss $PWD/dist/windows/
	echo "InnoSetup: Creating setup file..."
	docker run --rm -v "$(pwd)/dist/windows:/work/" amake/innosetup innosetup_waleadapp.iss
	echo "InnoSetup: Setup file created successfully"
	echo "Zipping setup file..."
	cd $(pwd)/dist/windows/Output/
	filename=$(ls -t WALeadApp-* | head -1)
	echo "Latest Setup : $filename"
	zipfilename="WALeadApp-setup.zip"
	echo "Zip filename : $zipfilename"
	zip -j $(pwd)/$zipfilename $(pwd)/$filename
	echo "Your Setup File is Ready, $(pwd)/dist/windws/Output/$zipfilename"
fi
