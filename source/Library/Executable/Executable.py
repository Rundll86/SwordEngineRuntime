import zipfile, subprocess, os, sys, json, random, easygui


def RandomString(Length):
    Result = ""
    for _ in range(Length):
        Result += random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        )
    return Result


RunningDir = os.path.dirname(__file__)
Info = json.load(open(os.path.join(RunningDir, "Info.json"), "r", encoding="utf8"))
GamePath = "C:\\"
while os.path.exists(GamePath):
    GamePath = os.path.expanduser(
        os.path.join(
            "~",
            "Documents",
            "My Games",
            Info["Name"],
            "Objects",
            RandomString(random.randint(10, 20)),
        )
    )
zipfile.ZipFile(os.path.join(RunningDir, "GameAsset.ddm")).extractall(GamePath)
if Info["IncludeRuntime"]:
    subprocess.Popen(
        [
            os.path.join(RunningDir, "SwordRun.exe"),
            "--Run",
            os.path.join(GamePath, Info["DirName"] if Info["Develop"] else ""),
        ]
    ).wait()
else:
    if os.environ["SWORD_INSTALL_PATH"] is None:
        easygui.msgbox(
            "Your computer has not yet installed SwordEngineRuntime. Please install it or ask the game author for a version of the game with a runtime.",
            "Error",
            icon="error",
        )
        sys.exit()
    else:
        subprocess.Popen(
            [
                os.path.join(os.environ["SWORD_INSTALL_PATH"], "SwordRun.exe"),
                "--Run",
                GamePath,
            ]
        ).wait()
