import json
from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS

FSUB_FILE = "fsub.json"

def load_fsub():
    try:
        with open(FSUB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"channels": []}

def save_fsub(data):
    with open(FSUB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@Client.on_message(filters.command("add_fsub") & filters.user(ADMINS))
async def add_fsub(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Send a valid channel username or ID.\nUsage: `/add_fsub @channelname`", quote=True)

    fsub_data = load_fsub()
    channel = message.command[1]

    if channel in fsub_data["channels"]:
        return await message.reply("⚠️ This channel is already in the force-sub list.")

    fsub_data["channels"].append(channel)
    save_fsub(fsub_data)
    await message.reply(f"✅ Added `{channel}` to force-sub list.")

@Client.on_message(filters.command("del_fsub") & filters.user(ADMINS))
async def del_fsub(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: `/del_fsub @channelname`")

    fsub_data = load_fsub()
    channel = message.command[1]

    if channel not in fsub_data["channels"]:
        return await message.reply("❌ This channel isn't in the force-sub list.")

    fsub_data["channels"].remove(channel)
    save_fsub(fsub_data)
    await message.reply(f"✅ Removed `{channel}` from force-sub list.")

@Client.on_message(filters.command("fsub_list") & filters.user(ADMINS))
async def fsub_list(client, message: Message):
    fsub_data = load_fsub()
    if not fsub_data["channels"]:
        return await message.reply("📭 No channels are set for force-subscribe yet.")

    text = "📌 **Current Force-Sub Channels:**\n\n"
    for ch in fsub_data["channels"]:
        text += f"➤ `{ch}`\n"
    await message.reply(text)

@Client.on_message(filters.command("forcesub") & filters.user(ADMINS))
async def fsub_help(client, message: Message):
    text = """
🔐 **Force Subscribe Control Panel**

**/add_fsub @channel** – Add a new fsub channel  
**/del_fsub @channel** – Remove a channel from fsub  
**/fsub_list** – View current force-sub channels  
"""
    await message.reply(text)
