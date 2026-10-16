import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_database
from ..models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from ..auth_utils import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    db = get_database()
    users_col = db["users"]
    
    if user_data.email:
        existing = await users_col.find_one({"email": user_data.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )
            
    prefix = "pg" if user_data.role == "PG Owner" else "ngo"
    user_id = f"{prefix}_{uuid.uuid4().hex[:8]}"
    
    doc = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email or f"{user_id}@zerowaste.demo",
        "role": user_data.role,
        "phone": user_data.phone,
        "address": user_data.address
    }
    
    await users_col.insert_one(doc)
    
    token = create_access_token({"sub": user_id, "role": doc["role"], "name": doc["name"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**doc)
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    db = get_database()
    users_col = db["users"]
    
    query = credentials.email_or_role.strip()
    
    # Check if role shorthand was provided e.g. "pg" or "ngo"
    if query.lower() in ["pg", "pg owner", "pg123"]:
        user = await users_col.find_one({"role": "PG Owner"}, {"_id": 0})
    elif query.lower() in ["ngo", "ngo456"]:
        user = await users_col.find_one({"role": "NGO"}, {"_id": 0})
    else:
        # Search by email, name or id
        user = await users_col.find_one(
            {"$or": [{"email": query}, {"id": query}, {"name": query}]},
            {"_id": 0}
        )
        
    if not user:
        # Create a default user on the fly if not found for convenience
        role = "PG Owner" if "pg" in query.lower() else "NGO"
        name = query if ("@" not in query) else query.split("@")[0].title()
        prefix = "pg" if role == "PG Owner" else "ngo"
        user_id = f"{prefix}_{uuid.uuid4().hex[:8]}"
        user = {
            "id": user_id,
            "name": name,
            "email": query if "@" in query else f"{user_id}@zerowaste.demo",
            "role": role,
            "phone": "+91 98765 00000",
            "address": "Bengaluru, Karnataka"
        }
        await users_col.insert_one(dict(user))

    token = create_access_token({"sub": user["id"], "role": user["role"], "name": user["name"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

@router.get("/users")
async def list_users():
    db = get_database()
    users = await db["users"].find({}, {"_id": 0}).to_list(length=100)
    return users
