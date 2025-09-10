@echo off
echo 🚀 Starting Concertiv Travel Ops Portal...
echo =========================================

echo.
echo 📋 Activating virtual environment...
call venv\Scripts\activate

echo.
echo 🌐 Starting Flask application...
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py