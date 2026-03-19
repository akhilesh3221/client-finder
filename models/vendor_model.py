from sqlalchemy import Column, Integer, String, DateTime
# THIS IS THE MISSING LINE:
from database import Base 

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(200))
    product = Column(String(200))
    city = Column(String(100))
    phone = Column(String(50))
    email = Column(String(200))
    status = Column(String(50), default="Pending")
    last_contacted = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)