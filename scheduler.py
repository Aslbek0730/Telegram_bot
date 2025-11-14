import asyncio
import logging
from typing import Iterable

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import GROUPS_FILE, REMINDER_TEXT, REMINDER_TIMES, TIMEZONE
from storage import load_chat_ids

logger = logging.getLogger(__name__)


async def send_reminders(bot: Bot) -> None:
    chat_ids = load_chat_ids(GROUPS_FILE)
    if not chat_ids:
        logger.info("No stored chat IDs. Skipping reminder dispatch.")
        return

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=REMINDER_TEXT)
            logger.info("Reminder sent to chat %s", chat_id)
        except Exception as exc:
            logger.exception("Failed to send reminder to %s: %s", chat_id, exc)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    for time_str in REMINDER_TIMES:
        hour, minute = map(int, time_str.split(":"))
        trigger = CronTrigger(hour=hour, minute=minute, timezone=TIMEZONE)
        scheduler.add_job(send_reminders, trigger, args=[bot], id=f"reminder-{time_str}")
    return scheduler


async def keep_scheduler_alive(bot: Bot) -> None:
    scheduler = setup_scheduler(bot)
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        scheduler.shutdown(wait=False)

