from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ListingCreate(BaseModel):
    foodName: str = Field(..., min_length=2, description="Food name / description")
    quantity: str = Field(..., description="Quantity e.g., Feeds 15-20 people")
    pickupTime: str = Field(..., description="Best before / pickup deadline")
    location: str = Field(..., description="Pickup address")
    photoFilename: Optional[str] = None

class ListingClaim(BaseModel):
    ngoId: str
    ngoName: str

class ListingResponse(BaseModel):
    id: str
    pgId: str
    pgName: str
    foodName: str
    quantity: str
    pickupTime: str
    location: str
    photoFilename: Optional[str] = None
    status: str = "Available" # "Available" or "Claimed"
    claimedByNgoId: Optional[str] = None
    claimedByNgoName: Optional[str] = None
    createdAt: Optional[str] = None
