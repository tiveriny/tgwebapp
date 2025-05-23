# Проверяем наличие изменений
$changes = git status --porcelain
if ($changes) {
    Write-Host "Обнаружены изменения в файлах:"
    Write-Host $changes

    # Запрашиваем сообщение коммита
    $commitMessage = Read-Host "Введите сообщение коммита"
    if (-not $commitMessage) {
        $commitMessage = "Update web app"
    }

    # Добавляем все изменения
    git add .

    # Создаем коммит
    git commit -m $commitMessage

    # Отправляем изменения в репозиторий
    git push origin main

    Write-Host "`nИзменения успешно отправлены в репозиторий."
    Write-Host "Подождите несколько минут, пока GitHub Pages обновит сайт."
    
    # Спрашиваем, хочет ли пользователь открыть сайт
    $openSite = Read-Host "Хотите открыть сайт? (y/n)"
    if ($openSite -eq "y") {
        Start-Process "https://tiveriny.github.io/tgwebapp"
    }
} else {
    Write-Host "Нет изменений для деплоя."
} 