import telegram
import importlib

from telegram import Update, Bot, ParseMode
from telegram.ext import CommandHandler, run_async

from meme_bot.modules import ALL_MODULES
from meme_bot import (
    dispatcher,
    logger,
    updater,
    TOKEN,
    WEBHOOK,
    LISTEN,
    CERT_PATH,
    PORT,
    URL,
    CallbackContext,
    logger,
)

IMPORTED = {}

START_TEXT = """
Hey fam! I'm {}, and I'm here to bring some funny maymays into your life!

Check out /help for a full list of my commands with detailed descriptions.

You can check out my sourcecode [here](https://github.com/HitsukiNetwork/MemeBot)
You can also follow the news channel: @HitsukiNews
""".format(
    dispatcher.bot.first_name
)

HELP_TEXT = """
Ohai, I see you'd like to know what memes I have for sale.
Well, here you go.

*Commands:*
 _<reply> = replying to a message_
 _<args> = adding a message after the command_
 - `/bify`: - _<reply>_
    *- replying to a message with replace a random character with the B emoji.*
 - `/clap`: - _<reply>_
    *- adds clap emojis at the begining, end, and in every space in a message.*
 - `/cp`: - _<reply>_
    *- a replica of mattatas copypasta command.*
 - `/deepfry`: - _<reply>_
    *- for when your images/stickers need to get a little fried.*
 - `/dllm`: - _<optional args>_
    *- sends a random chinese meme. if you add a number after the command, itll reply with a specific photo.*
 - `/forbes`: - _<reply>_
    *- turns a message into a Forbes headline.*
 - `/mock`: - _<reply>_
    *- mocks a replied message lick the spongebob meme.*
 - `/owo`: - _<reply>_
    *- OwO whats this? OwOfies a message.*
 - `/stretch`: - _<reply>_
    *- stretches vowels in a message a random number of times.*
 - `/thonkify`: - _<reply>/<args>_
    *- turns text into thonk text (only supports letters and none symbols for now).*
 - `/vapor`: - _<reply>/<args>_
    *- turns a message into vaporwave text.*
 - `/zalgofy`: - _<reply>_
    *- corrupts a message.*
 - `/kang`: - _<reply>_
    *- Kang a sticker or animated sticker.*
 - `/stickerid`: - _<reply>_
    *- Check stickerid.*
 - `/getsticker`: - _<reply>_
    *- Get sticker file.*
"""


for module_name in ALL_MODULES:
    imported_module = importlib.import_module(
        "meme_bot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")


def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        update.effective_message.reply_text(
            START_TEXT, parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Waow sur, you've UwU-ken me :3")


def help(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        update.effective_message.reply_text(
            HELP_TEXT, parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text(
            "Try this command again in a private message."
        )


def main():
    START_HANDLER = CommandHandler("start", start, run_async=True)
    HELP_HANDLER = CommandHandler("help", help, run_async=True)

    dispatcher.add_handler(START_HANDLER)
    dispatcher.add_handler(HELP_HANDLER)

    if WEBHOOK:
        logger.info("Using webhooks.")
        updater.start_webhook(listen=LISTEN, port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(
                url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        logger.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == "__main__":
    logger.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
