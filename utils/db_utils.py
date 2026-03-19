from sqlalchemy.orm import Session
from models.tender_model import Tender
from datetime import datetime

def save_tender_to_db(db: Session, data: dict):
    """
    Saves a tender to the database while ensuring:
    1. No duplicates (Check by tender_number)
    2. Auto-update if data (like Last Date) changes
    3. Proper session handling
    """
    try:
        # 1. SEARCH: Check if this Tender Number already exists
        # tender_number is the unique ID from GeM/IREPS/NTPC
        existing_tender = db.query(Tender).filter(
            Tender.tender_number == data.get('tender_number')
        ).first()

        if existing_tender:
            # 2. UPDATE LOGIC: If it exists, check if 'Last Date' or 'Estimate' updated
            # Government departments often extend deadlines.
            updated = False
            
            if existing_tender.last_date != data.get('last_date'):
                existing_tender.last_date = data.get('last_date')
                updated = True
                
            if existing_tender.estimate_cost != data.get('estimate_cost'):
                existing_tender.estimate_cost = data.get('estimate_cost')
                updated = True

            if updated:
                db.commit()
                print(f"🔄 Updated info for: {data['tender_number']}")
            else:
                print(f"⏩ Duplicate found, skipping: {data['tender_number']}")
            
            return False # Record was already there

        # 3. INSERT LOGIC: Create new record if not found
        new_tender = Tender(
            source=data.get('source'),
            tender_number=data.get('tender_number'),
            department=data.get('department'),
            tender_name=data.get('tender_name'),
            category=data.get('category'),
            estimate_cost=data.get('estimate_cost'),
            emd_amount=data.get('emd_amount'),
            publish_date=data.get('publish_date'),
            last_date=data.get('last_date'),
            link=data.get('link')
        )
        
        db.add(new_tender)
        db.commit()
        print(f"✅ Successfully Saved New Tender: {data['tender_number']}")
        return True

    except Exception as e:
        db.rollback() # Undo changes if there is a crash
        print(f"❌ Database Error in save_tender_to_db: {str(e)}")
        return False