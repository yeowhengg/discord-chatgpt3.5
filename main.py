import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        # only allow bot to read message from specific channel
        allowed_channel = str(self.get_channel(int(CHANNEL_NAME)))
        if message.channel.name != allowed_channel:
            return

        # client.user refers to the bot itself
        if message.author == client.user:
            return

        # Bots refer to the role name. change it to suit your server needs
        if "Bots" in [x.name for x in message.author.roles]:
            return

        if len(message.content) < 15:
            await message.channel.send("Please enter more more words to ask a question. Otherwise Yeow Heng is paying $0.002 for nothing haha")
            return
            
        async with message.channel.typing():
            print(f'Message from {message.author}: {message.content}')
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.content}]
            )
               
        await message.channel.send(response["choices"][0]["message"]["content"])

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(command_prefix = '/helloworld', intents=intents)
client.run(BOT_TOKEN)