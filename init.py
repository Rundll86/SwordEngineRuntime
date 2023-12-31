import os, zipfile

os.system("pip install Pyinstaller")
zipfile.ZipFile("core.zip").extractall("source/Core")
