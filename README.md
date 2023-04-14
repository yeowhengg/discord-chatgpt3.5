# discord-gpt

A simple bot that takes a message from users to interact with chat gpt's api to send real time answer to the server.

Usuage:

git clone https://github.com/yeowhengg/discord-gpt.git
cd DiscordGPT_Bot
docker compose up --build

rename .env_example to .env and replace the values with yours.

For additional CHANNEL_NAME, you can choose to replace the single value to multiple channel names like CHANNEL_NAME = '["Foo", "bar"]'
use the JSON library to load it.

e.g.

import json
CHANNEL_NAME = json.loads(os.getenv("CHANNEL_NAME"))


