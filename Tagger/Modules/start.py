from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Tagger import bot
from Tagger.db import save_user, save_group

# ADMIN/OWNER ID jisko logs jayenge
OWNER_ID = 7019600964  # apna user id yahan dal

# ✅ Handle /start in private chat
@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, message: Message):
    await save_user(message.from_user.id)
    me = await bot.get_me()

    # Log to owner
    log_text = (
        f"✦ {message.from_user.mention} just started the bot.\n\n"
        f"✦ ᴜsᴇʀ ɪᴅ ➠ `{message.from_user.id}`\n"
        f"✦ ᴜsᴇʀɴᴀᴍᴇ ➠ @{message.from_user.username if message.from_user.username else 'N/A'}"
    )
    await bot.send_message(OWNER_ID, log_text)

    await message.reply_text(
        """🌀 ᴛᴀɢᴀʟʟ ʙᴏᴛ
➖➖➖➖➖➖➖➖➖➖➖➖
‣ ᴀᴜᴛᴏ-ᴛᴀɢ ᴀʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ɪɴ ᴄʜᴜɴᴋs
‣ ᴜsᴇ /tagall ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ
‣ sᴜᴘᴘᴏʀᴛs ʀᴇᴘʟʏ + ᴄᴜsᴛᴏᴍ ᴍᴇssᴀɢᴇ
‣ sᴛᴏᴘ ᴛᴀɢ ᴀɴʏᴛɪᴍᴇ ᴜsɪɴɢ /stoptag
➖➖➖➖➖➖➖➖➖➖➖➖
ᴇᴀsʏ ᴛᴏ ᴜsᴇ & ғᴜʟʟʏ ғᴜɴᴄᴛɪᴏɴᴀʟ ᴛᴀɢɢɪɴɢ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘs 🚀""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
            [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/NARUTO_X_SUPPORT")
            ]
        ]),
        link_preview_options=None
    )


# ✅ Handle /start in groups
@bot.on_message(filters.command("start") & filters.group)
async def start_group(_, message: Message):
    await save_group(message.chat.id)

    # Group invite link
    try:
        invite_link = await bot.export_chat_invite_link(message.chat.id)
    except:
        invite_link = "N/A"

    # Log to owner
    log_text = (
        f"✦ {message.from_user.mention} just started the bot in group.\n\n"
        f"✦ ᴜsᴇʀ ɪᴅ ➠ `{message.from_user.id}`\n"
        f"✦ ᴜsᴇʀɴᴀᴍᴇ ➠ @{message.from_user.username if message.from_user.username else 'N/A'}\n"
        f"✦ ɢʀᴏᴜᴘ ➠ {message.chat.title}\n"
        f"✦ ɢʀᴏᴜᴘ ʟɪɴᴋ ➠ {invite_link}"
    )
    await bot.send_message(OWNER_ID, log_text)

    await message.reply_text(
        "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
    )