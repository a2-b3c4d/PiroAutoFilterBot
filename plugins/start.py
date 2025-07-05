from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, InviteHashExpired, UserAlreadyParticipant, ChatAdminRequired
from plugins.fsub_control import load_fsub
from time import time
from info import ADMINS, FSub_Approval_Mode

user_start_time = {}

@Client.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    user_id = message.from_user.id
    if user_start_time.get(user_id) and time() - user_start_time[user_id] < 2:
        return
    user_start_time[user_id] = time()

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
                title = chat.title or "Channel"

                # ⛓ Force-sub with approval support
                if FSub_Approval_Mode == "auto":
                    try:
                        invite_link = await client.create_chat_invite_link(chat.id, member_limit=1, creates_join_request=False)
                    except ChatAdminRequired:
                        invite_link = f"https://t.me/{chat.username}" if chat.username else None
                else:  # Manual Approval Mode
                    try:
                        invite_link = await client.create_chat_invite_link(chat.id, creates_join_request=True)
                    except ChatAdminRequired:
                        invite_link = f"https://t.me/{chat.username}" if chat.username else None

                if invite_link:
                    buttons.append([InlineKeyboardButton(f"🔗 Join {title}", url=invite_link)])
                    not_joined.append(title)

            except Exception as e:
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
