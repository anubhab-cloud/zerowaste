from fastapi import APIRouter
from ..database import get_database

router = APIRouter(prefix="/api/stats", tags=["Impact Statistics"])

@router.get("")
async def get_impact_stats():
    db = get_database()
    
    pg_count = await db["users"].count_documents({"role": "PG Owner"})
    ngo_count = await db["users"].count_documents({"role": "NGO"})
    total_listings = await db["listings"].count_documents({})
    claimed_listings = await db["listings"].count_documents({"status": "Claimed"})
    available_listings = await db["listings"].count_documents({"status": "Available"})
    fulfilled_requests = await db["requests"].count_documents({"status": "Fulfilled"})
    needed_requests = await db["requests"].count_documents({"status": "Needed"})
    
    # Calculate estimated meals served (baseline + ~25 per claimed listing)
    meals_served = 3000 + (claimed_listings * 25)
    
    return {
        "mealsServed": meals_served,
        "pgOwnersJoined": max(150, pg_count + 148), # Combined community baseline + registered
        "ngoPartners": max(45, ngo_count + 43),
        "totalListings": total_listings,
        "availableListings": available_listings,
        "claimedListings": claimed_listings,
        "fulfilledRequests": fulfilled_requests,
        "neededRequests": needed_requests
    }
