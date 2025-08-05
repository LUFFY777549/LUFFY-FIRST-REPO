from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_admin(bot: Client, chat_id: int, user_id: int) -> bool:
    """
    Check if the given user is an admin or owner in the chat.
    This ignores whether the bot itself is admin.
    """
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status

        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: {status}")

        # Check only for administrator or owner (creator)
        if status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            logger.info(f"User {user_id} IS admin in chat {chat_id}")
            return True
        else:
            logger.info(f"User {user_id} is NOT admin in chat {chat_id}")
            return False

    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {e}")
        return False