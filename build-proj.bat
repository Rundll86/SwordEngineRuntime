echo off
cls
rmdir /s /q source\Library
mkdir source\Library
xcopy /e /i /h /y ..\SwordEngineCore source\Library\SwordEngineCore
Pyinstaller -F source/SwordProj.py --add-data "source/Info.json;." --add-data "source/Library;Library" --add-data "source/Template;Template" -i favicon.ico