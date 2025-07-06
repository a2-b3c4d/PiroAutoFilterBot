from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from database.fsub_db import get_fsub_channels, get_fsub_mode

@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    user = message.from_user
    fsub_mode = get_fsub_mode()
    fsub_channels = get_fsub_channels()
    
    if fsub_mode == "on" and fsub_channels:
        buttons = []
        not_joined = []
        
        for ch in fsub_channels:
            try:
                member = await client.get_chat_member(ch, user.id)
                if member.status in ["left", "kicked"]:
                    raise UserNotParticipant
            except UserNotParticipant:
                try:
                    chat = await client.get_chat(ch)
                    title = chat.title
                    invite = f"https://t.me/{chat.username}" if chat.username else chat.invite_link
                    buttons.append([InlineKeyboardButton(f"🔗 Join {title}", url=invite)])
                    not_joined.append(title)
                except:
                    continue

        if not_joined:
            buttons.append([InlineKeyboardButton("✅ I Joined", callback_data="refresh_fsub")])
            return await message.reply(
                "😎 **Hey there!**\n\n🔐 To use this bot, please join the required channels:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    
    # If all fsub passed or disabled
    await message.reply(
        f"👋 **Hello {user.first_name}**\n\n✅ You’re now ready to use the bot!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💫 Updates", url="https://t.me/Exclusivetamilcc")]
        ])
    )

@Client.on_callback_query(filters.regex("refresh_fsub"))
async def refresh_fsub(client, callback):
    user_id = callback.from_user.id
    fsub_channels = get_fsub_channels()
    still_not_joined = []

    for ch in fsub_channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                still_not_joined.append(ch)
        except:
            still_not_joined.append(ch)

    if still_not_joined:
        return await callback.answer("🚫 You're still missing some channels!", show_alert=True)

    await callback.message.delete()
    await callback.message.reply("✅ Great! You're now ready to use the bot.")
