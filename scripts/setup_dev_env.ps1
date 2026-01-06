<#
PowerShell helper to create/activate a venv and install development packages.
Usage (from project root):
  .\scripts\setup_dev_env.ps1
#>
param(
    [string]$VenvPath = ".venv"
)

# Check for uv
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Warning "uv not found. Installing via pip..."
    python -m pip install uv
}

if (-not (Test-Path $VenvPath)) {
    Write-Output "Creating virtual environment at $VenvPath using uv..."
    uv venv $VenvPath
}

Write-Output "Activating virtual environment..."
& "$VenvPath\Scripts\Activate.ps1"

Write-Output "Installing dev requirements with uv..."
uv pip install -e .[dev]

Write-Output "Installing pre-commit hooks..."
python -m pre_commit install || Write-Output "pre-commit install failed; run 'python -m pre_commit install' manually"

Write-Output "Dev environment setup complete. In VSCode select the interpreter: $VenvPath\Scripts\python.exe"