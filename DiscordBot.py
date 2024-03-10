import DiscordClient
import messageProcessing

class DiscordBot():

    def __init__(self, token: str, mp: messageProcessing.MessageProcessor):
        self.client = DiscordClient.DiscordClient(mp)
        self.token = token

    def run(self):
        self.client.run(self.token)
