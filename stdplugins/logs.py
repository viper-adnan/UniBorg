"""Get Heroku Logs
Command - .logs"""

import heroku3
import asyncio
import os
import requests
import math
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="logs"))
async def _get_logs(event):        
  try:
       Heroku = heroku3.from_key(Config.HEROKU_API_KEY)                         
       app = Heroku.app(Config.HEROKU_APP_NAME)
  except:
  	 return await event.reply("```Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var.```")
  data = app.get_log()
  await event.edit("**Getting Logs....**")
  with open('Userbit-logs.txt', 'w') as log:
      log.write(data)
  key = requests.post('https://pasting.ga/api', json={"content": data, "heading":"Userbot Logs", "footer":True, "raw":True}).content.decode('utf-8')
  url = f'https://pasting.ga/{key}'
  await event.client.send_file(
      event.chat_id,
      "Userbit-logs.txt",
      reply_to=event.id,
      caption=f"[Logs]({url}) of 100+ lines.",
  )
  await event.delete()
  return os.remove('Userbit-logs.txt')
