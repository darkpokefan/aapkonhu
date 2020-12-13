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

import base64
from io import BytesIO
from PIL import Image

from telegram import Update
from telegram.ext import CommandHandler

from meme_bot.modules.thonkify_dict import thonkifydict
from meme_bot import CallbackContext, dispatcher

# thonkify initially made by @devrism for discord.
# Ported to Telegram Bot API (and) improved by @rupansh


def thonkify(update: Update, context: CallbackContext) -> str:
    bot = context.bot

    message = update.effective_message
    if not message.reply_to_message:
        msg = message.text.split(None, 1)[1]
    else:
        msg = message.reply_to_message.text

    # the processed photo becomes too long and unreadable + the telegram doesn't support any longer dimensions + you have the lulz.
    if (len(msg)) > 39:
        message.reply_text("thonk yourself")
        return

    tracking = Image.open(
        BytesIO(
            base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAYAAAOACAYAAAAZzQIQAAAALElEQVR4nO3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwZV4AAAfA8WFIAAAAASUVORK5CYII="
            )
        )
    )  # base64 encoded empty image(but longer)

    # remove characters thonkify can't parse
    for character in msg:
        if character not in thonkifydict:
            msg = msg.replace(character, "")

    # idk PIL. this part was untouched and ask @devrism for better explanation. According to my understanding, Image.new creates a new image and paste "pastes" the character one by one comparing it with "value" variable
    x = 0
    y = 896
    image = Image.new("RGBA", [x, y], (0, 0, 0))
    for character in msg:
        value = thonkifydict.get(character)
        addedimg = Image.new(
            "RGBA", [x + value.size[0] + tracking.size[0], y], (0, 0, 0)
        )
        addedimg.paste(image, [0, 0])
        addedimg.paste(tracking, [x, 0])
        addedimg.paste(value, [x + tracking.size[0], 0])
        image = addedimg
        x = x + value.size[0] + tracking.size[0]

    maxsize = 1024, 896
    if image.size[0] > maxsize[0]:
        image.thumbnail(maxsize, Image.ANTIALIAS)

    # put processed image in a buffer and then upload cause async
    with BytesIO() as buffer:
        buffer.name = "image.png"
        image.save(buffer, "PNG")
        buffer.seek(0)
        bot.send_sticker(chat_id=message.chat_id, sticker=buffer)


THONKIFY_HANDLER = CommandHandler("thonkify", thonkify, run_async=True)

dispatcher.add_handler(THONKIFY_HANDLER)
