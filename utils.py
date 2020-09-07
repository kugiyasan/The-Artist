import json

with open("dialogs.json") as jsonFile:
    dialogs = json.load(jsonFile)

def printLine():
    print("\u001b[1;37;40m" + "=" * 49)