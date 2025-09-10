# Concertiv Travel Ops Portal

A comprehensive web application for managing monthly travel data collection from Travel Management Companies (TMCs) and performing hotel price audits with savings calculations.

## Features

### Core Functionality
- **Monthly Travel Data Collection**: Automated email-based data requests to 13+ TMCs
- **Request Tracking**: End-to-end status monitoring with automated follow-ups
- **Mailbox Integration**: Automatic ingestion of Excel/CSV attachments from email replies
- **Dashboard Analytics**: Real-time KPIs and status reporting
- **Hotel Audit System**: Rate comparison and savings calculation with 25% gain-share

### Key Capabilities
- ✅ Send templated data-request emails to TMCs
- ✅ Track request status (Pending, Sent, Received, Failed)
- ✅ Automated 48-hour follow-up system
- ✅ Excel/CSV attachment parsing and validation
- ✅ Comprehensive dashboard with metrics and tables
- ✅ Hotel rate audit with savings calculations
- ✅ TMC management (add, edit, delete, activate/deactivate)
- ✅ Monthly cycle creation and management
- ✅ Real-time status updates and notifications

## Quick Start

### Prerequisites
- Python 3.8+
- Gmail account with App Password (for email functionality)

### Installation

1. **Clone and setup the project:**
   ```bash
   cd /workspace
   pip install -r requirements.txt
   ```

2. **Configure email settings:**
   ```bash
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   ```

3. **Initialize the database:**
   ```bash
   python init_db.py
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the portal:**
   Open http://localhost:5000 in your browser

## Usage Guide

### 1. TMC Management
- Navigate to **TMCs** to manage your Travel Management Companies
- Add new TMCs with contact information and outreach preferences
- Set TMCs as active/inactive to control which ones receive requests

### 2. Monthly Cycle Creation
- Go to **Create Cycle** to start a new monthly data collection
- Select the target month
- System creates requests for all active TMCs automatically

### 3. Sending Data Requests
- From the **Dashboard**, click "Send All Requests" for your selected month
- System sends templated emails to all TMC contacts
- Each request gets a unique tracking ID for reply matching

### 4. Monitoring Progress
- **Dashboard** shows real-time KPIs:
  - Total Requests
  - Received
  - Pending
  - Follow-ups Sent
  - Overdue count
- Status table shows per-TMC progress with timestamps
- Attachments table displays received files with parsing status

### 5. Automated Follow-ups
- System automatically sends follow-up emails 48 hours after initial request
- Manual follow-ups available via "Follow-up Overdue" button
- Follow-up counter tracks escalation attempts

### 6. Mailbox Integration
- Click "Scan Mailbox" to manually check for new replies
- System automatically scans every 10 minutes
- Excel/CSV attachments are automatically processed and linked to requests

### 7. Hotel Audit & Savings
- Navigate to **Hotel Audit** for Phase 2 functionality
- Upload Excel/CSV files with hotel rate data
- System calculates:
  - Best Available Rate (min of TMC and public rates)
  - Savings (Best Available - Concertiv rate)
  - Gain Share (25% of savings)
- View top performing hotels and total savings metrics

## Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password as `MAIL_PASSWORD`

### Email Templates

**Initial Request:**
```
Subject: Concertiv Monthly Travel Data Request — [Month Year]

Hi [Contact Name],
Kindly share the [Month Year] travel data using the attached template or your standard export.
Requested by: [Due Date]. If already sent, please ignore.

Thank you,
Concertiv Operations
(Reference: REQ-ID: [Request ID])
```

**Follow-up:**
```
Subject: Reminder — Travel Data Request [Month Year] (Pending)

Hi [Contact Name],
Quick reminder: we're awaiting the [Month Year] travel data.
Please reply with the Excel file attached.

Thank you!
```

## Data Formats

### Hotel Audit Upload
Expected columns in Excel/CSV:
- `hotel_name`: Hotel name
- `location`: Hotel location
- `concertiv_rate`: Concertiv negotiated rate
- `tmc_rate`: TMC quoted rate  
- `public_rate`: Public/rack rate

### TMC Data Attachments
- Supports `.xlsx`, `.xls`, and `.csv` files
- Basic validation includes row/column counting
- Parse errors are logged but don't prevent "Received" status

## Architecture

### Backend (Flask)
- **Models**: TMC, DataRequest, Attachment, HotelAuditRow
- **Services**: EmailService for sending and ingesting emails
- **Scheduler**: APScheduler for automated follow-ups and mailbox scanning
- **Database**: SQLite with SQLAlchemy ORM

### Frontend (Bootstrap 5)
- Responsive design with modern UI components
- Real-time updates and interactive dashboards
- Form validation and file upload handling
- Toast notifications and loading states

### Key Components
- **Dashboard**: Main analytics and control center
- **TMC Management**: CRUD operations for travel companies
- **Cycle Management**: Monthly workflow initiation
- **Email Integration**: SMTP sending and IMAP ingestion
- **File Processing**: Excel/CSV parsing with pandas
- **Audit System**: Hotel rate analysis and savings calculation

## Business Rules

1. **One Request Per TMC Per Month**: Prevents duplicate requests
2. **48-Hour Follow-up Window**: Automated escalation timing
3. **Request Status Flow**: Pending → Sent → Received (or Failed)
4. **Attachment Requirement**: Request marked "Received" only with valid file
5. **Overdue Definition**: Past due date without received status
6. **Savings Calculation**: Best Available Rate - Concertiv Rate (if positive)
7. **Gain Share**: 25% of calculated savings

## API Endpoints

- `GET /` - Dashboard with KPIs and tables
- `GET /tmcs` - TMC management interface
- `POST /tmcs/add` - Add new TMC
- `GET|POST /tmcs/<id>/edit` - Edit TMC
- `POST /tmcs/<id>/delete` - Delete TMC
- `GET|POST /create_cycle` - Create monthly cycle
- `GET /send_all/<month>` - Send all requests for month
- `GET /follow_up_overdue/<month>` - Send follow-up emails
- `GET /scan_mailbox` - Manual mailbox scan
- `GET /hotel_audit` - Hotel audit dashboard
- `POST /upload_hotel_data` - Upload hotel rate data

## Deployment

### Production Considerations
1. **Database**: Migrate from SQLite to PostgreSQL/MySQL
2. **Email**: Configure production SMTP server
3. **Security**: Add authentication and authorization
4. **Monitoring**: Implement logging and error tracking
5. **Scaling**: Add Redis for session management and caching

### Environment Variables
```bash
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-secure-password
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
```

## Support

For technical support or feature requests, please refer to the application logs and error messages. The system includes comprehensive error handling and user feedback mechanisms.

## License

Internal use only - Concertiv Travel Operations Portal