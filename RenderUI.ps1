$ErrorActionPreference = 'Stop'
$projectPython = Get-Command python -ErrorAction Stop
$env:PYTHONIOENCODING = 'utf-8'
& $projectPython.Source (Join-Path $PSScriptRoot 'tools/export_ui.py')
if ($LASTEXITCODE -ne 0) { throw 'UI export failed.' }
& $projectPython.Source (Join-Path $PSScriptRoot 'tools/render_ui.py')
if ($LASTEXITCODE -ne 0) { throw 'UI rendering failed.' }
