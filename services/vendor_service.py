from database import SessionLocal
from models.vendor_model import Vendor

def get_all_vendors():
    db = SessionLocal()
    vendors = db.query(Vendor).all()
    db.close()
    return vendors