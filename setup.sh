#!/bin/bash
echo "🚀 Concertiv Travel Ops Portal - Linux/macOS Setup"
echo "================================================="

echo ""
echo "📋 Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Error creating virtual environment"
    echo "Please make sure Python 3 is installed"
    exit 1
fi

echo ""
echo "📋 Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📋 Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error installing dependencies"
    echo "Trying individual packages..."
    pip install Flask Flask-SQLAlchemy Flask-Migrate pandas openpyxl xlrd APScheduler Werkzeug requests
fi

echo ""
echo "📋 Step 4: Initializing database..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "❌ Error initializing database"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 To start the application:"
echo "   1. Run: source venv/bin/activate"
echo "   2. Run: python app.py"
echo "   3. Open: http://localhost:5000"
echo ""
echo "🎯 Or run ./start.sh to launch automatically"