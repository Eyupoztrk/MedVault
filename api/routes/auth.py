from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status,Depends
from api.schemas.user import UserCreate, UserResponse
from api.core.database import db
from api.utils.auth import hash_password, verify_password,create_access_token
from api.models.userModel import user_dict
from bson import ObjectId
from datetime import timedelta


from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email zaten kayıtlı")

    user_data = user.dict()
    user_data["hashed_password"] = hash_password(user.password)
    user_data.pop("password")  
    
    user_data["created_at"] = datetime.now(timezone.utc).isoformat()
    
    if "date_of_birth" in user_data and user_data["date_of_birth"]:
        if hasattr(user_data["date_of_birth"], 'isoformat'):
            user_data["date_of_birth"] = user_data["date_of_birth"].isoformat()
        else:
            user_data["date_of_birth"] = str(user_data["date_of_birth"])

    result = await db.users.insert_one(user_data)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return user_dict(new_user)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Kullanıcı bulunamadı")
    
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    token = create_access_token(
        data={"user_id": str(user["_id"])},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": token, "token_type": "bearer"}