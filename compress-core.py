import zipfile, os


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


ZipDir("..\\SwordEngineCore", "source/Library/SwordEngineCore.zip")
