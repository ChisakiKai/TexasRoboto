import logging
import os
import sys
import time
import spamwatch
import telegram.ext as tg
from telethon import TelegramClient
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from configparser import ConfigParser
from rich.logging import RichHandler

StartTime = time.time()

# enable logging
FORMAT = "%(message)s"
logging.basicConfig(
    handlers=[RichHandler()], level=logging.INFO, format=FORMAT, datefmt="[%X]"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
log = logging.getLogger("rich")

log.info("Twxas is starting. | An Zero Union Project. | Licensed under GPLv3.")

log.info("Not affiliated to Ark or Levels in any way whatsoever.")
log.info("Project maintained by: github.com/ChisakiKai (t.me/ChisakiKai/TexasRoboto)")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    log.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ConfigParser()
parser.read("config.ini")
kagconfig = parser["kagconfig"]


OWNER_ID = kagconfig.getint("OWNER_ID")
OWNER_USERNAME = kagconfig.get("OWNER_USERNAME")
APP_ID = kagconfig.getint("APP_ID")
API_HASH = kagconfig.get("API_HASH")
WEBHOOK = kagconfig.getboolean("WEBHOOK", False)
URL = kagconfig.get("URL", None)
CERT_PATH = kagconfig.get("CERT_PATH", None)
PORT = kagconfig.getint("PORT", None)
INFOPIC = kagconfig.getboolean("INFOPIC", False)
DEL_CMDS = kagconfig.getboolean("DEL_CMDS", False)
STRICT_GBAN = kagconfig.getboolean("STRICT_GBAN", False)
ALLOW_EXCL = kagconfig.getboolean("ALLOW_EXCL", False)
CUSTOM_CMD = kagconfig.get("CUSTOM_CMD", None)
BAN_STICKER = kagconfig.get("BAN_STICKER", None)
TOKEN = kagconfig.get("TOKEN")
DB_URI = kagconfig.get("SQLALCHEMY_DATABASE_URI")
LOAD = kagconfig.get("LOAD").split()
LOAD = list(map(str, LOAD))
MESSAGE_DUMP = kagconfig.getfloat("MESSAGE_DUMP")
GBAN_LOGS = kagconfig.getfloat("GBAN_LOGS")
NO_LOAD = kagconfig.get("NO_LOAD").split()
NO_LOAD = list(map(str, NO_LOAD))
SUDO_USERS = kagconfig.get("SUDO_USERS").split()
SUDO_USERS = list(map(int, SUDO_USERS))
DEV_USERS = kagconfig.get("DEV_USERS").split()
DEV_USERS = list(map(int, DEV_USERS))
SUPPORT_USERS = kagconfig.get("SUPPORT_USERS").split()
SUPPORT_USERS = list(map(int, SUPPORT_USERS))
SARDEGNA_USERS = kagconfig.get("SARDEGNA_USERS").split()
SARDEGNA_USERS = list(map(int, SARDEGNA_USERS))
WHITELIST_USERS = kagconfig.get("WHITELIST_USERS").split()
WHITELIST_USERS = list(map(int, WHITELIST_USERS))
SPAMMERS = kagconfig.get("SPAMMERS").split()
SPAMMERS = list(map(int, SPAMMERS))
spamwatch_api = kagconfig.get("spamwatch_api")
CASH_API_KEY = kagconfig.get("CASH_API_KEY")
TIME_API_KEY = kagconfig.get("TIME_API_KEY")
WALL_API = kagconfig.get("WALL_API")
LASTFM_API_KEY = kagconfig.get("LASTFM_API_KEY")
try:
    CF_API_KEY = kagconfig.get("CF_API_KEY")
    log.info("AI antispam powered by Intellivoid.")
except:
    log.info("No Coffeehouse API key provided.")
    CF_API_KEY = None


SUDO_USERS.append(OWNER_ID)
DEV_USERS.append(OWNER_ID)

# SpamWatch
if spamwatch_api is None:
    sw = None
    log.warning("SpamWatch API key is missing! Check your config.ini")
else:
    try:
        sw = spamwatch.Client(spamwatch_api)
    except:
        sw = None
        log.warning("Can't connect to SpamWatch!")

updater = tg.Updater(
    TOKEN,
    workers=min(32, os.cpu_count() + 4),
    request_kwargs={"read_timeout": 10, "connect_timeout": 10},
)
telethn = TelegramClient("texas", APP_ID, API_HASH)
dispatcher = updater.dispatcher

kp = Client(
    "TexasPyro",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
)
apps = []
apps.append(kp)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
SARDEGNA_USERS = list(SARDEGNA_USERS)
SPAMMERS = list(SPAMMERS)

# Load at end to ensure all prev variables have been set
from tg_bot.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler


def spamfilters(text, user_id, chat_id):
    # print("{} | {} | {}".format(text, user_id, chat_id))
    if int(user_id) in SPAMMERS:
        print("This user is a spammer!")
        return True
    else:
        return False
