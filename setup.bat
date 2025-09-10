@echo off
echo 🚀 Concertiv Travel Ops Portal - Windows Setup
echo ===============================================

echo.
echo 📋 Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Error creating virtual environment
    echo Please make sure Python is installed and in your PATH
    pause
    exit /b 1
)

echo.
echo 📋 Step 2: Activating virtual environment...
call venv\Scripts\activate

echo.
echo 📋 Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error installing dependencies
    echo Trying individual packages...
    pip install Flask Flask-SQLAlchemy Flask-Migrate pandas openpyxl xlrd APScheduler Werkzeug requests
)

echo.
echo 📋 Step 4: Initializing database...
python init_db.py
if errorlevel 1 (
    echo ❌ Error initializing database
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 🌐 To start the application:
echo    1. Run: venv\Scripts\activate
echo    2. Run: python app.py
echo    3. Open: http://localhost:5000
echo.
echo 🎯 Or run start.bat to launch automatically
pause