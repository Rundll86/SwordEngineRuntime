import os, argparse, json, shutil, subprocess


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


class ActionType:
    Create = "Create"
    Build = "Build"


class ExternalArg:
    Action = ActionType.Create
    Name = "MyGame"
    Author = ""
    Version = "1.0.0"
    MainClass = "MyGame"
    Config = "sword.config.json"


RunningDir = os.path.dirname(__file__)
InfoFile = os.path.join(RunningDir, "Info.json")
InfoData = json.load(open(InfoFile, encoding="utf8"))
VersionInfo = InfoData["Version"]
TemplatePath = os.path.join(RunningDir, "Template")
LibraryPath = os.path.join(RunningDir, "Library")
Parser = argparse.ArgumentParser()
Parser.add_argument("Action")
Parser.add_argument("-N", "--Name", default="MyGame")
Parser.add_argument("-A", "--Author", default="")
Parser.add_argument("-V", "--Version", default="1.0.0")
Parser.add_argument("-E", "--MainClass", default="MyGame")
Parser.add_argument("-C", "--Config", default="sword.config.json")
Args: ExternalArg = Parser.parse_args()
if Args.Action == ActionType.Create:
    print(f'Creating "{Args.Name}"...')
    print("Initing workspace...")
    MkdirIfNotExists("source")
    open(f"source/{Args.MainClass}.js", "w", encoding="utf8").write(
        open(os.path.join(TemplatePath, "MainClass.js"), "r", encoding="utf8")
        .read()
        .replace("$ClassName$", Args.MainClass)
        .replace("$GameName$", Args.Name)
    )
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
            "Platform": "win32",
            "IncludeRuntime": False,
            "CompressRelease": True,
        },
        "MainClass": "MyGame",
        "Entry": "./source/{MainClass}.js",
    }
    json.dump(SwordConfig, open(Args.Config, "w", encoding="utf8"))
    print("Installing libraries...")
    MkdirIfNotExists("node_modules")
    RemoveDirIfExists("node_modules\\sword-engine-core")
    shutil.copytree(
        os.path.join(LibraryPath, "SwordEngineCore"),
        "node_modules\\sword-engine-core",
    )
    RemoveDirIfExists("node_modules\\sword-engine-core\\node_modules")
    os.remove("node_modules\\sword-engine-core\\package-lock.json")
    print("OK.")
elif Args.Action == ActionType.Build:
    pass
else:
    print("Invalid ActionType.")
