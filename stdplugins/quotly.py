"""QuotLy: Avaible commands: .qbot and .qcolour <colour code/colour name>
"""
import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from uniborg.util import admin_cmd

chat = "@QuotLyBot"

@borg.on(admin_cmd(pattern="qbot ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("**Reply to any user message.**")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("**Reply to text message.**")
       return
    sender = reply_message.sender
    await event.edit("**Making a Quote**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me ( **@QuotLyBot** )```")
              return
          if response.text.startswith("Hi!"):
             await event.edit("**Can you kindly disable your forward privacy settings for good?**")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

@borg.on(admin_cmd(pattern="qcolour ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    color = event.pattern_match.group(1)
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
              await event.client.send_message(chat, "/qcolor {}".format(color))
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me ( **@QuotLyBot** )```")
              return
          await event.edit(response)
          await asyncio.sleep(5)
          await event.delete()
