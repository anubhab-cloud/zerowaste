import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from ..database import get_database
from ..models.listing import ListingCreate, ListingClaim, ListingResponse
from ..auth_utils import get_current_user_optional

router = APIRouter(prefix="/api/listings", tags=["Food Listings"])

@router.get("", response_model=List[ListingResponse])
async def get_listings(
    status: Optional[str] = Query(None, description="Filter by status e.g. Available, Claimed"),
    pg_id: Optional[str] = Query(None, description="Filter by PG Owner ID"),
    ngo_id: Optional[str] = Query(None, description="Filter by Claiming NGO ID")
):
    db = get_database()
    query = {}
    if status:
        query["status"] = status
    if pg_id:
        query["pgId"] = pg_id
    if ngo_id:
        query["claimedByNgoId"] = ngo_id
        
    cursor = db["listings"].find(query, {"_id": 0}).sort("createdAt", -1)
    listings = await cursor.to_list(length=200)
    return listings

@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_data: ListingCreate,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    db = get_database()
    listing_id = f"l_{uuid.uuid4().hex[:8]}"
    
    pg_id = current_user.get("id", "pg_anonymous") if current_user else "pg_anonymous"
    pg_name = current_user.get("name", "Anonymous PG") if current_user else "Anonymous PG"
    
    doc = {
        "id": listing_id,
        "pgId": pg_id,
        "pgName": pg_name,
        "foodName": listing_data.foodName,
        "quantity": listing_data.quantity,
        "pickupTime": listing_data.pickupTime,
        "location": listing_data.location,
        "photoFilename": listing_data.photoFilename,
        "status": "Available",
        "claimedByNgoId": None,
        "claimedByNgoName": None,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db["listings"].insert_one(doc)
    return ListingResponse(**doc)

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: str):
    db = get_database()
    listing = await db["listings"].find_one({"id": listing_id}, {"_id": 0})
    if not listing:
        raise HTTPException(status_code=404, detail="Surplus listing not found")
    return ListingResponse(**listing)

@router.put("/{listing_id}/claim", response_model=ListingResponse)
async def claim_listing(
    listing_id: str,
    claim_data: ListingClaim
):
    db = get_database()
    listing = await db["listings"].find_one({"id": listing_id})
    if not listing:
        raise HTTPException(status_code=404, detail="Surplus listing not found")
        
    if listing.get("status") == "Claimed":
        raise HTTPException(status_code=400, detail="This listing has already been claimed.")
        
    update_doc = {
        "$set": {
            "status": "Claimed",
            "claimedByNgoId": claim_data.ngoId,
            "claimedByNgoName": claim_data.ngoName,
            "claimedAt": datetime.now(timezone.utc).isoformat()
        }
    }
    
    await db["listings"].update_one({"id": listing_id}, update_doc)
    updated = await db["listings"].find_one({"id": listing_id}, {"_id": 0})
    return ListingResponse(**updated)

@router.delete("/{listing_id}")
async def delete_listing(listing_id: str):
    db = get_database()
    result = await db["listings"].delete_one({"id": listing_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"message": "Listing deleted successfully", "id": listing_id}
