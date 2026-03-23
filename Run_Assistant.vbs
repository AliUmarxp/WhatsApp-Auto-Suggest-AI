Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = strPath

' 0 means hide window completely, False means don't wait for it to finish
objShell.Run "python main.py", 0, False
