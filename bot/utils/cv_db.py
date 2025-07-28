from motor.motor_asyncio import AsyncIOMotorClient
from config import load_config

config = load_config()


client = AsyncIOMotorClient(config.mongo_uri)
db = client["bec-2025-bot"]  

users_collection = db["users"]
teams_collection = db["teams"]
cv_collection = db["cv"]

async def update_cv_file_path(user_id: int, file_path: str) -> bool:
    result = await users_collection.update_one(
        {"telegram_id": user_id},
        {"$set": {"cv_file_path": file_path}},
        upsert=True
    )
    return result.matched_count > 0 or result.upserted_id is not None

async def add_cv(user_id: int, cv_file_id: str = None, position: str = None, 
                 languages: list = None, education: str = None, experience: str = None, 
                 skills: list = None, about: str = None, contacts: dict = None):
    user = await users_collection.find_one({"telegram_id": user_id})
    cv_data = {
        "telegram_id": user_id,
        "username": user["username"] if user else user["name"],
        "cv_file_id": cv_file_id,
        "position": position,
        "languages": languages,
        "education": education,
        "experience": experience,
        "skills": skills,
        "about": about,
        "contacts": contacts
    }
    await cv_collection.update_one(
        {"telegram_id": user_id},  
        {"$set": cv_data},        
        upsert=True               
    )
