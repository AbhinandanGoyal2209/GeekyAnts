$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".codex_python311\python.exe"

if (-not (Test-Path $python)) {
    throw "Portable Python runtime not found at $python"
}

Set-Location $root
& $python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
