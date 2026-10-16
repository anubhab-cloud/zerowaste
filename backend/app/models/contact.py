from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)

class ContactResponse(ContactCreate):
    id: str
    createdAt: str
