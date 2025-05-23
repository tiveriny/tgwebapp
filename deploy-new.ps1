# Deployment script
Write-Host "Starting deployment..." -ForegroundColor Green

git add .
$commitMessage = Read-Host "Enter commit message"
git commit -m $commitMessage
git push

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "Your site: https://tiveriny.github.io/tgwebapp" -ForegroundColor Cyan
Write-Host "Changes will be available in 1-2 minutes" -ForegroundColor Yellow

$openSite = Read-Host "Open site? (y/n)"
if ($openSite -eq 'y') {
    Start-Process "https://tiveriny.github.io/tgwebapp"
} 