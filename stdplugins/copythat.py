"""Get Telegram Profile Picture and other information
and set as own profile.
Syntax: .copythat @username
Or reply .copythat to anyone's msg.

.copymem use in a group"""
#Copy That Plugin by @ViperAdnan
#Give credit if you are going to kang it.

import html
import os
import asyncio
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from uniborg.util import admin_cmd
from telethon.tl import functions
import random

@borg.on(admin_cmd(pattern="copythat ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("**Cloning...**")
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = "⁮"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    await borg(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name,
        about=user_bio
    ))
    try:
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        pfile = await borg.upload_file(profile_pic)  # pylint:disable=E060      
        await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
            pfile
        ))
    except:
      pass
    #message_id_to_reply = event.message.reply_to_msg_id
    #if not message_id_to_reply:
    #    message_id_to_reply = event.message.id
    #await borg.send_message(
    #  event.chat_id,
    #  "Hey ? Whats Up !",
    #  reply_to=message_id_to_reply,
    #  )
    await event.delete()
    os.remove(profile_pic)
    await borg.send_message(
      event.chat_id,
      "**We are same bro.**",
      reply_to=reply_message
      )

@borg.on(admin_cmd(pattern="copymem ?(.*)"))
async def _(event):
  await event.edit("`Started`")
  while True:
    if event.fwd_from:
        return
    if event.is_private:
      await event.edit('**Use in a group**')
      return
    userid_list= []
    async for victim in borg.iter_participants(event.chat.id): 
      userid_list.append(victim.id)
    user_id = random.choice(userid_list)
    users = await event.client(functions.users.GetFullUserRequest(
              id=user_id
              ))
    user = await event.client.get_entity(user_id)
    profile_pic = await event.client.download_profile_photo(user_id, Config.TMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = user.first_name
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    last_name = user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = ""
    # inspired by https://telegram.dog/afsaI181
    user_bio = users.about
    if user_bio is not None:
        user_bio = html.escape(users.about)
    if user_bio is None:
      user_bio = ""
    await borg(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name,
        about=user_bio
    ))
    try:
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        pfile = await borg.upload_file(profile_pic)  # pylint:disable=E060      
        await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
        pfile
        ))
        os.remove(profile_pic)
    except:
      pass
    logger.info("Copied {}".format(user_id))
    await asyncio.sleep(60)

async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
