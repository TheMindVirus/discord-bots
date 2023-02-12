import random, asyncio, sys, struct, socket, time, json, discord
from discord.ext import commands

TOKEN = "<insert token here>"

intents = discord.Intents.default()
intents.message_content = True
rconmcbot = None
discordbot = commands.Bot(command_prefix = "#", intents = intents, permissions = 2048)

minecraft_server = 0
discord_server = 0
ready = 1

def main():
    global rconmcbot, discordbot
    rconmcbot = RCON()
    rconmcbot.command("/say Hi")
    discordbot.run(TOKEN)

class RCON:
    def __init__(self):
        global minecraft_server
        
        self.host = "127.0.0.1"
        self.port = 25575
        self.pswd = "123456"
        
        self.reader = None
        self.writer = None
        self.timeout = 10

        self.LOGIN = 3 # 1
        self.COMMAND = 2
        self.RESPONSE = 0
        self.INVALID_AUTH = -1

        print("__//Minecraft RCON Test\\\\__")
        self.connect()
        while minecraft_server is not ready:
            pass

    def connect(self):
        global minecraft_server
        try:
            print("Connecting to Host...", file = sys.stderr)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect((self.host, self.port))
            self.exchange(self.LOGIN, self.pswd)
            minecraft_server = ready
            print("Minecraft Ready")
        except Exception as error:
            #raise error
            print(error, file = sys.stderr)

    def command(self, command):
        try:
            message = self.exchange(self.COMMAND, command)
            print("Received:", message)
            return message
        except Exception as error:
            print(error, file = sys.stderr)
            return None

    def exchange(self, request_type, message):
        request_id = random.randint(0, 65535)
        data = struct.pack("<ii", request_id, request_type) \
             + message.encode() + b"\x00\x00"
        packet = struct.pack("<i", len(data)) + data
        self.socket.sendall(packet)
        msg, conn = self.socket.recvfrom(4)
        available = struct.unpack("<i", msg)[0]
        data, conn = self.socket.recvfrom(available)
        if not data.endswith(b"\x00\x00"):
            raise Exception("Invalid Data Received")
            return None
        request_type, request_id = struct.unpack("<ii", data[0:8])
        if request_type == self.INVALID_AUTH:
            raise Exception("Invalid Password Entered")
            return None
        message = data[8:-2].decode()
        return request_type, message

@discordbot.event
async def on_ready():
    global discord_server
    discord_server = ready
    print("Discord Ready")

@discordbot.command(name = "rconbot") # decorators still suck
async def on_command(ctx, *args):
    global rconmcbot, discordbot
    print(*args)
    rconmcbot.command("/say " + str(*args))
    response = "response"
    await ctx.send(response)

if __name__ == "__main__":
    main()
