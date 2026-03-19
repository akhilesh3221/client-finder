from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.vendor_model import Vendor
from google_api_service import get_google_maps_clients

router = APIRouter()

# Schema for Editing
class VendorEdit(BaseModel):
    company: str
    phone: str

@router.get("/vendors")
def get_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

@router.post("/search-clients/")
def find_new_clients(keyword: str, location: str, db: Session = Depends(get_db)):
    new_data = get_google_maps_clients(keyword, location)
    if not new_data:
        return {"message": "No results found."}

    added_count = 0
    for item in new_data:
        company_name = item['company'][:200]
        phone_num = item['phone'][:50]
        
        # Duplicate Check
        existing = db.query(Vendor).filter(Vendor.company == company_name, Vendor.phone == phone_num).first()
        
        if not existing:
            vendor = Vendor(
                company=company_name,
                product=item['product'][:200],
                city=item['city'][:100],
                phone=phone_num,
                email=item['email'][:200],
                status="Pending"
            )
            db.add(vendor)
            added_count += 1
    
    db.commit()
    return {"message": f"Added {added_count} new leads from {location}."}

@router.put("/vendors/{vendor_id}/done")
def mark_done(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if vendor:
        vendor.status = "Done"
        db.commit()
    return {"message": "Marked as done"}

@router.put("/vendors/{vendor_id}")
def edit_vendor(vendor_id: int, data: VendorEdit, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if vendor:
        vendor.company = data.company
        vendor.phone = data.phone
        db.commit()
    return {"message": "Updated"}

@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if vendor:
        db.delete(vendor)
        db.commit()
    return {"message": "Deleted"}