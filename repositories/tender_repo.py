from sqlalchemy.orm import Session
from models.tender_model import Tender

def get_all_live_tenders(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches all tenders, ordered by the most recently published.
    """
    return db.query(Tender).order_by(Tender.publish_date.desc()).offset(skip).limit(limit).all()

def get_tenders_by_source(db: Session, source_name: str):
    """
    Filters tenders from a specific website (e.g., 'GeM', 'IREPS').
    """
    return db.query(Tender).filter(Tender.source == source_name).all()
