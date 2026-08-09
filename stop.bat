@echo off
color 0C
title 🔴 STOP - Leave Management System

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🔴  STOPPING ALL SERVICES                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔄 Stopping all Python/Celery processes...
taskkill /f /im python.exe /fi "windowtitle eq 🖥️  Django Server*" 2>nul
taskkill /f /im python.exe /fi "windowtitle eq ⚡ Celery Worker*" 2>nul
taskkill /f /im celery.exe 2>nul

echo ✅ All services stopped!
echo.
echo 💡 You can now close this window.
pause >nul