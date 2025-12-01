<# Quick setup for Windows PowerShell #>

$pythonCandidates = @("python3.14", "python3", "python")
$python = $null

foreach ($candidate in $pythonCandidates) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $python = $candidate
        break
    }
}

if (-not $python) {
    Write-Error "python3.14 or python is required in PATH."
    exit 1
}

Write-Host "Using Python interpreter: $python"
& $python -m venv .venv
. ".\\.venv\\Scripts\\Activate.ps1"
python -m pip install --upgrade pip
pip install -e .

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env (add your GEMINI_API_KEY or GOOGLE_API_KEY)."
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "Next steps:"
Write-Host "  .\\.venv\\Scripts\\Activate.ps1"
Write-Host "  python assistant.py ask -p \"Hello\" -m \"gemini-2.5-flash\""
