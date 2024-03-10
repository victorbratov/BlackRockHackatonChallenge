import discord
import messageProcessing


class DiscordClient(discord.Client):

    def __init__(self, mp: messageProcessing.MessageProcessor):
        self.mp = mp
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Bot {self.user} is ready")

    async def on_message(self, message: discord.Message):

        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            ans = self.mp.process_message(message.author.id, message.author.name, message.content)
            await message.author.send(ans)