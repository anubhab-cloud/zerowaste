import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..config import settings

router = APIRouter(prefix="/api/upload", tags=["Uploads"])

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
        
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = ".jpg"
    unique_name = f"{uuid.uuid4().hex[:12]}{ext}"
    destination_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "filename": unique_name,
        "originalName": file.filename,
        "url": f"/uploads/{unique_name}"
    }
