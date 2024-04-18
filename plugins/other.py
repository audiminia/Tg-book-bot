from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message,CallbackQuery

from config import ADMINS
from datetime import datetime
from time import time

uptime = datetime.now()

@Bot.on_message(filters.command("start"))
async def start(client, m: Message):
    await m.reply_text(f"""
Hi {m.from_user.mention()},

🎵 Welcome, welcome, come on in! 📚
Let's dive into tales where adventures begin! 🌟
With notes and pages, we'll sing and dance, 🎶
In the world of imagination, let's take a chance! 🌈
So grab a book and join the show, 📖
Let's make music and stories flow! 🎵📚

use /book <book name> to get your book
""" 
    ,quote=True)
    
def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

@Bot.on_message(filters.command('ping') & filters.user(ADMINS))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.now() 
    delta = current_time - uptime
    stime = get_readable_time(delta.seconds)
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "<b>PONG!!</b>🏓 \n"
        f"<b>• Pinger -</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"<b>• Uptime -</b> <code>{stime}</code>\n"
    )