echo off
cls
Pyinstaller -F source/SwordRun.py --add-data "source/Info.json;." --add-data "source/Core;Core" --add-data "source/Template;Template" -i favicon.ico