#    Hitsuki (A telegram bot project)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import sys
from os import path

import telegram.ext as tg

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    LISTEN = os.environ.get("0.0.0.0", "")
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    DEEPFRY_TOKEN = os.environ.get("DEEPFRY_TOKEN", "")

elif path.exists("meme_bot/config.py"):
    from meme_bot.config import Config

    TOKEN = Config.API_KEY
    WEBHOOK = Config.WEBHOOK
    LISTEN = Config.LISTEN
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    DEEPFRY_TOKEN = Config.DEEPFRY_TOKEN

updater = tg.Updater(TOKEN)
dispatcher = updater.dispatcher
CallbackContext = tg.CallbackContext
