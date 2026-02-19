@echo off
echo ================================
echo    TARO BOT - ЗАПУСК
echo ================================

:: Убиваем старые процессы
echo [1/5] Останавливаем старые процессы...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

:: Запускаем ngrok в фоне
echo [2/5] Запускаем ngrok...
start /min "ngrok" C:\Project\Taro_bot\ngrok.exe http 3000
timeout /t 3 /nobreak >nul

:: Получаем ngrok URL через API
echo [3/5] Получаем ngrok URL...
for /f "delims=" %%i in ('powershell -Command "(Invoke-WebRequest -Uri 'http://localhost:4040/api/tunnels' -UseBasicParsing | ConvertFrom-Json).tunnels[0].public_url"') do set NGROK_URL=%%i

if "%NGROK_URL%"=="" (
    echo ОШИБКА: не удалось получить ngrok URL
    pause
    exit /b 1
)

echo Ngrok URL: %NGROK_URL%

:: Обновляем .env
echo [4/5] Обновляем .env...
echo BOT_TOKEN=8566471637:AAEwsGbUq3AMbEDnnJPRD_It5gXTFGAD5Lc> .env
echo WEBAPP_URL=%NGROK_URL%>> .env

:: Запускаем WebApp сервер
echo [5/5] Запускаем WebApp сервер и бота...
start /min "WebApp Server" cmd /c "cd webapp\server && node index.js"
timeout /t 2 /nobreak >nul

:: Запускаем бота
start "Taro Bot" cmd /c "python bot.py"

echo.
echo ================================
echo  ВСЁ ЗАПУЩЕНО!
echo  Ngrok: %NGROK_URL%
echo ================================
echo.
pause
