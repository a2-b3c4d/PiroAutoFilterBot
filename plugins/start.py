from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.fsub_control import load_fsub
from pyrogram.errors import UserNotParticipant
from time import time

# Prevent spam /start
user_start_time = {}

@Client.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    user_id = message.from_user.id

    # Anti-spam: Allow only 1 start every 2 seconds
    if user_start_time.get(user_id) and time() - user_start_time[user_id] < 2:
        return  # Ignore spamming

    user_start_time[user_id] = time()  # Save last time

    fsub_data = load_fsub()

    if not fsub_data["channels"]:
        return await message.reply("👋 Welcome! No Force Subscribe channels are set.")

    buttons = []
    not_joined = []

    for ch in fsub_data["channels"]:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                raise UserNotParticipant
        except UserNotParticipant:
            try:
                chat = await client.get_chat(ch)
                title = chat.title
                username = chat.username
                invite_link = f"https://t.me/{username}" if username else chat.invite_link
                buttons.append([InlineKeyboardButton(f"🔗 {title}", url=invite_link)])
                not_joined.append(title)
            except Exception:
                continue

    if not_joined:
        buttons.append([InlineKeyboardButton("✅ I Joined", callback_data="refresh_fsub")])
        return await message.reply(
            "**🔒 You must join these channels to use this bot:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    await message.reply(f"👋 Hello {message.from_user.mention}!\n\n✅ You have joined all required channels!")

@Client.on_callback_query(filters.regex("refresh_fsub"))
async def refresh_callback(client, callback_query):
    user_id = callback_query.from_user.id
    fsub_data = load_fsub()
    not_joined = []

    for ch in fsub_data["channels"]:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                raise UserNotParticipant
        except UserNotParticipant:
            not_joined.append(ch)

    if not_joined:
        return await callback_query.answer("❗ You haven't joined all required channels.", show_alert=True)

    await callback_query.message.delete()
    await callback_query.message.reply("✅ Great! You've joined all channels. You can now use the bot.")
