from typing import Dict

from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (PeerChannel)

from config import logger, API_ID, API_HASH, SESSION_STRING


@logger.catch
async def get_channel_data(user_input_channel: str) -> Dict[int, dict]:
    """
    Returns dictionary with channel users data
    user_input_channel: ID of channel without head "-100"
    """

    async with TelegramClient(StringSession(SESSION_STRING), int(API_ID), str(API_HASH)) as client:
        await client.start()
        print("Client Created")

        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await client.get_entity(entity)

        offset = 0
        limit = 100
        all_participants = []
        while True:
            participants = await client(GetParticipantsRequest(
                my_channel, ChannelParticipantsSearch(''), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)
        all_user_details: Dict[int, dict] = {
            participant.id:
                {
                    "id": participant.id,
                    "first_name": participant.first_name,
                    "last_name": participant.last_name,
                    "user": participant.username,
                    "phone": participant.phone,
                    "is_bot": participant.bot
                }
            for participant in all_participants
            if not participant.bot
        }

    return all_user_details
