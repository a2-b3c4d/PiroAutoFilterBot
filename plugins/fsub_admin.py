from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
from database.fsub_db import (
    add_fsub_channel, remove_fsub_channel, get_fsub_channels,
    toggle_fsub_mode, get_fsub_mode
)

@Client.on_message(filters.command("addchnl") & filters.user(ADMINS))
async def add_channel(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("📝 Usage: `/addchnl -1001234567890`", quote=True)
    try:
        channel_id = int(message.command[1])
        added = add_fsub_channel(channel_id)
        if added:
            return await message.reply(f"✅ Channel `{channel_id}` added to force-sub list.")
        else:
            return await message.reply("⚠️ Channel already in the list.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

@Client.on_message(filters.command("delchnl") & filters.user(ADMINS))
async def del_channel(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("📝 Usage: `/delchnl -1001234567890`", quote=True)
    try:
        channel_id = int(message.command[1])
        removed = remove_fsub_channel(channel_id)
        if removed:
            return await message.reply(f"✅ Channel `{channel_id}` removed from force-sub list.")
        else:
            return await message.reply("❌ Channel not found in the list.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

@Client.on_message(filters.command("listchnl") & filters.user(ADMINS))
async def list_channels(client, message: Message):
    channels = get_fsub_channels()
    if not channels:
        return await message.reply("📭 No channels added to force-sub yet.")
    text = "**📌 Force-Subscribe Channels:**\n"
    for ch in channels:
        text += f"➤ `{ch}`\n"
    await message.reply(text)

@Client.on_message(filters.command("fsub_mode") & filters.user(ADMINS))
async def fsub_toggle(client, message: Message):
    mode = toggle_fsub_mode()
    await message.reply(f"🔁 Force Subscribe mode is now: **{mode.upper()}**")
