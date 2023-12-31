echo off
cls
rmdir /s /q installer\asset
mkdir installer\asset
copy dist\SwordRun.exe installer\asset
copy dist\SwordProj.exe installer\asset
copy favicon.ico installer\favicon.ico
Pyinstaller -F installer/installer.py --add-data "installer/asset;asset" --add-data "installer/language;language" --add-data "favicon.ico;." -i favicon.ico