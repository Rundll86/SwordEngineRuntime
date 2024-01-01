echo off
cls
python compress-core.py
Pyinstaller -F source/SwordProj.py --add-data "source/Info.json;." --add-data "source/Library;Library" --add-data "source/Template;Template" --add-data "source/Favicon.ico;." -i favicon.ico