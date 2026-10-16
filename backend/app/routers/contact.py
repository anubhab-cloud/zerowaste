import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, status
from ..database import get_database
from ..models.contact import ContactCreate, ContactResponse

router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(contact: ContactCreate):
    db = get_database()
    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    
    doc = {
        "id": msg_id,
        "name": contact.name,
        "email": contact.email,
        "subject": contact.subject,
        "message": contact.message,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db["contacts"].insert_one(doc)
    return ContactResponse(**doc)

@router.get("", response_model=List[ContactResponse])
async def list_messages():
    db = get_database()
    cursor = db["contacts"].find({}, {"_id": 0}).sort("createdAt", -1)
    return await cursor.to_list(length=100)
