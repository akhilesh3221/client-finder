from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models.tender_model import Tender
from utils.tender_scrapers import scrape_gem_all
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/api/tenders")
def get_tenders(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Start the scraper in the background
    background_tasks.add_task(scrape_gem_all, db)
    
    # 2. Immediately return the existing data so the page loads fast
    return db.query(Tender).order_by(Tender.id.desc()).limit(100).all()

@router.get("/tenders-dashboard")
def tenders_page(request: Request):
    return templates.TemplateResponse("tenders.html", {"request": request})