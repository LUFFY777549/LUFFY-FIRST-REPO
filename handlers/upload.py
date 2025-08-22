from pyrogram import filters
from pyrogram.types import Message
from WaifuBot import bot
from database.db import add_waifu

RARITIES = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟡 Legendary",
    4: "🟢 Medium",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "💸 Premium Edition",
    8: "🌤 Summer",
    9: "🎐 Celestial",
    10: "❄️ Winter",
    11: "💝 Valentine",
    12: "🎃 Halloween",
    13: "🎄 Christmas Special",
    14: "🪐 𝙊𝙢𝙣𝙞𝙫𝙚𝙧𝙨𝙖𝙡 🪐",
    15: "🎭 Cosplay Master 🎭",
    16: "🎗️ 𝘼𝙈𝙑 𝙀𝙙𝙞𝙩𝙞𝙤𝙣",
    17: "🧧 𝙀𝙫𝙚𝙣𝙩𝙨",
    18: "🍑 Echhi",
}

@bot.on_message(filters.command("upload", prefixes=["/", "."]))
async def upload_waifu(_, message: Message):
    try:
        if len(message.command) < 5:
            return await message.reply(
                "❌ Usage: `/upload {name} {anime} {rarity_number} {waifu_id}`\n\nExample:\n`/upload Naruto-Uzumaki Naruto-Shippuden 5 11`"
            )

        name = message.command[1]
        anime = message.command[2]
        rarity_number = int(message.command[3])
        waifu_id = int(message.command[4])

        if rarity_number not in RARITIES:
            return await message.reply("❌ Invalid rarity number! Please use 1–18.")

        rarity = RARITIES[rarity_number]

        # Add waifu to DB
        await add_waifu(waifu_id, name, anime, rarity)

        await message.reply(
            f"✅ Waifu Uploaded Successfully!\n\n"
            f"👤 **Name:** {name}\n"
            f"📺 **Anime:** {anime}\n"
            f"💎 **Rarity:** {rarity}\n"
            f"🆔 **Waifu ID:** {waifu_id}"
        )

    except Exception as e:
        await message.reply(f"⚠️ Error: `{str(e)}`")