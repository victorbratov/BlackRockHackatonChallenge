import discord

class DiscordClient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Bot {self.user} is ready")

    async def on_message(self, message):

        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            await message.channel.send('Hello!')
