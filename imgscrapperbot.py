#! /usr/bin/python3

from requests_cache import CachedSession
from discord.ext import commands
from dotenv import load_dotenv
from io import BytesIO
import logging
import discord
import os

COMMAND_PREFIX = '/'
INTENTS = discord.Intents.default()

load_dotenv()

class ImgScrapperBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

        try:
            # Load environment variables
            self.token: str = os.environ['BOT_TOKEN']
            self.pexels_api_key: str = os.environ['PEXELS_API_KEY']
        except KeyError as e:
            raise KeyError(f'Environment variable {e} not set')

        self.cache = CachedSession('url_cache', expire_after=10000)

    # Get relevant image bytes from Pexels API
    def scraper(self, query: str) -> bytes:
        url = f'https://api.pexels.com/v1/search'
        headers = {'Authorization': self.pexels_api_key}
        params = {'query': query, 'per_page': 1}

        try:
            response: str = self.cache.get(url, headers=headers, params=params)
        except discord.HTTPException:
            return b'HTTPException: Could not get picture'

        picture_url = response.json()['photos'][0]['src']['original']
        return self.cache.get(picture_url).content

    @staticmethod
    def setup_logging(path: str = 'bot.log'):
        handler = logging.FileHandler(filename=path, encoding='utf-8')
        discord.utils.setup_logging(handler=handler)

# Bot setup
bot = ImgScrapperBot(COMMAND_PREFIX, INTENTS)
bot.setup_logging()


@bot.event
async def on_ready() -> None:
    logging.info(f'Logged in as {bot.user}')
    await bot.tree.sync()


@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error) -> None:
    _, title, description = str(error).split(':')
    await interaction.response.send_message(embed=discord.Embed(title=title, description=description, colour=discord.Colour.red()))


@bot.tree.command(name='search', description='Search for image based on query')
async def search(interaction: discord.Interaction, query: str) -> None:
    logging.info(f'Searching "{query}" image for {interaction.user}')
    await interaction.response.send_message(file=discord.File(BytesIO(bot.scraper(query)), filename='image.jpg'))


@bot.tree.command(name='dm', description='Share images with others')
async def dm(interaction: discord.Interaction, user: discord.Member, query: str) -> None:
    if not user:
        raise commands.UserNotFound(user.mention)

    logging.info(f'{interaction.user} sent "{query}" image to {user}')
    await user.send(file=discord.File(BytesIO(bot.scraper(query)), filename='image.jpg'))
    await interaction.response.send_message(embed=discord.Embed(title='Message sent', colour=discord.Colour.dark_green()))


if __name__ == '__main__':
    bot.run(bot.token, log_handler=None)
