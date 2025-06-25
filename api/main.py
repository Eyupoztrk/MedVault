from fastapi import FastAPI
from api.routes import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "MedVault API çalışıyor!"}
