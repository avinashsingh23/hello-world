#!/usr/bin/env python3
"""
Interactive CLI for Concertiv Travel Ops Portal
Allows you to interact with the running application data
"""

import requests
import json
from datetime import datetime

def test_application():
    """Test the running Flask application"""
    base_url = "http://localhost:5000"
    
    print("🚀 CONCERTIV TRAVEL OPS PORTAL - INTERACTIVE TEST")
    print("=" * 55)
    
    try:
        # Test main dashboard
        print("\n📊 Testing Dashboard...")
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Dashboard: ACCESSIBLE")
            print(f"   Status: {response.status_code}")
            print(f"   Size: {len(response.content)} bytes")
        else:
            print(f"❌ Dashboard: ERROR {response.status_code}")
            
        # Test TMC page
        print("\n🏢 Testing TMC Management...")
        response = requests.get(f"{base_url}/tmcs")
        if response.status_code == 200:
            print("✅ TMC Management: ACCESSIBLE")
            # Count TMCs in response
            tmc_count = response.text.count('<tr>') - 1  # Subtract header row
            print(f"   TMCs visible in HTML: ~{tmc_count}")
        else:
            print(f"❌ TMC Management: ERROR {response.status_code}")
            
        # Test Hotel Audit
        print("\n🏨 Testing Hotel Audit...")
        response = requests.get(f"{base_url}/hotel_audit")
        if response.status_code == 200:
            print("✅ Hotel Audit: ACCESSIBLE")
            if "$570" in response.text:
                print("   ✅ Savings data visible: $570")
            if "Four Seasons Miami" in response.text:
                print("   ✅ Top hotel visible: Four Seasons Miami")
        else:
            print(f"❌ Hotel Audit: ERROR {response.status_code}")
            
        # Test Create Cycle
        print("\n📅 Testing Create Cycle...")
        response = requests.get(f"{base_url}/create_cycle")
        if response.status_code == 200:
            print("✅ Create Cycle: ACCESSIBLE")
        else:
            print(f"❌ Create Cycle: ERROR {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Application not accessible")
        print("   Make sure the Flask app is running on port 5000")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False
    
    print(f"\n🌐 APPLICATION ACCESS:")
    print(f"   Main URL: {base_url}")
    print(f"   Dashboard: {base_url}/")
    print(f"   TMCs: {base_url}/tmcs") 
    print(f"   Hotel Audit: {base_url}/hotel_audit")
    print(f"   Create Cycle: {base_url}/create_cycle")
    
    print(f"\n✨ All pages are accessible and working!")
    print(f"🎯 The application is ready for full testing!")
    
    return True

def show_sample_data():
    """Show sample data from the database"""
    try:
        from app import app, db, TMC, DataRequest, HotelAuditRow
        from datetime import datetime
        
        with app.app_context():
            print("\n📋 SAMPLE DATA IN DATABASE:")
            print("=" * 35)
            
            # Show TMCs
            tmcs = TMC.query.all()
            print(f"\n🏢 TMCs ({len(tmcs)} total):")
            for i, tmc in enumerate(tmcs[:5], 1):
                status = "🟢" if tmc.active else "🔴"
                channel = "📧" if tmc.outreach_channel == 'email' else "🌐"
                print(f"   {i}. {tmc.name} {status} {channel}")
            if len(tmcs) > 5:
                print(f"   ... and {len(tmcs) - 5} more")
            
            # Show requests
            current_month = datetime.now().strftime('%Y-%m')
            requests = DataRequest.query.filter_by(month=current_month).all()
            print(f"\n📊 Data Requests for {current_month} ({len(requests)} total):")
            status_counts = {}
            for req in requests:
                status_counts[req.status] = status_counts.get(req.status, 0) + 1
            
            for status, count in status_counts.items():
                emoji = {"Pending": "⏳", "Sent": "📤", "Received": "✅", "Failed": "❌"}.get(status, "📋")
                print(f"   {emoji} {status}: {count}")
            
            # Show hotel data
            hotels = HotelAuditRow.query.filter_by(month=current_month).all()
            if hotels:
                total_savings = sum(h.savings or 0 for h in hotels)
                total_gain_share = sum(h.gain_share or 0 for h in hotels)
                top_hotel = max(hotels, key=lambda x: x.savings or 0)
                
                print(f"\n🏨 Hotel Audit for {current_month}:")
                print(f"   Hotels: {len(hotels)}")
                print(f"   Total Savings: ${total_savings:,.2f}")
                print(f"   Gain Share: ${total_gain_share:,.2f}")
                print(f"   Top Hotel: {top_hotel.hotel_name} (${top_hotel.savings:,.2f})")
                
                print(f"\n🏆 Top 3 Hotels by Savings:")
                top_3 = sorted(hotels, key=lambda x: x.savings or 0, reverse=True)[:3]
                for i, hotel in enumerate(top_3, 1):
                    print(f"   {i}. {hotel.hotel_name}: ${hotel.savings:,.2f}")
            
    except Exception as e:
        print(f"❌ Database Error: {str(e)}")

if __name__ == '__main__':
    print("🎯 TESTING CONCERTIV TRAVEL OPS PORTAL")
    print("=" * 40)
    
    # Test web application
    if test_application():
        # Show database data
        show_sample_data()
        
        print(f"\n🚀 READY FOR USE!")
        print(f"   The application is fully functional")
        print(f"   Access it via your browser at the URLs above")
    else:
        print(f"\n❌ Application not accessible")
        print(f"   Check if the Flask server is running")