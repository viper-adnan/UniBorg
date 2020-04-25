"""Unofficial updater. Currently in Deployment Stage
Command - .update 
Replace . with your command handler 
This May result in Downtime of bot.
If you are using fork than add a heroku var.
GIT_REPO_URL = {your fork url}"""


#"""Update UserBot code (for UniBorg)
#Syntax: .update
#\nAll Credits goes to © @Three_Cube_TeKnoways
#\nFor this awasome plugin.\nPorted from PpaperPlane Extended"""

from os import remove
from os import execl
import sys
# from git import Repo
# from git.exc import GitCommandError
# from git.exc import InvalidGitRepositoryError
# from git.exc import NoSuchPathError
# from .. import bot
# from uniborg.events import register
import git
import asyncio
import random
import re
import time
from collections import deque
import requests
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon import events
from uniborg.util import admin_cmd
from contextlib import suppress
import os
import sys
import asyncio
# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "**Looks like a custom branch {branch_name}**"
    "Is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)
GIT_REPO_URL = os.environ.get("GIT_REPO_URL", "https://github.com/viper-adnan/userbot/")
BOT_IS_UP_TO_DATE = "`The userbot is up-to-date.\nThank you for Using this Service.`"
NEW_BOT_UP_DATE_FOUND = (
    "**New update found for `{branch_name}` branch.**\n"
    "**Changelog: {changelog}\n\n"
    "Updating...**"
)
NEW_UP_DATE_FOUND = (
    "**New update found for `{branch_name}` branch.**\n"
    "\n**Updating...**"
)
REPO_REMOTE_NAME = os.environ.get("REPO_REMOTE_NAME", "temponame")
IFFUCI_ACTIVE_BRANCH_NAME = "master"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "**No heroku application found.**"
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "**Re-Starting heroku application.**"
# -- Constants End -- #


@borg.on(admin_cmd(pattern="update ?(.*)", outgoing=True))
async def updater(message):
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, GIT_REPO_URL)
        origin.fetch()
        repo.create_head(IFFUCI_ACTIVE_BRANCH_NAME, origin.refs.master)
        repo.heads.master.checkout(True)

    active_branch_name = repo.active_branch.name
    if active_branch_name != IFFUCI_ACTIVE_BRANCH_NAME:
        await message.edit(IS_SELECTED_DIFFERENT_BRANCH.format(
            branch_name=active_branch_name
        ))
        return False

    try:
        repo.create_remote(REPO_REMOTE_NAME, GIT_REPO_URL)
    except Exception as e:
        print(e)
        pass

    temp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    temp_upstream_remote.fetch(active_branch_name)

    changelog = generate_change_log(
        repo,
        DIFF_MARKER.format(
            remote_name=REPO_REMOTE_NAME,
            branch_name=active_branch_name
        )
    )

    if not changelog:
        await message.edit("**Checking for updates...**")
        await asyncio.sleep(1.5)
 
    message_one = NEW_BOT_UP_DATE_FOUND.format(
        branch_name=active_branch_name,
        changelog=changelog
    )
    message_two = NEW_UP_DATE_FOUND.format(
        branch_name=active_branch_name
    )

    if len(message_one) > 4095:
        with open("change.log", "w+", encoding="utf8") as out_file:
            out_file.write(str(message_one))
        await tgbot.send_message(
            message.chat_id,
            document="change.log",
            caption=message_two
        )
        await asyncio.sleep(8)
        os.remove("change.log")
    else:
        await message.edit(message_one)
        await asyncio.sleep(1.5)

    temp_upstream_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    if Config.HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            if Config.HEROKU_APP_NAME is not None:
                heroku_app = None
                for i in heroku_applications:
                    if i.name == Config.HEROKU_APP_NAME:
                        heroku_app = i
                if heroku_app is None:
                    await message.edit("**Invalid APP Name. Please set the name of your bot in heroku in the var `HEROKU_APP_NAME.`**")
                    return
                heroku_git_url = heroku_app.git_url.replace(
                    "https://",
                    "https://api:" + Config.HEROKU_API_KEY + "@"
                )
                if "heroku" in repo.remotes:
                    remote = repo.remote("heroku")
                    remote.set_url(heroku_git_url)
                else:
                    remote = repo.create_remote("heroku", heroku_git_url)
                asyncio.get_event_loop().create_task(deploy_start(tgbot, message, HEROKU_GIT_REF_SPEC, remote))

            else:
                await message.edit("**Please create the var `HEROKU_APP_NAME` as the key and the name of your bot in heroku as your value.**")
                return
        else:
            await message.edit(NO_HEROKU_APP_CFGD)
    else:
        await message.edit("**No heroku api key found in** `HEROKU_API_KEY` **var.**")
        

def generate_change_log(git_repo, diff_marker):
    out_put_str = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        out_put_str += f"•[{repo_change.committed_datetime.strftime(d_form)}]: {repo_change.summary} <{repo_change.author}>\n"
    return out_put_str

async def deploy_start(tgbot, message, refspec, remote):
    await message.edit(RESTARTING_APP)
    await message.edit("**Deployment Started Successfully !**")
    remote.push(refspec=refspec)
    await tgbot.disconnect()
    await message.edit("**Already Up-to-date.**")
    os.execl(sys.executable, sys.executable, *sys.argv)
