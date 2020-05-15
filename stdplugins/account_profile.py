"""Profile Updation Commands
.setbio <Bio>
.setname <Name>
.setpfp <reply to image>
.delpfp <number>"""
import os
from telethon import events
from telethon.tl import functions
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="setbio (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=bio
        ))
        await event.edit("**Profile bio changed successfully.**")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="setname ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if  "\\n" in names:
        first_name, last_name = names.split("\\n", 1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            first_name=first_name,
            last_name=last_name
        ))
        await event.edit("**Name changed successfully.**")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="setpfp"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("**Downloading Profile Picture...**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    photo = None
    try:
        photo = await borg.download_media(  # pylint:disable=E0602
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY  # pylint:disable=E0602
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("**Uploading profile picture...**")
            file = await borg.upload_file(photo)  # pylint:disable=E0602
            try:
                await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                    file
                ))
            except Exception as e:  # pylint:disable=C0103,W0703
                await event.edit(str(e))
            else:
                await event.edit("**Profile Picture changed successfully.**")
    try:
        os.remove(photo)
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:disable=E0602

@borg.on(admin_cmd(pattern="delpfp ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
       n = event.pattern_match.group(1)
    else:
       n = 1
    try:
      await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=n)))
    except Exception as e:
        await event.edit(str(e))