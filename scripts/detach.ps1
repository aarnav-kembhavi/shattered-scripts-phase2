# Start a bash script detached from Claude Code (and from any terminal) as a Windows scheduled task, so it survives
# the session ending. The task runs as the current user, hidden, on battery too, with no time limit.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name m4c -Script scripts/m4c_chain.sh [-ScriptArgs "..."]
# Task name: ShatteredScripts_<Name>. Inspect: Get-ScheduledTask ShatteredScripts_* | Get-ScheduledTaskInfo
# Stop:      Stop-ScheduledTask ShatteredScripts_<Name>   (kills the hidden wscript; child processes may need Stop-Process)
param([Parameter(Mandatory)][string]$Name, [Parameter(Mandatory)][string]$Script, [string]$ScriptArgs = "")
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$bash = "C:\Program Files\Git\bin\bash.exe"
$task = "ShatteredScripts_$Name"
$inner = "cd '$($repo -replace '\\','/')' && exec bash $Script $ScriptArgs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -WorkingDirectory $repo `
  -Argument "//B `"$repo\scripts\hidden.vbs`" `"$bash`" -lc `"$inner`""
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
  -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -StartWhenAvailable
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddYears(10)  # never fires; started explicitly below
Register-ScheduledTask -TaskName $task -Action $action -Settings $settings -Trigger $trigger -Force | Out-Null
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 3
Get-ScheduledTask -TaskName $task | Get-ScheduledTaskInfo | Select-Object TaskName, LastRunTime, LastTaskResult
(Get-ScheduledTask -TaskName $task).State
