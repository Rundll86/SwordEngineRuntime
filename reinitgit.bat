rmdir /s /q .git
git clone git@github.com:Rundll86/SwordEngineRuntime.git
xcopy /e /i /h /y SwordEngineRuntime\.git .git
rmdir /s /q SwordEngineRuntime
pushing.bat