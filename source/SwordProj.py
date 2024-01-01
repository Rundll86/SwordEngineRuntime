import os, argparse, json, shutil, subprocess, zipfile


def RunAsPowerShell(Cmd):
    subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def CamelToSnakeCase(CamelCaseString):
    snake_case_string = ""
    check_list = "abcdefghijklmnopqrstuvwxyz-0123456789"
    for char in CamelCaseString:
        char: str
        if char.isupper():
            snake_case_string += "-" + char.lower()
        else:
            snake_case_string += char
    if snake_case_string[0] == "-":
        snake_case_string = snake_case_string[1:]
    for i in snake_case_string:
        if i not in check_list:
            snake_case_string = snake_case_string.strip(i)
    return snake_case_string


def MkdirIfNotExists(Path):
    if not os.path.exists(Path):
        os.mkdir(Path)


def RemoveDirIfExists(Path):
    if os.path.exists(Path) and os.path.isdir(Path):
        RunAsPowerShell(f'rmdir /s /q "{Path}"')


def ZipDir(DirName, FileName, DontZip: list = []):
    FolderPath = os.path.join(os.getcwd(), DirName)
    File = zipfile.ZipFile(FileName, "w")
    DontZip.append(FileName)
    for Root, _, Files in os.walk(FolderPath):
        if os.path.basename(Root) in DontZip:
            continue
        for File2 in Files:
            if File2 in DontZip:
                continue
            FilePath = os.path.join(Root, File2)
            File.write(FilePath, os.path.relpath(FilePath, FolderPath))
    File.close()


class ActionType:
    Create = "CREATE"
    Build = "BUILD"


class ExternalArg:
    Action = ActionType.Create
    Name = "MyGame"
    Author = ""
    Version = "1.0.0"
    MainClass = "MyGame"
    Config = "sword.config.json"
    DevelopMode = False


RunningDir = os.path.dirname(__file__)
InfoFile = os.path.join(RunningDir, "Info.json")
InfoData = json.load(open(InfoFile, encoding="utf8"))
VersionInfo = InfoData["Version"]
TemplatePath = os.path.join(RunningDir, "Template")
LibraryPath = os.path.join(RunningDir, "Library")
BuilderPath = os.path.join(LibraryPath, "Builder", "builder.exe")
Parser = argparse.ArgumentParser()
Parser.add_argument("Action")
Parser.add_argument("-N", "--Name", default=ExternalArg.Name)
Parser.add_argument("-A", "--Author", default=ExternalArg.Author)
Parser.add_argument("-V", "--Version", default=ExternalArg.Version)
Parser.add_argument("-E", "--MainClass", default=ExternalArg.MainClass)
Parser.add_argument("-C", "--Config", default=ExternalArg.Config)
Parser.add_argument(
    "-D", "--DevelopMode", default=ExternalArg.DevelopMode, action="store_true"
)
Args: ExternalArg = Parser.parse_args()
if Args.Action.upper() == ActionType.Create:
    print(f'Creating "{Args.Name}"...')
    print(f"Initing {'develop ' if Args.DevelopMode else ''}workspace...")
    MkdirIfNotExists("source")
    open(f"source/{Args.MainClass}.js", "w", encoding="utf8").write(
        open(
            os.path.join(
                TemplatePath, f"MainClass{'-Develop' if Args.DevelopMode else ''}.js"
            ),
            "r",
            encoding="utf8",
        )
        .read()
        .replace("$ClassName$", Args.MainClass)
        .replace("$GameName$", Args.Name)
    )
    shutil.copyfile(os.path.join(RunningDir, "Favicon.ico"), "favicon.ico")
    print("Initing config files...")
    Package = {
        "name": CamelToSnakeCase(Args.Name),
        "version": Args.Version,
        "author": Args.Author,
        "scripts": {"start": "swordrun -r ."},
        "devDependencies": {"sword-engine-core": "^1.0.0"},
    }
    json.dump(Package, open("package.json", "w", encoding="utf8"))
    SwordConfig = {
        "Name": Args.Name,
        "Author": "",
        "Version": "1.0.0",
        "Build": {
            "IncludingRuntime": False,
            "CompressRelease": True,
            "OutputPath": "build",
            "Clean": True,
            "Favicon": "favicon.ico",
        },
        "MainClass": "MyGame",
        "Entry": "./source/{MainClass}.js",
        "SwordRun": VersionInfo["Run"],
    }
    json.dump(SwordConfig, open(Args.Config, "w", encoding="utf8"))
    print("Installing libraries...")
    MkdirIfNotExists(os.path.join(LibraryPath, "SwordEngineCore"))
    zipfile.ZipFile(os.path.join(LibraryPath, "SwordEngineCore.zip")).extractall(
        os.path.join(LibraryPath, "SwordEngineCore")
    )
    MkdirIfNotExists("node_modules")
    RemoveDirIfExists("node_modules\\sword-engine-core")
    shutil.copytree(
        os.path.join(LibraryPath, "SwordEngineCore"),
        "node_modules\\sword-engine-core",
    )
    RemoveDirIfExists("node_modules\\sword-engine-core\\node_modules")
    os.remove("node_modules\\sword-engine-core\\package-lock.json")
    os.remove("node_modules\\sword-engine-core\\pushing.bat")
    os.remove("node_modules\\sword-engine-core\\.gitignore")
    RunAsPowerShell(f"rmdir /s /q node_modules\\sword-engine-core\\.git")
    RunAsPowerShell(f'rmdir /s /q "{os.path.join(LibraryPath, "SwordEngineCore")}"')
    print("OK.")
elif Args.Action.upper() == ActionType.Build:
    SwordConfig = json.load(open(Args.Config, "r", encoding="utf8"))
    if SwordConfig["Build"]["Clean"]:
        print("Cleaning...")
        RunAsPowerShell(f'rmdir /s /q "{SwordConfig["Build"]["OutputPath"]}"')
        os.makedirs(SwordConfig["Build"]["OutputPath"])
    print("Compressing game data...")
    MkdirIfNotExists(SwordConfig["Build"]["OutputPath"])
    ZipDir(
        ".",
        os.path.join(SwordConfig["Build"]["OutputPath"], "GameAsset.ddm"),
        [SwordConfig["Build"]["OutputPath"]],
    )
    print("Generating executable file...")
    print(" - Generating source code...")
    shutil.copy(
        os.path.join(LibraryPath, "Executable", "Executable.py"),
        SwordConfig["Build"]["OutputPath"],
    )
    print(" - Generating start up info...")
    CurrentDir = os.getcwd()
    os.chdir(SwordConfig["Build"]["OutputPath"])
    InfoFile = {
        "Name": SwordConfig["Name"],
        "IncludeRuntime": SwordConfig["Build"]["IncludingRuntime"],
    }
    json.dump(InfoFile, open("Info.json", "w", encoding="utf8"))
    print(" - Building executable file...")
    print("  - Generating build tree...")
    StartData = [
        BuilderPath,
        "-w",
        "-i",
        os.path.join(CurrentDir, SwordConfig["Build"]["Favicon"]),
        "-F",
        os.path.join(LibraryPath, "Executable", "Executable.py"),
        "--add-data",
        "GameAsset.ddm;.",
        "--add-data",
        "Info.json;.",
    ]
    if SwordConfig["Build"]["IncludingRuntime"]:
        print("   - Loading runtime archive...")
        StartData.append("--add-data")
        StartData.append(
            os.path.join(os.environ["SWORD_INSTALL_PATH"], "SwordRun.exe") + ";."
        )
    print("  - Generating...")
    subprocess.Popen(
        StartData,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    ).wait()
    print(" - Cleaning...")
    os.remove("GameAsset.ddm")
    os.remove("Executable.py")
    os.remove("Executable.spec")
    os.remove("Info.json")
    RunAsPowerShell("rmdir /s /q build")
    shutil.copyfile("dist\\Executable.exe", f"{SwordConfig['Name']}.exe")
    RunAsPowerShell("rmdir /s /q dist")
    if SwordConfig["Build"]["CompressRelease"]:
        print("Compressing game release...")
        File = zipfile.ZipFile("GameRelease.zip", "w")
        File.write(f"{SwordConfig['Name']}.exe")
        File.close()
    os.chdir(CurrentDir)
    print("Builded successfully.")
else:
    print("Invalid ActionType.")
