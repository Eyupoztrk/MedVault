
from fastapi import APIRouter, HTTPException, Depends
from api.core.database import db
from api.models.userModel import user_dict
from api.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_all_users():
    users_cursor = db.users.find({})
    users = []
    async for user in users_cursor:
        users.append(user_dict(user))
    return users


@router.get("/{user_id}")
async def get_user_by_id(user_id: str):
    from bson import ObjectId
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        return user_dict(user)
    except:
        raise HTTPException(status_code=400, detail="Geçersiz kullanıcı ID")
    
@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return user_dict(current_user)