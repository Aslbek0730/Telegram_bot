import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

DEFAULT_BOT_TOKEN = " "

BOT_TOKEN = os.getenv("BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()
if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is missing. Set it via env vars or config.DEFAULT_BOT_TOKEN."
    )

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
GROUPS_FILE = DATA_DIR / "groups.json"

REMINDER_TEXT = (
    "📢 Eslatma!\n\n"
    "Hurmatli guruh a'zolari. Iltimos raqamli mahalladan davomatdan o'tib qo'yinglar."
)

REMINDER_TIMES = ["08:00", "08:30", "09:00"]

TIMEZONE_NAME = os.getenv("TIMEZONE", "Asia/Tashkent")
TIMEZONE = ZoneInfo(TIMEZONE_NAME)

