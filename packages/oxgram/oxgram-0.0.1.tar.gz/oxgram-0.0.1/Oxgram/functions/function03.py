from .collections import SMessage
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant
#==============================================================

async def Forcesub(bot, update, channel=None):

    if not channel:
        return SMessage(taskcode=100)
    try:
        userid = update.from_user.id
        usered = await bot.get_chat_member(channel, userid)
        if (usered.status == ChatMemberStatus.BANNED):
            return SMessage(taskcode=200)
        else:
            return SMessage(taskcode=100)
    except UserNotParticipant:
        return SMessage(taskcode=300)
    except Exception as messages:
        return SMessage(taskcode=400, errors=messages)

#==============================================================
