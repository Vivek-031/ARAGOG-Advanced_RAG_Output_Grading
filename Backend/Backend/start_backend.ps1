# Medical RAG Backend Startup Script

Write-Host "🚀 Starting Medical RAG Backend..." -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} else {
    Write-Host "❌ ERROR: Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Python found: $pythonCmd" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if requirements are installed
Write-Host "📦 Installing/Updating dependencies..." -ForegroundColor Yellow
Write-Host "⏳ This may take 10-30 minutes on first run (downloading ML models)..." -ForegroundColor Yellow
pip install --upgrade pip -q
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "✅ All dependencies installed" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting Flask server on http://localhost:5000..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ First startup will download ML models (~10GB). Please be patient..." -ForegroundColor Yellow
Write-Host ""

# Run the Flask app
python app.py
