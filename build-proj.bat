echo off
cls
rmdir /s /q source\Library\SwordEngineCore
xcopy /e /i /h /y ..\SwordEngineCore source\Library\SwordEngineCore
Pyinstaller -F source/SwordProj.py --add-data "source/Info.json;." --add-data "source/Library;Library" --add-data "source/Template;Template" --add-data "source/Favicon.ico;." -i favicon.ico