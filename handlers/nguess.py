import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import waifus_col, add_waifu_to_harem, add_gold, is_registered_user

# Game state memory (per chat)
active_games = {}

# Reward amount
REWARD_GOLD = 200


async def send_new_round(chat_id, client: Client):
    waifu = await waifus_col.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    if not waifu:
        return None
    waifu = waifu[0]

    msg = await client.send_photo(
        chat_id,
        photo=waifu["image_url"],  # db.py me tumne "image_url" rakha hai
        caption=(
            "🎭 **Guess the Waifu!**\n\n"
            "⏳ You have **5 minutes** to guess her name!"
        )
    )

    active_games[chat_id] = {
        "waifu": waifu,
        "msg_id": msg.id,
        "task": asyncio.create_task(end_game_after_timeout(chat_id, client))
    }
    return waifu


async def end_game_after_timeout(chat_id, client: Client):
    await asyncio.sleep(300)  # 5 min
    if chat_id in active_games:
        waifu = active_games[chat_id]["waifu"]
        await client.send_message(
            chat_id,
            f"⏳ Time’s up! Nobody guessed **{waifu['name']}**.\n\n🎮 Game ended."
        )
        del active_games[chat_id]


@Client.on_message(filters.command("nguess") & filters.group)
async def start_guess_game(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_games:
        return await message.reply("⚠️ A game is already running in this group!")

    waifu = await send_new_round(chat_id, client)
    if not waifu:
        await message.reply("❌ No waifus uploaded yet. Use /upload first.")
    else:
        await message.reply("🎮 Guessing Game started! Type waifu’s **name** to guess.")


@Client.on_message(filters.text & filters.group)
async def handle_guess(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()

    if chat_id not in active_games:
        return

    waifu = active_games[chat_id]["waifu"]

    if text == waifu["name"].lower():
        winner = message.from_user
        await message.reply(
            f"🏆 {winner.mention} guessed it right!\n\n✨ It was **{waifu['name']}** 🎉"
        )

        # Reward + add to harem
        if await is_registered_user(user_id):
            await add_gold(user_id, REWARD_GOLD)
            await add_waifu_to_harem(user_id, waifu)

        # End current game
        active_games[chat_id]["task"].cancel()
        del active_games[chat_id]

        # Start next round
        await asyncio.sleep(2)
        await send_new_round(chat_id, client)