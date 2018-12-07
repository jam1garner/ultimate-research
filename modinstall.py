import sys
import os

def _isValidHex(s):
    try:
        int(s, 16)
        return True
    except:
        return False

def getFileBaseName(path):
    return os.path.splitext(os.path.split(path)[-1])[0]

def installMod(archive, modFilename):
    offset = int(getFileBaseName(modFilename), 16)
    archive.seek(offset)
    with open(modFilename, 'rb') as f:
        modContents = f.read()
        modSize = len(modContents)
        backup = archive.read(modSize)
        with open(modFilename + '.backup', 'wb') as f_backup:
            f_backup.write(backup)
        archive.seek(offset)
        archive.write(modContents)
    print("Mod '{}' successfully installed".format(modFilename))

def main(args):
    if len(args) == 0 or args == ['--help']:
        print("No mod paths passed\n\nUsage:\npython3 modinstall.py [mod paths]")
        quit()

    if not os.path.exists("data.arc"):
        print("Make sure you're running the script beside your data.arc")
        quit()

    with open('data.arc', 'r+b') as archive:
        for mod in args:
            if not os.path.exists(mod):
                print("'{}' not valid mod path".format(mod))
                continue
            fileName = getFileBaseName(mod)
            if not _isValidHex(fileName):
                print("Filename '{}' not valid hex number".format(fileName))
                continue
            installMod(archive, mod)
    
if __name__ == "__main__":
    main(sys.argv[1:])
