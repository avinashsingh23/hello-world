#!/usr/bin/env python3
"""
Initialize the database with sample data for the Concertiv Travel Ops Portal
"""

from app import app, db, TMC, DataRequest, Attachment, HotelAuditRow
from datetime import datetime, timedelta
import uuid

def create_sample_data():
    """Create sample TMCs and data for testing"""
    
    # Sample TMCs
    sample_tmcs = [
        {
            'name': 'American Express Global Business Travel',
            'contact_name': 'John Smith',
            'contact_email': 'john.smith@amexgbt.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'BCD Travel',
            'contact_name': 'Sarah Johnson',
            'contact_email': 'sarah.johnson@bcdtravel.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'Carlson Wagonlit Travel',
            'contact_name': 'Mike Wilson',
            'contact_email': 'mike.wilson@carlsonwagonlit.com',
            'outreach_channel': 'portal',
            'active': True
        },
        {
            'name': 'Concur Travel',
            'contact_name': 'Lisa Davis',
            'contact_email': 'lisa.davis@concur.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'Egencia',
            'contact_name': 'David Brown',
            'contact_email': 'david.brown@egencia.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'FCM Travel Solutions',
            'contact_name': 'Jennifer Taylor',
            'contact_email': 'jennifer.taylor@fcm.travel',
            'outreach_channel': 'portal',
            'active': True
        },
        {
            'name': 'Frosch Travel',
            'contact_name': 'Robert Miller',
            'contact_email': 'robert.miller@frosch.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'GBTA',
            'contact_name': 'Amanda White',
            'contact_email': 'amanda.white@gbta.org',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'HRG North America',
            'contact_name': 'Chris Anderson',
            'contact_email': 'chris.anderson@hrgworldwide.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'Travel Leaders Corporate',
            'contact_name': 'Michelle Garcia',
            'contact_email': 'michelle.garcia@travelleaders.com',
            'outreach_channel': 'portal',
            'active': True
        },
        {
            'name': 'TripActions',
            'contact_name': 'Kevin Martinez',
            'contact_email': 'kevin.martinez@tripactions.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'World Travel Inc',
            'contact_name': 'Rachel Thompson',
            'contact_email': 'rachel.thompson@worldtravel.com',
            'outreach_channel': 'email',
            'active': True
        },
        {
            'name': 'Corporate Travel Management',
            'contact_name': 'Daniel Lee',
            'contact_email': 'daniel.lee@ctm.com',
            'outreach_channel': 'email',
            'active': True
        }
    ]
    
    # Create TMCs
    for tmc_data in sample_tmcs:
        tmc = TMC(**tmc_data)
        db.session.add(tmc)
    
    db.session.commit()
    
    # Create sample hotel audit data for current month
    current_month = datetime.now().strftime('%Y-%m')
    
    sample_hotels = [
        {
            'hotel_name': 'Marriott Times Square',
            'location': 'New York, NY',
            'concertiv_rate': 285.00,
            'tmc_rate': 320.00,
            'public_rate': 350.00
        },
        {
            'hotel_name': 'Hilton Chicago',
            'location': 'Chicago, IL',
            'concertiv_rate': 195.00,
            'tmc_rate': 240.00,
            'public_rate': 280.00
        },
        {
            'hotel_name': 'Hyatt Regency San Francisco',
            'location': 'San Francisco, CA',
            'concertiv_rate': 310.00,
            'tmc_rate': 380.00,
            'public_rate': 420.00
        },
        {
            'hotel_name': 'Sheraton Boston Hotel',
            'location': 'Boston, MA',
            'concertiv_rate': 225.00,
            'tmc_rate': 275.00,
            'public_rate': 310.00
        },
        {
            'hotel_name': 'W Hotel Los Angeles',
            'location': 'Los Angeles, CA',
            'concertiv_rate': 340.00,
            'tmc_rate': 410.00,
            'public_rate': 450.00
        },
        {
            'hotel_name': 'Four Seasons Miami',
            'location': 'Miami, FL',
            'concertiv_rate': 395.00,
            'tmc_rate': 480.00,
            'public_rate': 520.00
        },
        {
            'hotel_name': 'Ritz Carlton Atlanta',
            'location': 'Atlanta, GA',
            'concertiv_rate': 275.00,
            'tmc_rate': 330.00,
            'public_rate': 365.00
        },
        {
            'hotel_name': 'Grand Hyatt Seattle',
            'location': 'Seattle, WA',
            'concertiv_rate': 255.00,
            'tmc_rate': 310.00,
            'public_rate': 340.00
        },
        {
            'hotel_name': 'Omni Dallas Hotel',
            'location': 'Dallas, TX',
            'concertiv_rate': 185.00,
            'tmc_rate': 235.00,
            'public_rate': 270.00
        },
        {
            'hotel_name': 'JW Marriott Denver',
            'location': 'Denver, CO',
            'concertiv_rate': 210.00,
            'tmc_rate': 265.00,
            'public_rate': 295.00
        }
    ]
    
    for hotel_data in sample_hotels:
        # Calculate derived fields
        concertiv_rate = hotel_data['concertiv_rate']
        tmc_rate = hotel_data['tmc_rate']
        public_rate = hotel_data['public_rate']
        
        best_available_rate = min(tmc_rate, public_rate)
        savings = max(best_available_rate - concertiv_rate, 0)
        gain_share = savings * 0.25
        
        hotel_audit = HotelAuditRow(
            month=current_month,
            hotel_name=hotel_data['hotel_name'],
            location=hotel_data['location'],
            concertiv_rate=concertiv_rate,
            tmc_rate=tmc_rate,
            public_rate=public_rate,
            best_available_rate=best_available_rate,
            savings=savings,
            gain_share=gain_share
        )
        db.session.add(hotel_audit)
    
    db.session.commit()
    print(f"✅ Created {len(sample_tmcs)} TMCs and {len(sample_hotels)} hotel audit records")

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if data already exists
        if TMC.query.count() == 0:
            create_sample_data()
        else:
            print("ℹ️  Sample data already exists, skipping creation")
        
        print("🚀 Database initialization complete!")
        print("\nYou can now:")
        print("1. Run the application: python app.py")
        print("2. Access the portal at: http://localhost:5000")
        print("3. Create a monthly cycle and start managing travel data requests")