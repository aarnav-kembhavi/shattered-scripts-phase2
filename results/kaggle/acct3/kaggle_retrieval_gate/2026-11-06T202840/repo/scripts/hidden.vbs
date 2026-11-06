' Run a command line with no console window and wait for it (so the scheduled task stays "Running" while it runs).
' Usage: wscript.exe //B hidden.vbs <program> [args...]
Set sh = CreateObject("WScript.Shell")
cmd = ""
For Each a In WScript.Arguments
  cmd = cmd & " """ & a & """"
Next
WScript.Quit sh.Run(Trim(cmd), 0, True)
