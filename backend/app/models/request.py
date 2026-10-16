from typing import Optional
from pydantic import BaseModel, Field

class RequestCreate(BaseModel):
    itemName: str = Field(..., min_length=2, description="Name of the requested item")
    quantity: str = Field(..., description="Quantity needed e.g., 500 containers")

class RequestPledge(BaseModel):
    pgId: str
    pgName: str

class RequestResponse(BaseModel):
    id: str
    ngoId: str
    ngoName: str
    itemName: str
    quantity: str
    status: str = "Needed" # "Needed" or "Fulfilled"
    fulfilledByPgId: Optional[str] = None
    fulfilledByPgName: Optional[str] = None
    createdAt: Optional[str] = None
