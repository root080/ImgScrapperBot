# ImgScrapperBot
An application that uses `discord.py` async API to manage a Discord bot.

# Configuration
Create the `.env ` file in the script directory with the following format:
```
BOT_TOKEN=<your_token>
PEXELS_API_KEY=<your_key>
```
For more information regarding how to get the keys refer to **Discord Developer Portal** and **Pexels API Documentation**.
Then you can either run it directly on your machine (`./imgscrapperbot.py`) or in a container:
```
CONTAINER_NAME=<your_name> && docker build -t $CONTAINER_NAME . && docker run -d $CONTAINER_NAME
```

