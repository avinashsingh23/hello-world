# 🚀 Concertiv Travel Ops Portal - Local Setup Guide

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8+** installed on your machine
- **pip** (Python package installer)
- **Git** (optional, for cloning)

## 🛠️ Step-by-Step Local Installation

### Step 1: Download the Project Files

**Option A: Download Files Directly**
Copy all the files from the `/workspace` directory to your local machine:

```
concertiv-portal/
├── app.py                    # Main Flask application
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── demo.py                  # Demo script
├── interact.py              # Interactive test script
├── templates/               # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── tmcs.html
│   ├── add_tmc.html
│   ├── edit_tmc.html
│   ├── create_cycle.html
│   └── hotel_audit.html
├── static/                  # CSS and JS files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md
```

**Option B: Create Project Structure**
1. Create a new folder: `mkdir concertiv-portal`
2. Navigate to it: `cd concertiv-portal`
3. Copy all the files from this workspace

### Step 2: Set Up Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

If you encounter any issues, install packages individually:
```bash
pip install Flask>=2.3.0
pip install Flask-SQLAlchemy>=3.0.0
pip install Flask-Migrate>=4.0.0
pip install pandas>=2.0.0
pip install openpyxl>=3.1.0
pip install xlrd>=2.0.0
pip install APScheduler>=3.10.0
pip install Werkzeug>=2.3.0
pip install requests
```

### Step 4: Initialize the Database

```bash
# Initialize database with sample data
python init_db.py
```

You should see:
```
✅ Database tables created
✅ Created 13 TMCs and 10 hotel audit records
🚀 Database initialization complete!
```

### Step 5: Run the Application

```bash
# Start the Flask application
python app.py
```

You should see:
```
🚀 Starting Concertiv Travel Ops Portal...
📍 Server will be accessible at: http://0.0.0.0:5000
🌐 External access: Check your environment's port forwarding
✨ Application loaded with 13 TMCs and sample data
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### Step 6: Access the Application

Open your web browser and go to:
**http://localhost:5000**

## 🎯 What You'll See

### Dashboard (http://localhost:5000/)
- **KPI Cards**: 13 Total Requests, 0 Received, 13 Pending
- **Action Buttons**: Send All, Follow-up, Scan Mailbox
- **Status Table**: All TMCs with request status
- **Attachments Table**: File processing results

### TMC Management (http://localhost:5000/tmcs)
- **13 Pre-loaded TMCs**: American Express, BCD Travel, etc.
- **Add/Edit/Delete**: Full CRUD operations
- **Contact Management**: Email addresses and preferences

### Create Cycle (http://localhost:5000/create_cycle)
- **Monthly Selection**: Choose target month
- **Request Generation**: Creates requests for all active TMCs
- **Duplicate Prevention**: Prevents multiple cycles per month

### Hotel Audit (http://localhost:5000/hotel_audit)
- **Savings Summary**: $570 total savings, $142.50 gain-share
- **Top Hotels**: Ranked by savings amount
- **File Upload**: Process Excel/CSV hotel data
- **Rate Calculations**: Automatic best rate and savings computation

## 🧪 Test the Application

### Quick Test Script
```bash
# Run the interactive test
python interact.py
```

### Demo Script
```bash
# Run the demo to see data
python demo.py
```

## ⚙️ Configuration (Optional)

### Email Integration
To enable email functionality, set environment variables:

**Windows:**
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-app-password
```

**macOS/Linux:**
```bash
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-app-password"
```

### Gmail Setup for Email Features
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Google Account → Security → 2-Step Verification → App passwords
3. Use the generated password as MAIL_PASSWORD

## 🔧 Troubleshooting

### Common Issues:

**1. Port Already in Use**
```bash
# Kill any process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

**2. Python Module Not Found**
```bash
# Make sure virtual environment is activated
# Re-install requirements
pip install -r requirements.txt
```

**3. Database Issues**
```bash
# Delete and recreate database
rm concertiv_portal.db
python init_db.py
```

**4. Permission Errors**
```bash
# Run with appropriate permissions
# On Windows: Run as Administrator
# On macOS/Linux: Use sudo if needed
```

## 📁 Project Structure

```
concertiv-portal/
├── app.py                    # Main Flask application (560 lines)
├── init_db.py               # Database setup with sample data
├── requirements.txt         # Python dependencies
├── concertiv_portal.db      # SQLite database (auto-created)
├── uploads/                 # File upload directory (auto-created)
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── dashboard.html      # Main dashboard with KPIs
│   ├── tmcs.html           # TMC listing page
│   ├── add_tmc.html        # Add TMC form
│   ├── edit_tmc.html       # Edit TMC form
│   ├── create_cycle.html   # Monthly cycle creation
│   └── hotel_audit.html    # Hotel audit and savings
└── static/                  # Static assets
    ├── css/
    │   └── style.css       # Custom styles (300+ lines)
    └── js/
        └── app.js          # JavaScript functionality (400+ lines)
```

## 🎉 Success Confirmation

When everything is working, you should be able to:

1. ✅ **Access all pages** without errors
2. ✅ **Add/Edit TMCs** through the interface
3. ✅ **Create monthly cycles** and see requests generated
4. ✅ **Upload hotel data** and see savings calculated
5. ✅ **Navigate smoothly** between all sections
6. ✅ **See responsive design** on different screen sizes

## 🚀 You're Ready!

The Concertiv Travel Ops Portal is now running locally on your machine with:
- **13 pre-loaded TMCs**
- **Sample hotel audit data**
- **All features fully functional**
- **Modern, responsive interface**

**Access URL**: http://localhost:5000

Enjoy exploring your fully functional travel operations portal! 🎉