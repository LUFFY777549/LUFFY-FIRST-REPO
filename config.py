# config.py
import os

API_ID = int(os.getenv("API_ID", "21218274"))
API_HASH = os.getenv("API_HASH", "3474a18b61897c672d315fb330edb213")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8288304784:AAH-UOflloHLYkwU7ji32Q9tx_7o1JYeQLQ")
ADMINS = list(map(int, os.getenv("ADMINS", "7576729648,7758363857,7692444709,6596417062").split(',')))