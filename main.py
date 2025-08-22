# main.py
import asyncio
import importlib
import pkgutil
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN


# Client Initialize
bot = Client(
    "WaifuNguessBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")  # Auto load handlers
)


# Load all handlers manually (if needed)
def load_handlers():
    package = "handlers"
    for _, name, _ in pkgutil.iter_modules([package]):
        importlib.import_module(f"{package}.{name}")


if __name__ == "__main__":
    print("⚡ WaifuNguess Bot Starting...")
    load_handlers()
    bot.run()