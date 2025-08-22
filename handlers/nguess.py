# handlers/nguess.py
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import waifus_col, guess_games, add_gold, add_waifu_to_harem, is_registered_user

# -------- Settings -------- #
REWARD_COINS = 20
STREAK_REWARD = 20  # streak required to win a random waifu
TIME_LIMIT = 300    # 5 min

# -------- Helper Function: New Round -------- #
async def send_new_round(chat_id: int, client: Client):
    waifus = await waifus_col.find().to_list(length=None)

    if not waifus:
        await client.send_message(chat_id, "❌ No waifus uploaded yet!")
        return None

    waifu = random.choice(waifus)

    # ✅ Handle image key
    image_id = waifu.get("image") or waifu.get("file_id")
    if not image_id:
        await client.send_message(chat_id, f"⚠️ No image found for '{waifu.get('name', 'Unknown')}'.")
        return None

    # Question message
    await client.send_photo(
        chat_id,
        photo=image_id,
        caption=(
            "🎭 **Character Guessing Game** 🎭\n\n"
            "✨ A mysterious character has appeared! ✨\n\n"
            "🔍 *Can you guess who this is?*\n"
            "⏳ You have **5 minutes** to answer!\n\n"
            "💬 Type just the **name** in chat!"
        )
    )

    # Save game state in DB
    await guess_games.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "answer": waifu["name"].lower(),
            "waifu": waifu,
            "active": True,
            "streak": 0
        }},
        upsert=True
    )

    # End game after timeout
    asyncio.create_task(end_game_after_timeout(chat_id, client))

    return waifu


# -------- End Game Timeout -------- #
async def end_game_after_timeout(chat_id: int, client: Client):
    await asyncio.sleep(TIME_LIMIT)
    game = await guess_games.find_one({"chat_id": chat_id, "active": True})
    if game:
        await client.send_message(
            chat_id,
            f"⏳ Time’s up! Nobody guessed **{game['answer'].title()}**.\n\n💔 The game has ended."
        )
        await guess_games.update_one({"chat_id": chat_id}, {"$set": {"active": False}})


# -------- Start Guess Game -------- #
@Client.on_message(filters.command("waifuguess"))
async def start_guess_game(client: Client, message: Message):
    chat_id = message.chat.id
    game = await guess_games.find_one({"chat_id": chat_id, "active": True})
    if game:
        return await message.reply("⚠️ A game is already running in this group!")

    waifu = await send_new_round(chat_id, client)
    if waifu:
        await message.reply("✅ Game started! Guess the waifu by typing her name 👀")


# -------- Check Answers -------- #
@Client.on_message(filters.text & ~filters.command(["waifuguess"]))
async def check_answer(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_answer = message.text.strip().lower()

    game = await guess_games.find_one({"chat_id": chat_id, "active": True})
    if not game:
        return

    correct_answer = game.get("answer", "").lower()

    if user_answer == correct_answer:
        waifu = game["waifu"]

        # Update streak
        new_streak = game.get("streak", 0) + 1

        # Reward user with coins
        if await is_registered_user(user_id):
            await add_gold(user_id, REWARD_COINS)

        msg_text = (
            "🎉 **Correct!** 🎉\n\n"
            f"🏆 +{REWARD_COINS} Coins | 🔥 Streak: {new_streak}\n\n"
            f"The character was **{waifu['name']}** from **{waifu['anime']}** {waifu['rarity']}!"
        )

        # If streak reached reward threshold
        if new_streak >= STREAK_REWARD:
            random_waifu = random.choice(await waifus_col.find().to_list(length=None))
            if await is_registered_user(user_id):
                await add_waifu_to_harem(user_id, random_waifu)

            msg_text += (
                "\n\n💎 **Bonus Reward!** 💎\n"
                f"You maintained a **{STREAK_REWARD} streak** and received a random waifu: "
                f"**{random_waifu['name']}** from **{random_waifu['anime']}** {random_waifu['rarity']}!"
            )
            new_streak = 0  # reset streak

        await message.reply(msg_text)

        # Update streak in DB
        await guess_games.update_one(
            {"chat_id": chat_id},
            {"$set": {"streak": new_streak}}
        )

        # Start next round
        await send_new_round(chat_id, client)