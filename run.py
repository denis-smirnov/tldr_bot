import telepot
from app import launch_bot
from os import environ

bot = telepot.Bot(environ['TELEGRAM_TOKEN'])
launch_bot(bot)
