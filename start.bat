@echo off
chcp 65001 >nul
title 🚀 Leave Management System - Automation Project
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🚀  LEAVE MANAGEMENT SYSTEM - STARTUP SCRIPT           ║
echo ║                                                              ║
echo ║     Automation Engineer Project - Harri Palestine           ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📂 Changing to project directory...
cd C:\Users\HITECH\automation_project

echo 📦 Activating virtual environment...
call venv\Scripts\activate

echo.
echo ════════════════════════════════════════════════════════════════
echo 📦 Starting Services...
echo ════════════════════════════════════════════════════════════════
echo.

echo [1/3] 🖥️  Starting Django Server on port 8000...
start "🖥️  Django Server" cmd /c "python manage.py runserver"

echo [2/3] ⏳ Waiting for Django to initialize...
timeout /t 3 /nobreak >nul

echo [3/3] ⚡ Starting Celery Worker (Background Tasks)...
start "⚡ Celery Worker" cmd /c "python -m celery -A core worker --pool=solo --loglevel=info"

echo.
echo ════════════════════════════════════════════════════════════════
echo ✅ ALL SERVICES STARTED SUCCESSFULLY!
echo ════════════════════════════════════════════════════════════════
echo.

echo 🌐 URLs:
echo    📊 Admin Panel:  http://127.0.0.1:8000/admin/
echo    📡 API Base:     http://127.0.0.1:8000/api/
echo    📝 API Docs:     http://127.0.0.1:8000/api/
echo    🤖 AI Summary:   http://127.0.0.1:8000/api/leave-requests/summary/
echo.

echo ════════════════════════════════════════════════════════════════
echo 💡 TIPS:
echo    - Use Ctrl+C in each window to stop a service
echo    - Or close the command prompt windows
echo    - All services run in separate windows
echo ════════════════════════════════════════════════════════════════

echo.
echo 🟢 Press any key to keep this window open...
pause >nul