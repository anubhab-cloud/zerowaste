from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str = Field(..., description="Organization or Person Name")
    email: Optional[EmailStr] = None
    role: str = Field(..., description="'PG Owner' or 'NGO'")
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: Optional[str] = "demo123"

class UserLogin(BaseModel):
    email_or_role: str
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
