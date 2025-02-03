import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID'))
    DB_PATH = 'database/'