"""Restart or Terminate the bot from any chat
Available Commands:
.restart
.shutdown"""
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
from telethon import events
import asyncio
import os
import sys
import heroku3
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="restart"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`It will take 30 seconds for restarting.`\n**Restarted Successfully !**")
    await asyncio.sleep(1.5)
    await event.edit("**Restarted Successfully !**")
    if Config.HEROKU_APP_NAME and Config.HEROKU_API_KEY:
      heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
      app = heroku_conn.app(Config.HEROKU_APP_NAME)
      app.restart()
    else:
      await borg.disconnect()
      os.execl(sys.executable, sys.executable, *sys.argv)
      quit()


@borg.on(admin_cmd(pattern="shutdown"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("**Turning off ...Manually turn me on later.**")
    await borg.disconnect()
