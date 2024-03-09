import DiscordClient
import discord

class DiscordBot():

    def __init__(self, token: str):
        self.client = DiscordClient.DiscordClient()
        self.token = token

    def run(self):
        self.client.run(self.token)
