import discord, subprocess

COMMAND = ".py"
TOKEN = "<Insert Token From Discord Here>"

client = discord.Client()

def version():
    shell = subprocess.Popen("python -VV", shell = True,
                             stdin = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
    result = shell.stdout.read().decode()
    return result

def interpret(command):
    shell = subprocess.Popen("python", shell = True,
                             stdin = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
    result = shell.communicate(command.encode())
    return result[0].decode() + result[1].decode()

@client.event
async def on_message(message):
    if message.content.startswith(COMMAND):
        try:
            if len(message.content) == len(COMMAND):
                result = version()
            else:
                result = interpret(message.content[len(COMMAND) + 1:])
            if (result is not None) and (result != ""):
                await message.channel.send(result)
        except Exception as error:
            await message.channel.send(error)

client.run(TOKEN)
