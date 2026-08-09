@echo off
color 0E
title 🔍 CHECK - Leave Management System Status

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🔍  SERVICE STATUS CHECK                               ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📊 Checking Services...
echo.

echo 🔍 Django Server:
netstat -ano | findstr :8000 >nul
if %errorlevel%==0 (
    echo    ✅ RUNNING on port 8000
) else (
    echo    ❌ NOT RUNNING
)

echo.
echo 🔍 Celery Worker:
tasklist /fi "windowtitle eq ⚡ Celery Worker*" | findstr python >nul
if %errorlevel%==0 (
    echo    ✅ RUNNING
) else (
    echo    ❌ NOT RUNNING
)

echo.
echo 🔍 Celery Beat:
tasklist /fi "windowtitle eq ⏰ Celery Beat*" | findstr python >nul
if %errorlevel%==0 (
    echo    ✅ RUNNING
) else (
    echo    ❌ NOT RUNNING (optional)
)

echo.
echo 🔍 Active Python Processes:
tasklist /fi "imagename eq python.exe" | findstr python

echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause >nul