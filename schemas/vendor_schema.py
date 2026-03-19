from pydantic import BaseModel


class Vendor(BaseModel):

    company: str
    product: str
    city: str
    phone: str
    email: str

    class Config:
        orm_mode = True