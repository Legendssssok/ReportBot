import os
import time

class Config(object):
    # Pyrogram Client
    API_ID    =  11573285 # ⚠️ Required
    API_HASH  = "f2cc3fdc32197c8fbaae9d0bf69d2033" # ⚠️ Required
    BOT_TOKEN =  "6881298907:AAEUslppizLWBMCS6AwF0x4CtuTzVtPp47s"# ⚠️ Required
    
    # Other Configs
    BOT_START_TIME = time.time()
    OWNER = int("5591734243") # ⚠️ Required
    SUDO = list(map(int, os.environ.get("SUDO", "5591734243").split()))  # ⚠️ Required
    # Web Response Config
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))
