import discord, asyncio, threading, serial, sys

def main():
    client = ClientMod()
    client.testmode = False
    client.schedtime = 0.01
    client.errortime = 1
    client.command = ".pico"
    client.token = "<Insert >"
    client.port = "COM5"
    client.baudrate = 115200
    client.run(client.token)

class ClientMod(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channelID = None
        self.device = serial.Serial()
    
    def run(self, *args, **kwargs):
        if self.testmode:
            self.task = self.loop.create_task(self.test())
        else:
            self.task = self.loop.create_task(self.on_serial())
        super().run(*args, **kwargs)
    
    async def on_message(self, message):
        self.channelID = message.channel.id
        if message.content.startswith(self.command):
            try:
                if self.testmode:
                    await message.channel.send("PING")
                data = message.content[len(self.command) + 1:] + "\r\n"
                print("check")
                if self.device.is_open:
                    self.device.write(data.encode())
                    self.device.flush()
            except Exception as error:
                self.device.close()
                print(error, file = sys.stderr)
                await message.channel.send(error)
                await asyncio.sleep(self.errortime)
    
    async def on_serial(self):
        while True:
            try:
                if not self.device.is_open:
                    self.device = serial.Serial()
                    self.device.port = self.port
                    self.device.baudrate = self.baudrate
                    self.device.open()
                    if self.device.is_open:
                        print("Connected to " + str(self.port)
                              + " @ " + str(self.baudrate))
                if self.device.is_open and self.device.in_waiting:
                    data = ""
                    while self.device.in_waiting:
                        data += self.device.read().decode()
                    sys.stdout.write(data)
                    channel = self.get_channel(self.channelID)
                    if channel != None:
                        await channel.send(data)
                    else:
                        print("Channel Not Connected", file = sys.stderr)
            except Exception as error:
                self.device.close()
                print(error, file = sys.stderr)
                channel = self.get_channel(self.channelID)
                if channel != None:
                    await channel.send(message)
                else:
                    print("Channel Not Connected", file = sys.stderr)
                await asyncio.sleep(self.errortime)
            await asyncio.sleep(self.schedtime)

    async def test(self):
        while True:
            print("PING")
            channel = self.get_channel(self.channelID)
            if channel != None:
                await channel.send("ACK")
            else:
                print("NACK")
            await asyncio.sleep(self.errortime)

if __name__ == "__main__":
    main()
