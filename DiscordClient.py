import discord
import messageProcessing


class DiscordClient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Bot {self.user} is ready")

    async def on_message(self, message: discord.Message):

        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            if messageProcessing.message_is_command(message.content):
                await message.author.send(messageProcessing.process_command(message.content))
            else:
                await message.author.send("these are the avaliable commands:\n" + messageProcessing.process_command('/show_commands'))