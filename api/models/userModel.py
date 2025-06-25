from datetime import datetime


def user_dict(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "date_of_birth": user.get("date_of_birth"),
        "gender": user.get("gender"),
    }
