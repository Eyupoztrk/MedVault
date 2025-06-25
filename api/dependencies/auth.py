from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.utils.auth import decode_access_token
from api.core.database import db
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user = await db.users.find_one({"_id": ObjectId(payload["user_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    return user
