import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, Message

from config import BOT_TOKEN, GROUPS_FILE, REMINDER_TEXT
from scheduler import setup_scheduler
from storage import load_chat_ids, save_chat_ids

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text, F.chat.type == ChatType.PRIVATE)
async def handle_private(message: Message) -> None:
    await message.answer(
        "Assalomu alaykum!\n\n"
        "Meni guruhingizga qo'shing. Men har kuni 08:00, 08:30 va 09:00 da "
        "eslatma yuborib turaman."
    )


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_bot_added(event: ChatMemberUpdated) -> None:
    chat_id = event.chat.id
    chat_ids = load_chat_ids(GROUPS_FILE)
    if chat_id not in chat_ids:
        chat_ids.add(chat_id)
        save_chat_ids(GROUPS_FILE, chat_ids)
        logger.info("Stored new chat_id %s", chat_id)

    await bot.send_message(
        chat_id,
        "Salom hammaga! Men endi bu guruhga eslatma yuborib turaman.",
    )


async def start() -> None:
    scheduler = setup_scheduler(bot)
    scheduler.start()
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())

