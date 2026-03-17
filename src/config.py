import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
if ADMIN_IDS_STR:
    ADMINS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]
else:
    ADMINS = []

PAYMENT_CONTACT = os.getenv("PAYMENT_CONTACT", "@krivha9")

PREMIUM_STARS_PRICE = 150

BASE_DIR = Path(__file__).parent.parent
MEDIA_DIR = BASE_DIR / "media"