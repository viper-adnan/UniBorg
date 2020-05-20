#Made By @Nihinivi Keep Credits If You Are Goanna Kang This Lol
#And Thanks To The Creator Of Autopic This Script Was Made from Snippets From That Script
#Usage .gamerpfp  Im Not Responsible For Any Ban caused By This
import requests , re , random 
import urllib , os 
from telethon.tl import functions
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from uniborg.util import admin_cmd
import asyncio
from time import sleep

AUTOPFP_PACK = os.environ.get("AUTOPFP_PACK", None)
if AUTOPFP_PACK is None:
  PACK = [
  "star-wars-wallpaper-1080p",
  "4k-sci-fi-wallpaper",
  "star-wars-iphone-6-wallpaper",
  "kylo-ren-wallpaper",
  "darth-vader-wallpaper"
  ]
else:
  PACK = AUTOPFP_PACK
async def animepp():
    os.system("rm -rf donot.jpg")
    rnd = random.randint(0, len(PACK) - 1)
    pack = PACK[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile('/\w+/full.+.jpg')
    f = f.findall(pc)
    fy = "http://getwallpapers.com"+random.choice(f)
    print(fy)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve("https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf","f.ttf")
    urllib.request.urlretrieve(fy,"donottouch.jpg")
@borg.on(admin_cmd(pattern="gamerpfp ?(.*)"))
async def main(event):
    await event.edit("**Starting Gamer Profile Pic.**") #Owner @NihiNivi
    while True:
      try:
        await animepp()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await event.client(functions.photos.UploadProfilePhotoRequest( file))
        os.system("rm -rf donottouch.jpg")
      except:
        pass
      await asyncio.sleep(60) #Edit this to your required needs