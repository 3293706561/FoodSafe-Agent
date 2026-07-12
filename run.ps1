$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$Python = "C:\Users\lenovopc\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Question = $args -join " "

if (-not $Question.Trim()) {
    $Question = "label missing production date"
}

$Script = Join-Path $ProjectRoot "foodsafety_agent.py"
& $Python $Script $Question
