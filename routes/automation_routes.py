from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.vendor_model import Vendor
from datetime import datetime
import smtplib
from email.message import EmailMessage

router = APIRouter()

@router.post("/automate/email-blast")
def email_blast(db: Session = Depends(get_db)):
    try:
        # 1. Fetch leads (Limit to 10 for testing to avoid spam blocks)
        targets = db.query(Vendor).filter(
            Vendor.message_count < 3,
            Vendor.email.contains('@')
        ).order_by(Vendor.message_count.asc()).limit(10).all()

        if not targets:
            return {"status": "info", "message": "No pending leads with valid emails found."}

        # 2. SMTP Configuration
        SENDER_EMAIL = "avaenterprisesraipur@gmail.com"
        SENDER_PASSWORD = "zhec xcrw dvnu rkty"  # <-- PUT YOUR 16-DIGIT CODE HERE

        sent_count = 0
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            for lead in targets:
                msg = EmailMessage()
                
                # --- DYNAMIC MESSAGE LOGIC ---
                if lead.message_count == 0:
                    msg['Subject'] = f"Secure Government Orders for {lead.company}"
                    content = f"Hello Team {lead.company},\n\nI noticed you are leading providers of {lead.product}. I can help you with L1 Strategy & Bid Filing on the GeM Portal.\n\nBest,\nAkhilesh Sharma | 8982879443"
                else:
                    msg['Subject'] = f"Follow-up: GeM Tenders for {lead.product}"
                    content = f"Hi {lead.company}, new tenders for {lead.product} are closing soon. Should we discuss the bidding strategy?"

                msg.set_content(content)
                msg['From'] = SENDER_EMAIL
                msg['To'] = lead.email
                
                server.send_message(msg)
                
                # Update Database
                lead.message_count += 1
                lead.last_contacted = datetime.now()
                sent_count += 1
        
        db.commit()
        return {"status": "success", "message": f"Successfully sent {sent_count} proposals!"}
    
    except smtplib.SMTPAuthenticationError:
        return {"status": "error", "message": "Gmail Authentication Failed. Check your App Password."}
    except Exception as e:
        return {"status": "error", "message": f"System Error: {str(e)}"}

@router.post("/automate/whatsapp-blast")
def whatsapp_blast(db: Session = Depends(get_db)):
    # Simulating WhatsApp logic for now
    targets = db.query(Vendor).filter(Vendor.message_count < 3).limit(10).all()
    if not targets:
        return {"status": "info", "message": "No leads available for WhatsApp."}
    
    for lead in targets:
        lead.message_count += 1
        lead.last_contacted = datetime.now()
    
    db.commit()
    return {"status": "success", "message": f"WhatsApp sequence started for {len(targets)} leads."}