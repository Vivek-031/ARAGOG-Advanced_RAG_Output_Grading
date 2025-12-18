# Fix Medical QA Checkpoints Folder Structure
# This script moves nested folders to the correct location

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "🔧 FIXING MEDICAL QA FOLDER STRUCTURE" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan

$baseDir = "medical_qa_checkpoints"
$nestedDir = Join-Path $baseDir "medical_qa_checkpoints"
$targetDir = $baseDir

# Check if nested structure exists
if (Test-Path (Join-Path $nestedDir "medical_qa_v1.0")) {
    Write-Host "`n⚠️  Nested structure detected" -ForegroundColor Yellow
    Write-Host "Moving files from: $nestedDir" -ForegroundColor Yellow
    Write-Host "To: $targetDir" -ForegroundColor Yellow
    
    # Move medical_qa_v1.0 folder
    $source = Join-Path $nestedDir "medical_qa_v1.0"
    $dest = Join-Path $targetDir "medical_qa_v1.0"
    
    if (Test-Path $dest) {
        Write-Host "`n⚠️  Target already exists, removing..." -ForegroundColor Yellow
        Remove-Item $dest -Recurse -Force
    }
    
    Write-Host "`n📦 Moving medical_qa_v1.0..." -ForegroundColor Cyan
    Move-Item -Path $source -Destination $dest -Force
    Write-Host "✅ Moved medical_qa_v1.0" -ForegroundColor Green
    
    # Move version_log.txt if exists
    $versionLog = Join-Path $nestedDir "version_log.txt"
    if (Test-Path $versionLog) {
        Write-Host "📦 Moving version_log.txt..." -ForegroundColor Cyan
        Move-Item -Path $versionLog -Destination $targetDir -Force
        Write-Host "✅ Moved version_log.txt" -ForegroundColor Green
    }
    
    # Remove empty nested folder
    if (Test-Path $nestedDir) {
        $remaining = Get-ChildItem $nestedDir
        if ($remaining.Count -eq 0) {
            Write-Host "`n🗑️  Removing empty nested folder..." -ForegroundColor Cyan
            Remove-Item $nestedDir -Recurse -Force
            Write-Host "✅ Cleaned up" -ForegroundColor Green
        } else {
            Write-Host "`n⚠️  Nested folder still contains files:" -ForegroundColor Yellow
            $remaining | ForEach-Object { Write-Host "   - $($_.Name)" -ForegroundColor Yellow }
        }
    }
    
    Write-Host "`n" + "="*70 -ForegroundColor Green
    Write-Host "✅ FOLDER STRUCTURE FIXED!" -ForegroundColor Green
    Write-Host "="*70 -ForegroundColor Green
    
} elseif (Test-Path (Join-Path $targetDir "medical_qa_v1.0")) {
    Write-Host "`n✅ Folder structure is already correct!" -ForegroundColor Green
} else {
    Write-Host "`n❌ medical_qa_v1.0 folder not found!" -ForegroundColor Red
    Write-Host "Please check your download." -ForegroundColor Red
    exit 1
}

# Verify structure
Write-Host "`n📋 VERIFICATION:" -ForegroundColor Cyan
$requiredPaths = @(
    "medical_qa_checkpoints\medical_qa_v1.0\metadata.json",
    "medical_qa_checkpoints\medical_qa_v1.0\moe_router.pt",
    "medical_qa_checkpoints\medical_qa_v1.0\faiss_indexes",
    "medical_qa_checkpoints\src\medical_qa_inference.py",
    "medical_qa_checkpoints\src\medical_qa_conversation.py"
)

$allGood = $true
foreach ($path in $requiredPaths) {
    if (Test-Path $path) {
        Write-Host "✅ $path" -ForegroundColor Green
    } else {
        Write-Host "❌ $path" -ForegroundColor Red
        $allGood = $false
    }
}

if ($allGood) {
    Write-Host "`n🎉 All files in correct location!" -ForegroundColor Green
    Write-Host "You can now run: python app.py" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️  Some files are still missing!" -ForegroundColor Yellow
}
