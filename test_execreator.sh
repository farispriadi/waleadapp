#!/bin/bash
echo "======================="
echo "Welcome to Aladeve Executable Creator"
echo "======================="
echo "Easy creating exe from python code on the cloud"
echo "Wine : Test exe file..."
OUTPUT=$(wine $(pwd)/dist/windows/WALeadApp/WALeadApp.exe 2>&1)
IS_OUTERR=false
if [[ $OUTPUT == *"WinError"* ]]
then
	IS_OUTERR = true
	echo "Find Error in Exe File based on OUTPUT"
elif [[ $OUTPUT == *"wine:"* ]]
then
	IS_OUTERR = true
	echo "Find Error in Exe File based on OUTPUT"
elif [[ $OUTPUT == *"err:ntoskrnl:ZwLoadDriver"* ]]
then
	echo "Exe File Seems Good based on OUTPUT"
elif [[ $OUTPUT == *"err:"* ]]
then
	IS_OUTERR = true
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
elif [[ $ERR == *"err:ntoskrnl:ZwLoadDriver"* ]]
then
	echo "Exe File Seems Good based on ERROR"
else
	echo "Exe File Seems Good based on ERROR"
fi
echo "Detail ERROR : $ERR"
echo $IS_ERR
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