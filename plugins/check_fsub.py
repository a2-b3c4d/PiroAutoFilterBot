from pyrogram.errors import UserNotParticipant
from plugins.fsub_control import load_fsub

async def check_user_fsub(user_id, client):
    fsub_data = load_fsub()
    for ch in fsub_data["channels"]:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False, ch
        except UserNotParticipant:
            return False, ch
        except Exception:
            continue
    return True, None
