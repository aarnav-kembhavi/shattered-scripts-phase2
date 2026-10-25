param([string]$book, [string]$sheet, [string]$range, [string]$png)
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
$wb = $xl.Workbooks.Open($book)
$ws = $wb.Worksheets.Item($sheet)
$ws.Activate(); $ws.Unprotect()
$r = $ws.Range($range)
$r.Rows.AutoFit() | Out-Null
$r.CopyPicture(1, 2) | Out-Null
$co = $ws.ChartObjects().Add(0, 0, $r.Width, $r.Height)
$co.Activate() | Out-Null
$co.Chart.Paste() | Out-Null
$co.Chart.Export($png) | Out-Null
$co.Delete() | Out-Null
$wb.Close($false); $xl.Quit()
"ok $png"
