from flask import Flask, render_template, request as flask_request, jsonify, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
import os
import uuid
import smtplib
import imaplib
import email
import email.mime.text
import email.mime.multipart
import pandas as pd
import io
import threading
import time
from werkzeug.utils import secure_filename
import re
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///concertiv_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')

# IMAP configuration for mailbox ingestion
app.config['IMAP_SERVER'] = 'imap.gmail.com'
app.config['IMAP_PORT'] = 993

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class TMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    outreach_channel = db.Column(db.String(20), default='email')  # 'portal' or 'email'
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    data_requests = db.relationship('DataRequest', backref='tmc', lazy=True)

class DataRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), unique=True, nullable=False)
    tmc_id = db.Column(db.Integer, db.ForeignKey('tmc.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    status = db.Column(db.String(20), default='Pending')  # Pending, Sent, Received, Failed
    sent_at = db.Column(db.DateTime)
    due_at = db.Column(db.DateTime)
    received_at = db.Column(db.DateTime)
    follow_up_count = db.Column(db.Integer, default=0)
    last_follow_up_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attachments = db.relationship('Attachment', backref='data_request', lazy=True)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_request_id = db.Column(db.Integer, db.ForeignKey('data_request.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    file_path = db.Column(db.String(500))
    parsed = db.Column(db.Boolean, default=False)
    row_count = db.Column(db.Integer)
    column_count = db.Column(db.Integer)
    parse_error = db.Column(db.Text)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

class HotelAuditRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(7), nullable=False)
    hotel_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    concertiv_rate = db.Column(db.Float)
    tmc_rate = db.Column(db.Float)
    public_rate = db.Column(db.Float)
    best_available_rate = db.Column(db.Float)
    savings = db.Column(db.Float)
    gain_share = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Email Service
class EmailService:
    def __init__(self, app):
        self.app = app
        
    def send_email(self, to_email, subject, body, request_id=None):
        try:
            msg = email.mime.multipart.MIMEMultipart()
            msg['From'] = self.app.config['MAIL_USERNAME']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add request ID to body for tracking
            if request_id:
                body += f"\n\n(Reference: REQ-ID: {request_id})"
            
            msg.attach(email.mime.text.MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.app.config['MAIL_SERVER'], self.app.config['MAIL_PORT'])
            server.starttls()
            server.login(self.app.config['MAIL_USERNAME'], self.app.config['MAIL_PASSWORD'])
            text = msg.as_string()
            server.sendmail(self.app.config['MAIL_USERNAME'], to_email, text)
            server.quit()
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
    
    def scan_mailbox(self):
        try:
            mail = imaplib.IMAP4_SSL(self.app.config['IMAP_SERVER'], self.app.config['IMAP_PORT'])
            mail.login(self.app.config['MAIL_USERNAME'], self.app.config['MAIL_PASSWORD'])
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            for num in messages[0].split():
                status, msg_data = mail.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Extract request ID from email
                request_id = self._extract_request_id(email_message)
                if request_id:
                    self._process_email_attachments(email_message, request_id)
                
                # Mark as read
                mail.store(num, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Mailbox scanning failed: {str(e)}")
    
    def _extract_request_id(self, email_message):
        # Extract request ID from email body or subject
        subject = email_message.get('Subject', '')
        body = self._get_email_body(email_message)
        
        # Look for REQ-ID pattern
        pattern = r'REQ-ID:\s*([A-Z0-9-]+)'
        match = re.search(pattern, body + ' ' + subject)
        if match:
            return match.group(1)
        return None
    
    def _get_email_body(self, email_message):
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8')
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')
        return body
    
    def _process_email_attachments(self, email_message, request_id):
        with self.app.app_context():
            data_request = DataRequest.query.filter_by(request_id=request_id).first()
            if not data_request:
                return
            
            for part in email_message.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename and (filename.endswith('.xlsx') or filename.endswith('.xls') or filename.endswith('.csv')):
                        # Save attachment
                        file_data = part.get_payload(decode=True)
                        safe_filename = secure_filename(filename)
                        file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{request_id}_{safe_filename}")
                        
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        
                        # Create attachment record
                        attachment = Attachment(
                            data_request_id=data_request.id,
                            filename=filename,
                            file_type=filename.split('.')[-1],
                            file_size=len(file_data),
                            file_path=file_path
                        )
                        
                        # Try to parse the file
                        try:
                            if filename.endswith('.csv'):
                                df = pd.read_csv(io.BytesIO(file_data))
                            else:
                                df = pd.read_excel(io.BytesIO(file_data))
                            
                            attachment.parsed = True
                            attachment.row_count = len(df)
                            attachment.column_count = len(df.columns)
                        except Exception as e:
                            attachment.parse_error = str(e)
                        
                        db.session.add(attachment)
                        
                        # Update request status
                        data_request.status = 'Received'
                        data_request.received_at = datetime.utcnow()
                        
                        db.session.commit()

# Initialize email service
email_service = EmailService(app)

# Background scheduler for automated tasks
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def check_follow_ups():
    with app.app_context():
        # Find requests that need follow-up
        now = datetime.utcnow()
        overdue_requests = DataRequest.query.filter(
            DataRequest.status.in_(['Sent', 'Pending']),
            DataRequest.due_at < now,
            DataRequest.status != 'Received'
        ).all()
        
        for request in overdue_requests:
            if not request.last_follow_up_at or (now - request.last_follow_up_at).total_seconds() > 3600:  # 1 hour between follow-ups
                send_follow_up_email(request)

def send_follow_up_email(data_request):
    subject = f"Reminder — Travel Data Request {data_request.month} (Pending)"
    body = f"""Hi {data_request.tmc.contact_name},

Quick reminder: we're awaiting the {data_request.month} travel data.
Please reply with the Excel file attached.

Thank you!
Concertiv Operations"""
    
    success = email_service.send_email(
        data_request.tmc.contact_email,
        subject,
        body,
        data_request.request_id
    )
    
    if success:
        data_request.follow_up_count += 1
        data_request.last_follow_up_at = datetime.utcnow()
        db.session.commit()

# Schedule follow-up checks every hour
scheduler.add_job(func=check_follow_ups, trigger="interval", hours=1)

# Schedule mailbox scanning every 10 minutes
scheduler.add_job(func=email_service.scan_mailbox, trigger="interval", minutes=10)

# Routes
@app.route('/')
def dashboard():
    # Get current month for default selection
    current_month = datetime.now().strftime('%Y-%m')
    selected_month = flask_request.args.get('month', current_month)
    
    # Get KPIs for selected month
    requests = DataRequest.query.filter_by(month=selected_month).all()
    
    total_requests = len(requests)
    received = len([r for r in requests if r.status == 'Received'])
    pending = len([r for r in requests if r.status in ['Pending', 'Sent']])
    follow_ups_sent = sum(r.follow_up_count for r in requests)
    
    now = datetime.utcnow()
    overdue = len([r for r in requests if r.due_at and r.due_at < now and r.status != 'Received'])
    
    # Get status table data
    status_data = []
    for req in requests:
        status_data.append({
            'tmc_name': req.tmc.name,
            'sent_at': req.sent_at,
            'due_at': req.due_at,
            'status': req.status,
            'follow_ups': req.follow_up_count,
            'received_at': req.received_at,
            'notes': req.notes,
            'is_overdue': req.due_at and req.due_at < now and req.status != 'Received'
        })
    
    # Get attachments data
    attachments_data = []
    for req in requests:
        for attachment in req.attachments:
            attachments_data.append({
                'tmc_name': req.tmc.name,
                'request_id': req.request_id,
                'filename': attachment.filename,
                'file_type': attachment.file_type,
                'parsed': attachment.parsed,
                'row_count': attachment.row_count,
                'column_count': attachment.column_count,
                'received_at': attachment.received_at,
                'parse_error': attachment.parse_error
            })
    
    return render_template('dashboard.html',
                         selected_month=selected_month,
                         kpis={
                             'total_requests': total_requests,
                             'received': received,
                             'pending': pending,
                             'follow_ups_sent': follow_ups_sent,
                             'overdue': overdue
                         },
                         status_data=status_data,
                         attachments_data=attachments_data)

@app.route('/tmcs')
def tmcs():
    tmcs = TMC.query.all()
    return render_template('tmcs.html', tmcs=tmcs)

@app.route('/tmcs/add', methods=['GET', 'POST'])
def add_tmc():
    if flask_request.method == 'POST':
        tmc = TMC(
            name=flask_request.form['name'],
            contact_name=flask_request.form['contact_name'],
            contact_email=flask_request.form['contact_email'],
            outreach_channel=flask_request.form['outreach_channel'],
            active=flask_request.form.get('active') == 'on'
        )
        db.session.add(tmc)
        db.session.commit()
        flash('TMC added successfully!', 'success')
        return redirect(url_for('tmcs'))
    
    return render_template('add_tmc.html')

@app.route('/tmcs/<int:tmc_id>/edit', methods=['GET', 'POST'])
def edit_tmc(tmc_id):
    tmc = TMC.query.get_or_404(tmc_id)
    
    if flask_request.method == 'POST':
        tmc.name = flask_request.form['name']
        tmc.contact_name = flask_request.form['contact_name']
        tmc.contact_email = flask_request.form['contact_email']
        tmc.outreach_channel = flask_request.form['outreach_channel']
        tmc.active = flask_request.form.get('active') == 'on'
        db.session.commit()
        flash('TMC updated successfully!', 'success')
        return redirect(url_for('tmcs'))
    
    return render_template('edit_tmc.html', tmc=tmc)

@app.route('/tmcs/<int:tmc_id>/delete', methods=['POST'])
def delete_tmc(tmc_id):
    tmc = TMC.query.get_or_404(tmc_id)
    db.session.delete(tmc)
    db.session.commit()
    flash('TMC deleted successfully!', 'success')
    return redirect(url_for('tmcs'))

@app.route('/create_cycle', methods=['GET', 'POST'])
def create_cycle():
    if flask_request.method == 'POST':
        month = flask_request.form['month']
        
        # Check if cycle already exists for this month
        existing = DataRequest.query.filter_by(month=month).first()
        if existing:
            flash('Monthly cycle already exists for this month!', 'error')
            return redirect(url_for('create_cycle'))
        
        # Create requests for all active TMCs
        active_tmcs = TMC.query.filter_by(active=True).all()
        
        for tmc in active_tmcs:
            request_id = f"REQ-{month}-{tmc.id}-{uuid.uuid4().hex[:8]}"
            data_request = DataRequest(
                request_id=request_id,
                tmc_id=tmc.id,
                month=month,
                status='Pending'
            )
            db.session.add(data_request)
        
        db.session.commit()
        flash(f'Monthly cycle created for {month} with {len(active_tmcs)} requests!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_cycle.html')

@app.route('/send_all/<month>')
def send_all_requests(month):
    requests = DataRequest.query.filter_by(month=month, status='Pending').all()
    
    sent_count = 0
    for request in requests:
        # Format month for display
        month_year = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
        
        subject = f"Concertiv Monthly Travel Data Request — {month_year}"
        body = f"""Hi {request.tmc.contact_name},

Kindly share the {month_year} travel data using the attached template or your standard export.

Requested by: {(datetime.utcnow() + timedelta(days=2)).strftime('%Y-%m-%d')}. If already sent, please ignore.

Thank you,
Concertiv Operations"""
        
        success = email_service.send_email(
            request.tmc.contact_email,
            subject,
            body,
            request.request_id
        )
        
        if success:
            request.status = 'Sent'
            request.sent_at = datetime.utcnow()
            request.due_at = datetime.utcnow() + timedelta(hours=48)
            sent_count += 1
    
    db.session.commit()
    flash(f'Sent {sent_count} data requests successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/follow_up_overdue/<month>')
def follow_up_overdue(month):
    now = datetime.utcnow()
    overdue_requests = DataRequest.query.filter(
        DataRequest.month == month,
        DataRequest.status.in_(['Sent', 'Pending']),
        DataRequest.due_at < now,
        DataRequest.status != 'Received'
    ).all()
    
    follow_up_count = 0
    for request in overdue_requests:
        send_follow_up_email(request)
        follow_up_count += 1
    
    flash(f'Sent {follow_up_count} follow-up emails!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/scan_mailbox')
def scan_mailbox():
    try:
        email_service.scan_mailbox()
        flash('Mailbox scanned successfully!', 'success')
    except Exception as e:
        flash(f'Mailbox scan failed: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/hotel_audit')
def hotel_audit():
    selected_month = flask_request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    # Get hotel audit data for the selected month
    audit_data = HotelAuditRow.query.filter_by(month=selected_month).all()
    
    # Calculate totals
    total_savings = sum(row.savings or 0 for row in audit_data)
    total_gain_share = sum(row.gain_share or 0 for row in audit_data)
    
    # Get top hotels by savings
    top_hotels = sorted(audit_data, key=lambda x: x.savings or 0, reverse=True)[:10]
    
    return render_template('hotel_audit.html',
                         selected_month=selected_month,
                         audit_data=audit_data,
                         total_savings=total_savings,
                         total_gain_share=total_gain_share,
                         top_hotels=top_hotels)

@app.route('/upload_hotel_data', methods=['POST'])
def upload_hotel_data():
    if 'file' not in flask_request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('hotel_audit'))
    
    file = flask_request.files['file']
    month = flask_request.form['month']
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('hotel_audit'))
    
    try:
        # Read the Excel/CSV file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Clear existing data for this month
        HotelAuditRow.query.filter_by(month=month).delete()
        
        # Process each row
        for _, row in df.iterrows():
            # Calculate best available rate and savings
            concertiv_rate = float(row.get('concertiv_rate', 0) or 0)
            tmc_rate = float(row.get('tmc_rate', 0) or 0)
            public_rate = float(row.get('public_rate', 0) or 0)
            
            best_available_rate = min(tmc_rate, public_rate) if tmc_rate and public_rate else (tmc_rate or public_rate or 0)
            savings = max(best_available_rate - concertiv_rate, 0) if best_available_rate and concertiv_rate else 0
            gain_share = savings * 0.25
            
            audit_row = HotelAuditRow(
                month=month,
                hotel_name=row.get('hotel_name', ''),
                location=row.get('location', ''),
                concertiv_rate=concertiv_rate,
                tmc_rate=tmc_rate,
                public_rate=public_rate,
                best_available_rate=best_available_rate,
                savings=savings,
                gain_share=gain_share
            )
            db.session.add(audit_row)
        
        db.session.commit()
        flash(f'Hotel data uploaded successfully for {month}!', 'success')
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
    
    return redirect(url_for('hotel_audit'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)