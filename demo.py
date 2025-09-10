#!/usr/bin/env python3
"""
Demo script for Concertiv Travel Ops Portal
Shows key functionality working
"""

from app import app, db, TMC, DataRequest, HotelAuditRow
from datetime import datetime
import uuid

def demo_functionality():
    """Demonstrate key portal functionality"""
    with app.app_context():
        print("🚀 Concertiv Travel Ops Portal Demo")
        print("=" * 50)
        
        # Show TMCs
        tmcs = TMC.query.all()
        print(f"\n📋 TMCs in system: {len(tmcs)}")
        for tmc in tmcs[:5]:  # Show first 5
            status = "🟢 Active" if tmc.active else "🔴 Inactive"
            channel = "📧 Email" if tmc.outreach_channel == 'email' else "🌐 Portal"
            print(f"  • {tmc.name} ({channel}) - {status}")
        if len(tmcs) > 5:
            print(f"  ... and {len(tmcs) - 5} more")
        
        # Create a sample monthly cycle
        current_month = datetime.now().strftime('%Y-%m')
        print(f"\n📅 Creating monthly cycle for {current_month}")
        
        # Check if cycle exists
        existing_requests = DataRequest.query.filter_by(month=current_month).count()
        if existing_requests == 0:
            # Create requests for active TMCs
            active_tmcs = TMC.query.filter_by(active=True).all()
            created_count = 0
            
            for tmc in active_tmcs:
                request_id = f"REQ-{current_month}-{tmc.id}-{uuid.uuid4().hex[:8]}"
                data_request = DataRequest(
                    request_id=request_id,
                    tmc_id=tmc.id,
                    month=current_month,
                    status='Pending'
                )
                db.session.add(data_request)
                created_count += 1
            
            db.session.commit()
            print(f"✅ Created {created_count} data requests")
        else:
            print(f"ℹ️  Monthly cycle already exists with {existing_requests} requests")
        
        # Show request status
        requests = DataRequest.query.filter_by(month=current_month).all()
        status_counts = {}
        for req in requests:
            status_counts[req.status] = status_counts.get(req.status, 0) + 1
        
        print(f"\n📊 Request Status Summary:")
        for status, count in status_counts.items():
            emoji = {"Pending": "⏳", "Sent": "📤", "Received": "✅", "Failed": "❌"}.get(status, "📋")
            print(f"  {emoji} {status}: {count}")
        
        # Show hotel audit data
        hotel_data = HotelAuditRow.query.filter_by(month=current_month).all()
        if hotel_data:
            total_savings = sum(row.savings or 0 for row in hotel_data)
            total_gain_share = sum(row.gain_share or 0 for row in hotel_data)
            
            print(f"\n🏨 Hotel Audit Summary ({current_month}):")
            print(f"  📈 Hotels audited: {len(hotel_data)}")
            print(f"  💰 Total savings: ${total_savings:,.2f}")
            print(f"  📊 Gain share (25%): ${total_gain_share:,.2f}")
            
            # Show top 3 hotels by savings
            top_hotels = sorted(hotel_data, key=lambda x: x.savings or 0, reverse=True)[:3]
            print(f"  🏆 Top hotels by savings:")
            for i, hotel in enumerate(top_hotels, 1):
                print(f"    {i}. {hotel.hotel_name}: ${hotel.savings:,.2f}")
        else:
            print(f"\n🏨 No hotel audit data found for {current_month}")
        
        print(f"\n🌐 Portal Access:")
        print(f"  URL: http://localhost:5000")
        print(f"  Dashboard: http://localhost:5000/")
        print(f"  TMC Management: http://localhost:5000/tmcs")
        print(f"  Hotel Audit: http://localhost:5000/hotel_audit")
        
        print(f"\n✨ Key Features Available:")
        print(f"  ✅ TMC Management (Add/Edit/Delete)")
        print(f"  ✅ Monthly Cycle Creation")
        print(f"  ✅ Email Request Sending (with SMTP config)")
        print(f"  ✅ Automated Follow-up System")
        print(f"  ✅ Mailbox Ingestion (with IMAP config)")
        print(f"  ✅ Excel/CSV File Processing")
        print(f"  ✅ Hotel Rate Audit & Savings Calculation")
        print(f"  ✅ Real-time Dashboard with KPIs")
        print(f"  ✅ Status Tracking & Reporting")
        
        print(f"\n📧 Email Configuration Required:")
        print(f"  Set MAIL_USERNAME and MAIL_PASSWORD environment variables")
        print(f"  Example: export MAIL_USERNAME='your-email@gmail.com'")
        print(f"  Example: export MAIL_PASSWORD='your-app-password'")
        
        print(f"\n🎯 Next Steps:")
        print(f"  1. Configure email settings for full functionality")
        print(f"  2. Access the web portal at http://localhost:5000")
        print(f"  3. Create a monthly cycle and send requests")
        print(f"  4. Upload hotel data for audit analysis")
        print(f"  5. Monitor progress via the dashboard")

if __name__ == '__main__':
    demo_functionality()