import motor.motor_asyncio
from config import DB_URI

# Mongo Client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
db = mongo_client["WaifuNguessBot"]

# Collections
users_col = db["users"]
waifus_col = db["waifus"]
harems_col = db["harems"]


# ----------------- USERS -----------------
async def add_user(user_id: int, username: str = None):
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        data = {
            "user_id": user_id,
            "username": username,
            "balance": 0,
            "tickets": 0,
            "waifus_collected": 0,
            "gold": 0
        }
        await users_col.insert_one(data)


async def get_user(user_id: int):
    return await users_col.find_one({"user_id": user_id})


async def update_balance(user_id: int, amount: int):
    await users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )


async def update_tickets(user_id: int, amount: int):
    await users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"tickets": amount}},
        upsert=True
    )


async def add_gold(user_id: int, amount: int):
    """Add gold to user"""
    await users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )


async def is_registered_user(user_id: int) -> bool:
    """Check if user exists in DB"""
    user = await users_col.find_one({"user_id": user_id})
    return True if user else False


# ----------------- WAIFUS -----------------
async def upload_waifu(name: str, anime: str, rarity: str, image_url: str):
    waifu = {
        "name": name,
        "anime": anime,
        "rarity": rarity,
        "image_url": image_url
    }
    await waifus_col.insert_one(waifu)


async def get_random_waifu():
    pipeline = [{"$sample": {"size": 1}}]
    waifu = await waifus_col.aggregate(pipeline).to_list(length=1)
    return waifu[0] if waifu else None


# ----------------- HAREM -----------------
async def add_waifu_to_harem(user_id: int, waifu: dict):
    """Store waifu in user's harem"""
    await harems_col.update_one(
        {"user_id": user_id},
        {"$push": {"waifus": waifu}},
        upsert=True
    )
    await users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"waifus_collected": 1}},
        upsert=True
    )


async def get_harem(user_id: int):
    return await harems_col.find_one({"user_id": user_id})


# ----------------- LEADERBOARD -----------------
async def get_leaderboard(limit: int = 10):
    cursor = users_col.find().sort("waifus_collected", -1).limit(limit)
    return await cursor.to_list(length=limit)