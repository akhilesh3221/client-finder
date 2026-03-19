from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base, get_db

# 1. Import all your routers
from routes.vendor_routes import router as vendor_router
from routes.automation_routes import router as automation_router
from routes.tender_routes import router as tender_router

# 2. Import all models
from models.vendor_model import Vendor
from models.tender_model import Tender

# 3. Initialize Database Tables
Base.metadata.create_all(bind=engine)

# 4. CREATE THE APP (Must be at the top level before routes)
app = FastAPI()

# 5. Setup Templates
templates = Jinja2Templates(directory="templates")

# 6. DEFINE ROUTES (Now they can use @app)

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_leads = db.query(Vendor).count()
    pending_leads = db.query(Vendor).filter(Vendor.status == "Pending").count()
    total_tenders = db.query(Tender).count()
    
    return {
        "total_leads": total_leads,
        "pending_leads": pending_leads,
        "total_tenders": total_tenders
    }

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/blast-center")
def blast_center(request: Request):
    return templates.TemplateResponse("automation.html", {"request": request})

@app.get("/tenders-dashboard")
def tenders_dashboard(request: Request):
    return templates.TemplateResponse("tenders.html", {"request": request})

# 7. INCLUDE ALL ROUTERS
app.include_router(vendor_router)
app.include_router(automation_router)
app.include_router(tender_router)