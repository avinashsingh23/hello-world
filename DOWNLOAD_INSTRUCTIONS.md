# 📦 Download Concertiv Travel Ops Portal to Your Local Machine

## 🎯 Quick Start Guide

### Step 1: Download All Files
Copy these files from the workspace to your local machine:

**📁 Main Files:**
- `app.py` - Main Flask application (560 lines)
- `requirements.txt` - Python dependencies
- `init_db.py` - Database initialization script
- `README.md` - Complete documentation
- `LOCAL_SETUP_GUIDE.md` - This setup guide

**📁 Templates Folder (`templates/`):**
- `base.html` - Base template with navigation
- `dashboard.html` - Main dashboard with KPIs
- `tmcs.html` - TMC management page
- `add_tmc.html` - Add TMC form
- `edit_tmc.html` - Edit TMC form
- `create_cycle.html` - Monthly cycle creation
- `hotel_audit.html` - Hotel audit and savings

**📁 Static Files Folder (`static/`):**
- `static/css/style.css` - Custom styles (300+ lines)
- `static/js/app.js` - JavaScript functionality (400+ lines)

**📁 Setup Scripts:**
- `setup.bat` - Windows setup script
- `setup.sh` - Linux/macOS setup script
- `start.bat` - Windows start script
- `start.sh` - Linux/macOS start script

**📁 Utility Scripts:**
- `demo.py` - Demo script to show functionality
- `interact.py` - Interactive test script

## 🚀 Installation Methods

### Method 1: Automated Setup (Recommended)

**Windows Users:**
1. Download all files to a folder (e.g., `C:\concertiv-portal\`)
2. Double-click `setup.bat`
3. When setup completes, double-click `start.bat`
4. Open http://localhost:5000 in your browser

**Linux/macOS Users:**
1. Download all files to a folder (e.g., `~/concertiv-portal/`)
2. Open terminal in that folder
3. Run: `./setup.sh`
4. Run: `./start.sh`
5. Open http://localhost:5000 in your browser

### Method 2: Manual Setup

1. **Create project folder:**
   ```bash
   mkdir concertiv-portal
   cd concertiv-portal
   ```

2. **Set up virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python init_db.py
   ```

5. **Start application:**
   ```bash
   python app.py
   ```

6. **Access application:**
   Open http://localhost:5000

## 📋 File Structure After Download

```
concertiv-portal/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies  
├── init_db.py               # Database initialization
├── setup.bat                # Windows setup script
├── setup.sh                 # Linux/macOS setup script
├── start.bat                # Windows start script
├── start.sh                 # Linux/macOS start script
├── demo.py                  # Demo script
├── interact.py              # Test script
├── README.md                # Documentation
├── LOCAL_SETUP_GUIDE.md     # Setup instructions
├── templates/               # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── tmcs.html
│   ├── add_tmc.html
│   ├── edit_tmc.html
│   ├── create_cycle.html
│   └── hotel_audit.html
└── static/                  # CSS and JavaScript
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## ✅ What You'll Get

### 🎯 Fully Functional Application
- **Modern web interface** with Bootstrap 5
- **13 pre-loaded TMCs** (American Express, BCD Travel, etc.)
- **Hotel audit data** with $570 in calculated savings
- **All CRUD operations** working
- **File upload functionality**
- **Responsive mobile design**

### 📊 Sample Data Included
- **13 Travel Management Companies**
- **13 pending data requests** for current month
- **10 hotel records** with rate comparisons
- **Realistic business data** for testing

### 🔧 Ready-to-Use Features
- ✅ Dashboard with live KPIs
- ✅ TMC management (add/edit/delete)
- ✅ Monthly cycle creation
- ✅ Hotel audit with savings calculation
- ✅ Excel/CSV file processing
- ✅ Email integration (with SMTP setup)
- ✅ Automated follow-up system
- ✅ Status tracking and reporting

## 🎉 Success Indicators

When everything is working correctly:
1. ✅ Application starts without errors
2. ✅ Browser opens to http://localhost:5000
3. ✅ Dashboard shows 13 total requests
4. ✅ TMC page lists 13 companies
5. ✅ Hotel audit shows $570 savings
6. ✅ All navigation links work
7. ✅ Forms submit successfully

## 🆘 Need Help?

If you encounter issues:
1. Check Python is installed (3.8+)
2. Ensure pip is available
3. Try running setup scripts as administrator
4. Check the LOCAL_SETUP_GUIDE.md for troubleshooting

## 📞 Technical Support

The application includes:
- Comprehensive error handling
- Detailed logging
- User-friendly error messages
- Sample data for testing
- Complete documentation

---

**🎯 Download all files and run the setup script to get started!**

The Concertiv Travel Ops Portal will be running locally on your machine in minutes! 🚀