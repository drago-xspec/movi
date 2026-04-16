@echo off
REM CineBook - Windows Setup Script
REM This script automates the setup process on Windows

echo ==================================
echo 🎬 CineBook Installation Script (Windows)
echo ==================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    echo    Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python %python_version% found
echo.

REM Check MongoDB
echo Checking MongoDB installation...
mongod --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  MongoDB doesn't appear to be installed.
    echo    Download from: https://www.mongodb.com/try/download/community
    echo    Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo ✅ MongoDB found
)
echo.

REM Create virtual environment
echo Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully
echo.

REM Copy environment file
echo Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo ✅ .env file created (please review and update if needed)
) else (
    echo ✅ .env file already exists
)
echo.

REM Optional: Seed database
echo Attempting to connect to MongoDB...
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000).server_info()" 2>nul
if errorlevel 1 (
    echo ⚠️  MongoDB connection failed
    echo    Make sure MongoDB is running: mongod
    echo    You can seed the database later
) else (
    echo ✅ MongoDB is running
    echo.
    echo Seeding database with sample data...
    python seed_db.py
    if errorlevel 1 (
        echo ⚠️  Database seeding might have failed
    ) else (
        echo ✅ Database seeded successfully
    )
)
echo.

echo ==================================
echo ✅ Setup Complete!
echo ==================================
echo.
echo To start the application:
echo.
echo 1. Make sure MongoDB is running
echo    - Open Command Prompt and run: mongod
echo.
echo 2. Start Flask backend (Terminal 1)
echo    - Run: python app.py
echo.
echo 3. Serve frontend (Terminal 2)
echo    - Run: python -m http.server 8000
echo.
echo 4. Open in browser:
echo    - Navigate to: http://localhost:8000/index.html
echo.
echo 📖 Documentation:
echo    - Quick Start: QUICK_START.md
echo    - Full Docs: README.md
echo    - Features: FEATURES.md
echo.
echo ==================================
echo.
pause
