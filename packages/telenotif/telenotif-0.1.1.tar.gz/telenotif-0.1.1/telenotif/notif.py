# telenotif/__init__.py
from .notif import notif

__version__ = "0.1.1"

# telenotif/exceptions.py
class TelenotifError(Exception):
    """Base exception for telenotif library."""
    pass

# telenotif/notif.py
from telegram import Bot
from telegram.error import TelegramError
from .exceptions import TelenotifError  # Fixed import
import asyncio
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def _ensure_async_loop():
    """Ensure there's an event loop running."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

class notif:
    """
    A simple notification class that sends messages via Telegram bot.
    """
    
    def __init__(self, bot_token, user_id, disable_notification=False):
        self.bot = Bot(token=bot_token)
        self.user_id = user_id
        self.disable_notification = disable_notification
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Validate the bot token and user ID."""
        loop = _ensure_async_loop()
        try:
            loop.run_until_complete(self.bot.get_me())
        except TelegramError as e:
            raise TelenotifError(f"Invalid bot token: {str(e)}")
    
    async def _send_message_async(self, message):
        """Send message asynchronously."""
        try:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=message,
                disable_notification=self.disable_notification
            )
            return True
        except TelegramError as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False

    def alert(self, message):
        """Send a notification message."""
        loop = _ensure_async_loop()
        return loop.run_until_complete(self._send_message_async(message))