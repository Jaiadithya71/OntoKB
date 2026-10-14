# Script to build Docker image and export it as a tar file inside the project folder
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "==> Checking Docker daemon status..." -ForegroundColor Cyan
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker engine not responding"
    }
} catch {
    Write-Warning "Docker daemon is not running."
    Write-Host "Please start Docker Desktop from your Windows Start Menu, wait until it says 'Engine running', and re-run this script." -ForegroundColor Yellow
    exit 1
}

$ImageName = "ontokb:latest"
$OutputTar = Join-Path $PSScriptRoot "ontokb-latest.tar"

Write-Host "==> Building Docker image: $ImageName..." -ForegroundColor Cyan
docker build -t $ImageName -f Dockerfile .
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed."
    exit $LASTEXITCODE
}

Write-Host "==> Docker image '$ImageName' built successfully!" -ForegroundColor Green

Write-Host "==> Saving Docker image to '$OutputTar'..." -ForegroundColor Cyan
docker save -o $OutputTar $ImageName
if ($LASTEXITCODE -eq 0) {
    $sizeMB = [math]::Round(((Get-Item $OutputTar).Length / 1MB), 2)
    Write-Host "==> Export complete! Image tarball stored at: $OutputTar ($sizeMB MB)" -ForegroundColor Green
    Write-Host "You can load this image on any machine with: docker load -i docker/ontokb-latest.tar" -ForegroundColor Magenta
} else {
    Write-Error "Failed to export image archive."
}
