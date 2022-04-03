import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

file_name = "./db/session.txt"

with TelegramClient(StringSession(), int(API_ID), str(API_HASH)) as client:
    session = client.session.save()
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(session)
    print(f"Session information saved to {file_name}.")
