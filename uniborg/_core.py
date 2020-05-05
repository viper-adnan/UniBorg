# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import traceback
import os
from datetime import datetime
from uniborg import util


DELETE_TIMEOUT = 5


@borg.on(util.admin_cmd(pattern="load (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in borg._plugins:  # pylint:disable=E0602
            borg.remove_plugin(shortname)  # pylint:disable=E0602
        borg.load_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"**Successfully (re)loaded `{shortname}` Plugin.**")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load plugin {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@borg.on(util.admin_cmd(pattern="(?:remove) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"**Not removing `{shortname}` Plugin.")
    elif shortname in borg._plugins:  # pylint:disable=E0602
        borg.remove_plugin(shortname)  # pylint:disable=E0602
        path = "./stdplugins/{}.py".format(shortname)
        os.remove(path)
        msg = await event.respond(f"**Removed `{shortname}` Plugin**")
    else:
        msg = await event.respond(f"**Plugin `{shortname}` is not loaded**")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()

@borg.on(util.admin_cmd(pattern="(?:unload) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"**Not unloading `{shortname}` Plugin.")
    elif shortname in borg._plugins:  # pylint:disable=E0602
        borg.remove_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"**Unloaded `{shortname}` Plugin**")
    else:
        msg = await event.respond(f"**Plugin `{shortname}` is not loaded**")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


@borg.on(util.admin_cmd(pattern="send plugin (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def send_plug_in(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    plugin_name = event.pattern_match["shortname"]
    if plugin_name in borg._plugins:
        help_string = borg._plugins[plugin_name].__doc__
        load_string = f"**\nUse `.install plugin` while replying to this message to install plugin.**"
        if help_string:
            plugin_syntax = f"**Syntax for plugin `{plugin_name}`**:\n\n`{help_string}`\n{load_string}"
        else:
            plugin_syntax = f"{load_string}"
    the_plugin_file = "./stdplugins/{}.py".format(plugin_name)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        caption=plugin_syntax,
        force_document=True,
        allow_cache=False,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit("**Here is ↓ {} Plugin.**".format(plugin_name))


@borg.on(util.admin_cmd(pattern="install plugin"))  # pylint:disable=E0602
async def install_plug_in(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                borg.n_plugin_path  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                borg.load_plugin_from_file(downloaded_file_name)  # pylint:disable=E0602
                await event.edit("**Installed Plugin `{}` Successfully**".format(os.path.basename(downloaded_file_name)))
            else:
                path_file = os.path.basename(downloaded_file_name)
                pfile = path_file.replace(" (1)", "")
                os.remove("./stdplugins/{}".format(pfile))
                borg.load_plugin_from_file(downloaded_file_name)
                await event.edit("**Errors! Cannot install this plugin.\nMaybe already installed. 2**")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
