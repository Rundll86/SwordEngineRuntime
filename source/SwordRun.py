import os, argparse, json, subprocess, tempfile, random


def RunAsPowerShell(Cmd):
    subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def RandomString(Length):
    Result = ""
    for _ in range(Length):
        Result += random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        )
    return Result


class ExternalArg:
    Run = None
    Version = None


RunningDir = os.path.dirname(__file__)
while True:
    Tempdir = os.path.join(
        tempfile.gettempdir(), "SwordRun-Object", RandomString(random.randint(10, 20))
    )
    if not os.path.exists(Tempdir):
        if not os.path.exists(os.path.join(tempfile.gettempdir(), "SwordRun-Object")):
            os.mkdir(os.path.join(tempfile.gettempdir(), "SwordRun-Object"))
        os.mkdir(Tempdir)
        break
TemplatePath = os.path.join(RunningDir, "Template")
CoreFile = os.path.join(RunningDir, "Core", "runtime-core.exe")
InfoFile = os.path.join(RunningDir, "Info.json")
InfoData = json.load(open(InfoFile, encoding="utf8"))
VersionInfo = InfoData["Version"]
Parser = argparse.ArgumentParser()
Parser.add_argument("-R", "--Run", "-r", "--run", dest="Run", default=None)
Parser.add_argument(
    "-V", "--Version", "-v", "--version", dest="Version", action="store_true"
)
Args: ExternalArg = Parser.parse_args()
if Args.Version:
    print(VersionInfo["Run"])
if Args.Run is not None:
    os.chdir(Args.Run)
    Config = json.load(open("sword.config.json", "r", encoding="utf8"))
    LoaderFile = open(os.path.join(Tempdir, "sword-loader.js"), "w", encoding="utf8")
    LoaderFile.write(
        open(os.path.join(TemplatePath, "Loader.js"), "r", encoding="utf8")
        .read()
        .replace("$ClassName$", Config["MainClass"])
        .replace(
            "$MainFile$",
            os.path.join(
                os.getcwd(), Config["Entry"].format(MainClass=Config["MainClass"])
            ).replace("\\", "/"),
        )
        .replace("$AbsPath$", os.getcwd().replace("\\", "/"))
    )
    LoaderFile.close()
    print("SwordEngine Loaded!")
    print("GamePath:", os.getcwd())
    print("SwordLoader:", os.path.join(Tempdir, "sword-loader.js"))
    print("Runtime:", RunningDir)
    subprocess.Popen(
        [CoreFile, os.path.join(Tempdir, "sword-loader.js")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
