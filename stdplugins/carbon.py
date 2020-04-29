"""Carbon Scraper Plugin for Userbot. //text in creative way.
usage: .kargb //as a reply to any text message

Thanks to @r4v4n4 for vars,,, Random RGB feature and .py file support by @PhycoNinja13b"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from telethon import events
from urllib.parse import quote_plus
from urllib.error import HTTPError
from time import sleep
import asyncio
import os
import random
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="carbon ?(.*)", allow_sudo=True))
async def carbon_api(e):
 RED = random.randint(0,256)
 GREEN = random.randint(0,256)
 BLUE = random.randint(0,256)
 THEME= [         "3024-night",
                  "a11y-dark",
                  "blackboard",
                  "base16-dark",
                  "base16-light",
                  "cobalt",
                  "dracula",
                  "duotone-dark",
                  "hopscotch",
                  "lucario",
                  "material",
                  "monokai",
                  "night-owl",
                  "nord",
                  "oceanic-next",
                  "one-light",
                  "one-dark",
                  "panda-syntax",
                  "paraiso-dark",
                  "seti",
                  "shades-of-purple",
                  "solarized",
                  "solarized%20light",
                  "synthwave-84",
                  "twilight",
                  "verminal",
                  "vscode",
                  "yeti",
                  "zenburn",
]

 The = random.choice(THEME)


 if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
   """ A Wrapper for carbon.now.sh """
   event = await e.edit("▢▢▢▢▢▢")
   CARBON = 'https://carbon.now.sh/?bg=rgba({R}%2C{G}%2C{B}%2C1)&t={T}&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}'
   CARBONLANG = "en"
   reply_text = await e.get_reply_message()
   input_str = e.pattern_match.group(1)
   if input_str:
       pcode = input_str
   elif reply_text.media:
       downloaded_file_name = await borg.download_media(
           reply_text,
           Config.TMP_DOWNLOAD_DIRECTORY
       )
       m_list = None
       with open(downloaded_file_name, "rb") as fd:
           m_list = fd.readlines()
       pcode = ""
       for m in m_list:
           pcode += m.decode("UTF-8")
       os.remove(downloaded_file_name)
   elif reply_text:
       pcode = str(reply_text.message) # Importing message to module
   else:
       await event.edit("**I need something to make carbon.**")
   code = quote_plus(pcode) # Converting to urlencoded
   url = CARBON.format(code=code, R=RED, G=GREEN, B=BLUE, T=The, lang=CARBONLANG)
   await event.edit("▣▢▢▢▢▢")
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
   chrome_options.add_argument("--window-size=1920x1080")
   chrome_options.add_argument("--disable-dev-shm-usage")
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument('--disable-gpu')
   prefs = {'download.default_directory' : './'}
   chrome_options.add_experimental_option('prefs', prefs)
   await event.edit("▣▣▢▢▢▢")

   driver = webdriver.Chrome(executable_path=Config.CHROME_DRIVER, options=chrome_options)
   driver.get(url)
   download_path = './'
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
   command_result = driver.execute("send_command", params)

   #driver.find_element_by_xpath('//*[@id="__next"]/main/div[3]/div[2]/div[1]/div[1]/div/span[2]').click()
   driver.find_element_by_id("export-menu").click()
   await event.edit("▣▣▣▢▢▢")
   #driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
   sleep(5) # this might take a bit.
   driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   await event.edit("▣▣▣▣▢▢")
   sleep(5)
   await event.edit("▣▣▣▣▣▢")
   driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
   sleep(5) #Waiting for downloading

   await event.edit("⬛⬛⬛⬛⬛")
   file = './carbon.png'
   await event.edit("▣▣▣▣▣▣\n**Uploading...**")
   await e.client.send_file(
         e.chat_id,
         file,
         caption="**RGB Colour Code** = `({r},{g},{b})` \n**Theme** = `{theme}`".format(r=RED,g=GREEN,b=BLUE,theme=The),
         force_document=True,
         reply_to=e.message.reply_to_msg_id,
         )

   os.remove('./carbon.png')
   # Removing carbon.png after uploading
   await event.delete() # Deleting msg
