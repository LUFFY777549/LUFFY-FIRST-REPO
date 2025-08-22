import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from WAIFU import bot
from database.db import waifus_col, add_waifu_to_harem, add_gold, is_registered_user

# Game state memory (per chat)
active_games = {}

# Reward
REWARD_GOLD = 200

async def send_new_round(chat_id):
    waifu = await waifus_col.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    if not waifu:
        return None
    waifu = waifu[0]

    msg = await bot.send_photo(
        chat_id,
        photo=waifu["image"],
        caption=f"🎭 Guess the Waifu!\n\n⏳ You have 5 minutes to guess her name!"
    )

    active_games[chat_id] = {
        "waifu": waifu,
        "msg_id": msg.id,
        "task": asyncio.create_task(end_game_after_timeout(chat_id))
    }
    return waifu


async def end_game_after_timeout(chat_id):
    await asyncio.sleep(300)  # 5 min
    if chat_id in active_games:
        waifu = active_games[chat_id]["waifu"]
        await bot.send_message(chat_id, f"⏳ Time’s up! No one guessed **{waifu['name']}**. Game ended.")
        del active_games[chat_id]


@bot.on_message(filters.command("nguess") & filters.group)
async def start_guess_game(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_games:
        await message.reply("⚠️ A game is already running in this group!")
        return

    waifu = await send_new_round(chat_id)
    if not waifu:
        await message.reply("❌ No waifus uploaded yet. Use /upload first.")
    else:
        await message.reply("🎮 Guessing Game started! Type waifu’s name to guess.")


@bot.on_message(filters.text & filters.group)
async def handle_guess(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()

    if chat_id not in active_games:
        return

    waifu = active_games[chat_id]["waifu"]

    if text == waifu["name"].lower():
        # Winner found
        winner = message.from_user
        await message.reply(f"🏆 {winner.mention} guessed it right! It was **{waifu['name']}** 🎉")

        # Reward + harem add
        if await is_registered_user(user_id):
            await add_gold(user_id, REWARD_GOLD)
            await add_waifu_to_harem(user_id, waifu)
        
        # End current game
        active_games[chat_id]["task"].cancel()
        del active_games[chat_id]

        # Start next round
        await asyncio.sleep(2)
        await send_new_round(chat_id)