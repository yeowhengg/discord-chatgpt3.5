import discord
from dotenv import load_dotenv
import os
import openai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

class MyClient(discord.Client):
    async def on_ready(self):
        self.token = 0
        self.memory = {}
    
    async def on_message(self, message):
        # only allow bot to read message from specific channel
        allowed_channel = str(self.get_channel(int(CHANNEL_NAME)))
        if message.channel.name != allowed_channel:
            return

        # client.user refers to the bot itself
        if message.author == client.user:
            return
        
        self.memory.update(
            {
                message.author: {
                    "memory": [],
                    "answer_memory": []
                }
            }) if message.author not in self.memory else None

        # Bots refer to the role name. change it to suit your server needs
        if "Bots" in [x.name for x in message.author.roles]:
            return

        if message.content == "restart":
            self.memory[message.author]["memory"] = []
            self.memory[message.author]["answer_memory"] = []

        if len(message.content) < 15 or message.content.count(" ") < 3:
            await message.channel.send("Please enter more more words to ask a question. Otherwise Yeow Heng is paying $0.002 for nothing haha")
            return
        

        async with message.channel.typing():
            self.memory[message.author]["memory"].append(message.content)
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "In the event you do not know the answer, do not answer it with 'I am just a language model' or anything similar. Leave out those sentence and answer what you know. "},
            {"role": "user", "content": message.content}, 
            {"role": "assistant", "content": "".join(self.memory[message.author]["memory"])},
            {"role": "assistant", "content": "".join(self.memory[message.author]["answer_memory"])},
            ]
            )

            self.memory[message.author]["answer_memory"].append(response["choices"][0]["message"]["content"])
            self.token += response["usage"]["total_tokens"]
            print(f"total token used so far: {self.token}")

        await message.channel.send(response["choices"][0]["message"]["content"], reference=message)
        await message.channel.send("\nType restart to clear the chat's memory")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)