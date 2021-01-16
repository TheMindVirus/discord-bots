import discord, os, random

COMMAND = ".memebot"
TOKEN = "<Insert Token From Discord Here>"
IMGPATH = os.getcwd() + "\\images\\"
GREETING = "beep-boop-beep"

client = discord.Client()
random.seed()
picked = 0
    
@client.event
async def on_message(message):
    global picked
    if message.content.startswith(COMMAND):
        try:
            images = os.listdir(IMGPATH)
            if len(images) < 1:
                raise Exception("no memes")
            i = random.randrange(0, len(images))
            while i is picked:
                i = random.randrange(0, len(images))
            picked = i
            await message.channel.send(GREETING, file = discord.File(IMGPATH + images[i]))
        except Exception as error:
            await message.channel.send(error)

client.run(TOKEN)
