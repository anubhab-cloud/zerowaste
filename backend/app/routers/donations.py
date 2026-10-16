import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from ..database import get_database
from ..models.donation import DonationCreate, DonationResponse

router = APIRouter(prefix="/api/donations", tags=["Donations"])

@router.post("", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(donation: DonationCreate):
    db = get_database()
    don_id = f"don_{uuid.uuid4().hex[:8]}"
    txn_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
    
    doc = {
        "id": don_id,
        "transactionId": txn_id,
        "donorName": donation.donorName or "Kind Supporter",
        "donorEmail": donation.donorEmail,
        "amount": donation.amount,
        "paymentMethod": donation.paymentMethod,
        "targetItem": donation.targetItem,
        "targetNgo": donation.targetNgo,
        "status": "Completed",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db["donations"].insert_one(doc)
    return DonationResponse(**doc)

@router.get("", response_model=List[DonationResponse])
async def get_donations():
    db = get_database()
    cursor = db["donations"].find({}, {"_id": 0}).sort("createdAt", -1)
    donations = await cursor.to_list(length=50)
    return donations

@router.get("/summary")
async def get_donation_summary():
    db = get_database()
    donations = await db["donations"].find({}, {"_id": 0}).to_list(length=1000)
    total_amount = sum(d.get("amount", 0) for d in donations)
    count = len(donations)
    return {
        "totalRaised": total_amount,
        "totalDonations": count,
        "recentDonors": [d.get("donorName") for d in donations[:5]]
    }
