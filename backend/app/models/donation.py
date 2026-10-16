from typing import Optional
from pydantic import BaseModel, Field

class DonationCreate(BaseModel):
    donorName: str = "Kind Supporter"
    donorEmail: Optional[str] = None
    amount: float = Field(..., gt=0, description="Amount in INR")
    paymentMethod: str = Field(default="UPI", description="UPI, Card, NetBanking, ItemPledge")
    targetItem: Optional[str] = None
    targetNgo: Optional[str] = None

class DonationResponse(DonationCreate):
    id: str
    transactionId: str
    status: str = "Completed"
    createdAt: str
