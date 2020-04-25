"""Get heroku Usage and set/delete/get env vars
Commands:
.get var {var name}
.set var {var name} {value}
.del var {var name}
Above operation result in downtime of bot.
Get heroku dyno status by .usage
Replace . to your command handler
"""


#"""CC- refundisillegal\nSyntax:- .usage"""

import heroku3
import asyncio
import os
import requests
import math

from uniborg.util import admin_cmd, prettyjson
from sample_config import Config
# ================= 
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

@borg.on(admin_cmd(pattern=r"(set|get|del) var ?(.*)", allow_sudo=True))
async def variable(var):
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        return await var.edit("**[HEROKU]:"
                              "\nPlease setup your `HEROKU_APP_NAME` var.**")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        await var.edit("**Getting information...**")
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await var.edit("**ConfigVars:"
                                      f"\n\n`{variable}` = `{heroku_var[variable]}`**\n")
            else:
                return await var.edit("**ConfigVars:"
                                      f"\n\nError:\n-> `{variable}` doesn't exists**")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="**Output too large, sending it as a file**",
                    )
                else:
                    await var.edit("`[HEROKU]` ConfigVars:\n\n"
                                   "================================"
                                   f"\n```{result}```\n"
                                   "================================"
                                   )
            os.remove("configs.json")
            return
    elif exe == "set":
        await var.edit("**Setting information...**")
        val = var.pattern_match.group(2).split()
        try:
            val[1]
        except IndexError:
            return await var.edit("`.set var <config name> <value>`")
        await asyncio.sleep(1.5)
        if val[0] in heroku_var:
            await var.edit(f"`{val[0]}` **successfully changed to** `{val[1]}`")
        else:
            await var.edit(f"`{val[0]}` **successfully added with value:** `{val[1]}`")
        heroku_var[val[0]] = val[1]
    elif exe == "del":
        await var.edit("**Getting information to delete variable...**")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await var.edit("**Please specify ConfigVars you want to delete.**")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await var.edit(f"`{variable}` **deleted successfully.**")
            del heroku_var[variable]
        else:
            return await var.edit(f"`{variable}` **is not exists.**")

        
@borg.on(admin_cmd(pattern="usage ?(.*)", allow_sudo=True))
async def _(event):
    await event.edit("**Processing...**")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {HEROKU_API_KEY}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await event.edit("**Error: something went wrong.**\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    return await event.edit("**Dyno Usage**:\n\n"
                           f"• `Dyno usage for`  **{HEROKU_APP_NAME}**:\n"
                           f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                           f"**|**  [`{AppPercentage}`**%**]"
                           "\n"
                           "• `Dyno hours quota remaining this month`:\n"
                           f"     •  `{hours}`**h**  `{minutes}`**m**  "
                           f"**|**  [`{percentage}`**%**]"
                           )