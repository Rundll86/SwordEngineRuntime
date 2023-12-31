import json, conkits, os, easygui, msvcrt, shutil, subprocess, ctypes, sys, winreg

LanguageList = []
LanguageDisplayName = []
for i in os.listdir(os.path.join(os.path.dirname(__file__), "language")):
    try:
        File = open(
            os.path.join(os.path.dirname(__file__), "language", i), "r", encoding="utf8"
        )
        Data = json.load(File)
        LanguageList.append(Data)
        LanguageDisplayName.append(Data["Name"])
        File.close()
    except:
        continue
CurrentLanguage = "简体中文"


def PrettyPrint(Type, Value=None, Block=True):
    LanguageData = None
    for i in LanguageList:
        if i["Name"] == CurrentLanguage:
            LanguageData = i
    if Value is None:
        print(LanguageData[Type], end="\n" if Block else "", flush=True)
    else:
        print(LanguageData[Type][Value], end="\n" if Block else "", flush=True)


def CreateChoice(Options, Methods=None):
    selector = conkits.Choice(options=Options, methods=Methods)
    selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    selector.unchecked_ansi_code = conkits.Colors256.FORE255
    selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    return selector


def ClearConsole():
    os.system("cls")


def Getch():
    PrettyPrint("Press")
    msvcrt.getch()


def RunAsPowerShell(Cmd):
    subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def is_admin():
    try:
        return not not ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    PrettyPrint("NotAdmin")
    Getch()
    sys.exit()

ClearConsole()
PrettyPrint("Flow", 0)
CurrentLanguage = LanguageDisplayName[CreateChoice(LanguageDisplayName).run()]
PrettyPrint("Flow", 1)
Getch()
while True:
    PrettyPrint("Flow", 2, False)
    InstallPath = easygui.diropenbox()
    if InstallPath is None:
        print("")
        continue
    else:
        InstallPath = os.path.join(InstallPath, "SwordEngineRuntime")
        if not os.path.exists(InstallPath):
            os.mkdir(InstallPath)
        break
print(f"[ {InstallPath} ]")
PrettyPrint("Flow", 3)
PrettyPrint("Flow", 4)
shutil.copy(os.path.join(os.path.dirname(__file__), "asset/SwordRun.exe"), InstallPath)
PrettyPrint("Flow", 5)
shutil.copy(os.path.join(os.path.dirname(__file__), "asset/SwordProj.exe"), InstallPath)
PrettyPrint("Flow", 6)
if InstallPath not in os.environ["PATH"]:
    RunAsPowerShell(f'setx /M PATH "%PATH%;{InstallPath}"')
if os.environ.get("SWORD_INSTALL_PATH") is None:
    RunAsPowerShell(f'setx /M SWORD_INSTALL_PATH "{InstallPath}"')
PrettyPrint("Flow", 7)
shutil.copy(os.path.join(os.path.dirname(__file__), "favicon.ico"), InstallPath)
key = winreg.CreateKey(
    winreg.HKEY_LOCAL_MACHINE,
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SwordEngineRuntime",
)
winreg.SetValueEx(key, "DisplayName", None, winreg.REG_SZ, "SwordEngine Runtime")
winreg.SetValueEx(
    key, "DisplayIcon", None, winreg.REG_SZ, os.path.join(InstallPath, "favicon.ico")
)
key.Close()
PrettyPrint("Flow", 8)
Getch()
sys.exit()
