from sqlalchemy.orm import Session
from models.tender_model import Tender

def save_tender_to_db(db: Session, data: dict):
    # Check if tender already exists to avoid duplicates
    exists = db.query(Tender).filter(Tender.tender_number == data['tender_number']).first()
    if not exists:
        new_tender = Tender(
            tender_number=data['tender_number'],
            title=data['title'],
            category=data['category'],
            department=data['department'],
            bid_estimate=data['bid_estimate'],
            emd_amount=data['emd_amount'],
            publish_date=data['publish_date'],
            last_date=data['last_date'],
            source=data['source']
        )
        db.add(new_tender)
        db.commit()

# --- Example Scraper Functions ---
def scrape_gem_all():
    # Logic for GeM (using Selenium for infinite scroll)
    pass

def scrape_railways_all():
    # Logic for IREPS (Railways)
    pass