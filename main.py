# bot.py
import os

from dotenv import load_dotenv
import DiscordBot
import DiscordClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_PATH = os.getenv('DB_PATH')
print(TOKEN)

client = DiscordClient.DiscordClient()
bot = DiscordBot.DiscordBot(TOKEN)


if __name__ == "__main__":
    bot.run()
