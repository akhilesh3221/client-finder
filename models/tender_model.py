from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50))
    tender_number = Column(String(100), unique=True, index=True)
    department = Column(String(255))
    tender_name = Column(Text)
    category = Column(String(100))
    estimate_cost = Column(String(100))
    emd_amount = Column(String(100))
    publish_date = Column(String(50))
    last_date = Column(String(50))
    link = Column(String(500))
    scraped_at = Column(DateTime, default=datetime.now)