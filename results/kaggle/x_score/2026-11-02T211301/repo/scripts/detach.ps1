# Start a bash script detached from Claude Code (and from any terminal) as a Windows scheduled task, so it survives
# the session ending. The task runs as the current user, hidden, on battery too, with no time limit.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name m4c -Script scripts/m4c_chain.sh [-ScriptArgs "..."]
# Besides starting now, the task is restarted at logon and whenever Windows resumes from sleep (System log,
# Power-Troubleshooter event 1): on 2026-10-17 a sleep ended the running chains. A second instance is never started
# while one is running (IgnoreNew); chains resume from the cache and exit at once if their status is DONE.
# Task name: ShatteredScripts_<Name>. Inspect: Get-ScheduledTask ShatteredScripts_* | Get-ScheduledTaskInfo
# Stop:      Stop-ScheduledTask ShatteredScripts_<Name>   (kills the hidden wscript; child processes may need Stop-Process)
# Remove:    Unregister-ScheduledTask ShatteredScripts_<Name> -Confirm:$false   (otherwise it restarts on every wake)
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
$logon = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$cls = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$wake = New-CimInstance -CimClass $cls -ClientOnly
$wake.Enabled = $true
$wake.Delay = "PT1M"
$wake.Subscription = '<QueryList><Query Id="0" Path="System"><Select Path="System">' +
  "*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and EventID=1]]</Select></Query></QueryList>"
Register-ScheduledTask -TaskName $task -Action $action -Settings $settings -Trigger @($logon, $wake) -Force | Out-Null
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 3
Get-ScheduledTask -TaskName $task | Get-ScheduledTaskInfo | Select-Object TaskName, LastRunTime, LastTaskResult
(Get-ScheduledTask -TaskName $task).State
