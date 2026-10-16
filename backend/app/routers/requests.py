import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from ..database import get_database
from ..models.request import RequestCreate, RequestPledge, RequestResponse
from ..auth_utils import get_current_user_optional

router = APIRouter(prefix="/api/requests", tags=["Item Requests"])

@router.get("", response_model=List[RequestResponse])
async def get_requests(
    status: Optional[str] = Query(None, description="Filter by status e.g. Needed, Fulfilled"),
    ngo_id: Optional[str] = Query(None, description="Filter by NGO ID"),
    pg_id: Optional[str] = Query(None, description="Filter by fulfilling PG ID")
):
    db = get_database()
    query = {}
    if status:
        query["status"] = status
    if ngo_id:
        query["ngoId"] = ngo_id
    if pg_id:
        query["fulfilledByPgId"] = pg_id
        
    cursor = db["requests"].find(query, {"_id": 0}).sort("createdAt", -1)
    requests = await cursor.to_list(length=200)
    return requests

@router.post("", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    db = get_database()
    req_id = f"r_{uuid.uuid4().hex[:8]}"
    
    ngo_id = current_user.get("id", "ngo_anonymous") if current_user else "ngo_anonymous"
    ngo_name = current_user.get("name", "Helping Hands Foundation") if current_user else "Helping Hands Foundation"
    
    doc = {
        "id": req_id,
        "ngoId": ngo_id,
        "ngoName": ngo_name,
        "itemName": request_data.itemName,
        "quantity": request_data.quantity,
        "status": "Needed",
        "fulfilledByPgId": None,
        "fulfilledByPgName": None,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db["requests"].insert_one(doc)
    return RequestResponse(**doc)

@router.put("/{request_id}/pledge", response_model=RequestResponse)
async def pledge_request(
    request_id: str,
    pledge_data: RequestPledge
):
    db = get_database()
    req = await db["requests"].find_one({"id": request_id})
    if not req:
        raise HTTPException(status_code=404, detail="Item request not found")
        
    if req.get("status") == "Fulfilled":
        raise HTTPException(status_code=400, detail="This item request has already been pledged/fulfilled.")
        
    update_doc = {
        "$set": {
            "status": "Fulfilled",
            "fulfilledByPgId": pledge_data.pgId,
            "fulfilledByPgName": pledge_data.pgName,
            "pledgedAt": datetime.now(timezone.utc).isoformat()
        }
    }
    
    await db["requests"].update_one({"id": request_id}, update_doc)
    updated = await db["requests"].find_one({"id": request_id}, {"_id": 0})
    return RequestResponse(**updated)

@router.delete("/{request_id}")
async def delete_request(request_id: str):
    db = get_database()
    result = await db["requests"].delete_one({"id": request_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Request deleted successfully", "id": request_id}
