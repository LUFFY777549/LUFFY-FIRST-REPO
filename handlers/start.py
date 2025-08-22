# handlers/start.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


IMAGE_URL = "https://files.catbox.moe/n4sucx.jpg"


@Client.on_message(filters.command("start"))
async def start_cmd(bot: Client, message: Message):
    if message.chat.type == "private":
        # Private Chat Start
        caption = (
            "┏━━━━━━━━━━━━━━━━━━━━━━━━━⧫\n"
            "✾ Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ NGuess Bᴏᴛ!\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━⧫\n"
            "┏━━━━━━━━━━━━━━━━━━━━━━━━━⧫\n"
            "┠ ➻ I ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ɴɢᴜᴇꜱꜱ... I ᴍᴇᴀɴ, ᴅɪꜱᴄᴏᴠᴇʀ ʏᴏᴜʀ ʟᴜᴄᴋ!\n"
            "┃    ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ.\n"
            "┠ ➻ Yᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴜꜱɪɴɢ /nguess ᴄᴏᴍᴍᴀɴᴅ\n"
            "┃    ᴀɴᴅ ꜱᴇᴇ ᴡʜᴀᴛ ꜰᴏʀᴛᴜɴᴇ ᴀᴡᴀɪᴛꜱ ʏᴏᴜ!\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━⧫\n"
            "Tᴀᴘ ᴏɴ \"Hᴇʟᴘ\" ғᴏʀ ᴍᴏʀᴇ ᴄᴏᴍᴍᴀɴᴅs."
        )

        buttons = [
            [InlineKeyboardButton("📜 Hᴇʟᴘ", callback_data="help_menu")],
            [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{bot.me.username}?startgroup=true")]
        ]

        await message.reply_photo(
            photo=IMAGE_URL,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:
        # Group Chat Start
        caption = (
            f"ʜᴇʏ {message.from_user.mention},\n"
            f"ᴛʜɪs ɪs ɴGuess 🤖\n\n"
            f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title},\n"
            f"ɴGuess ᴄᴀɴ ɴᴏᴡ ʜᴇʟᴘ ʏᴏᴜ ᴛᴇꜱᴛ ʏᴏᴜʀ ʟᴜᴄᴋ!\n\n"
            f"ᴜꜱᴇ /nguess ᴛᴏ ꜱᴇᴇ ᴡʜᴀᴛ ꜰᴏʀᴛᴜɴᴇ ᴀᴡᴀɪᴛꜱ ʏᴏᴜ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ."
        )

        buttons = [
            [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{bot.me.username}?startgroup=true")]
        ]

        await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))


# Event: Bot added to group
@Client.on_message(filters.new_chat_members)
async def bot_added(bot: Client, message: Message):
    for member in message.new_chat_members:
        if member.id == bot.me.id:
            caption = (
                f"ʜᴇʏ {message.from_user.mention},\n"
                f"ᴛʜɪs ɪs ✦ NGuess Bᴏᴛ ✦ 🎲\n\n"
                f"✨ Tʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title} ✨"
            )

            buttons = [
                [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{bot.me.username}?startgroup=true")]
            ]

            await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))