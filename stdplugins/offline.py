"""
Commands - .offline .online
Offline = Add an offline tag in your name and change profile pic to black.
Online = Remove Offline Tag from your name and delete the black profile picture.
Note - If you have a last name remove it unless it automatically removed.
"""

# Made by @ViperAdnan
# Keep Credits if yoy are going to kang it.

import os , urllib, asyncio
from telethon import events
from telethon.tl import functions
from uniborg.util import admin_cmd

OFFLINE_TAG = "[Offline]"

@borg.on(admin_cmd(pattern="offline"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("**Already in Offline Mode.**")
        asyncio.sleep(2)
        await event.delete()      
        return
    await event.edit("**Changing Profile to Offline...**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    urllib.request.urlretrieve("https://telegra.ph/file/db3492a5f6cd90796d8db.jpg","donottouch.jpg")
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await borg(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit("**Changed profile to OffLine.**")
    try:
        os.system("rm -fr donottouch.jpg")
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:disable=E0602
    last_name = user.first_name
    first_name = OFFLINE_TAG
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=last_name,
            first_name=first_name
        ))
        result = "**`{} {}`\nI am Offline now.**".format(first_name, last_name)
        await event.edit(result)
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    asyncio.sleep(3)
    await event.delete()

@borg.on(admin_cmd(pattern="online"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("**Changing Profile to Online...**")
    else:
      await event.edit("**Already Online.**")
      asyncio.sleep(2)
      await event.delete()
      return
    first_name = user.last_name
    last_name = ""
    try:
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=last_name,
            first_name=first_name
        ))
        result = "**`{} {}`\nI am Online !**".format(first_name, last_name)
        await event.edit(result)
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    asyncio.sleep(3)
    await event.delete()
