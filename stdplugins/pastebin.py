"""IX.IO pastebin like site
Syntax: .paste for dogbin
        .cpaste for pasting.codes
        .npaste for nekobin
        .instant for dogbin instant view"""
from telethon import events
import asyncio
from datetime import datetime
import os, json
import requests
from uniborg.util import admin_cmd
from telethon.tl.types import MessageMediaWebPage
from telethon.errors.rpcerrorlist import YouBlockedUserError


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(admin_cmd(pattern="dpaste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.text
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("**Dogged to **[Dogbin]({})\n`in {} seconds.`\n**GoTo Original URL: {}**".format(url, ms, nurl))
    else:
        await event.edit("**Dogged to **[Dogbin]({})\n`in {} seconds.`".format(url, ms))

@borg.on(admin_cmd(pattern="paste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.cpaste <long text to include>`"
    if input_str:
        message = input_str
        code = False
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            if not isinstance(previous_message.media, MessageMediaWebPage):
              downloaded_file_name = await borg.download_media(
                  previous_message,
                  Config.TMP_DOWNLOAD_DIRECTORY,
                  progress_callback=progress
              )
              m_list = None
              with open(downloaded_file_name, "rb") as fd:
                  m_list = fd.readlines()
              message = ""
              for m in m_list:
                  message += m.decode("UTF-8")
              code = True
              os.remove(downloaded_file_name)
            else:
              message = previous_message.text
              code = False
        else:
            message = previous_message.text
            code = False
    else:
        message = "**SYNTAX:** `.cpaste <long text to include>`"
        code = False
    url = "https://pasting.codes/api"
    data_json = {"heading":"viperadnan","content": message,"footer":True,"code":code,"raw":True}
    r = requests.post(url, json=data_json)
    content = r.content.decode("UTF-8")
    if r.ok:
      msg = f"View on [Pasting](https://pasting.codes{content})"
    else:
      msg = content
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(f"```{msg}```")
    

@borg.on(admin_cmd(pattern="npaste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.npaste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.npaste <long text to include>`"
    py_file =  ""
    if downloaded_file_name.endswith(".py"):
        py_file += ".py"
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}{py_file}'
        reply_text = f'**Nekofied to** [Nekobin]({url})'
        await event.edit(reply_text)
    else:
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'
        reply_text = f'**Nekofied to** [Nekobin]({url})'
        await event.edit(reply_text)

@borg.on(admin_cmd(pattern="instant ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("```Making instant view...```")
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    chat = "@chotamreaderbot"
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=272572121))
              await event.client.send_message(chat, url)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@chotamreaderbot) u Nigga```")
              return
          await event.edit(f"[Instant View]({response.message.entities[0].url})")
