import discord
from dotenv import load_dotenv
import os
import openai
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        # client.user refers to the bot itself
        if message.author == client.user:
            return

        # Bots refer to the role name. change it to suit your server needs
        if "Bots" in [x.name for x in message.author.roles]:
            return

        async with message.channel.typing():
            print(f'Message from {message.author}: {message.content}')
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.content}]
            )
               
        await message.channel.send(response["choices"][0]["message"]["content"])
    
    async def typing(ctx):
        async with ctx.typing():
            await asyncio.sleep(2)
        
        await ctx.send("Done typing")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)