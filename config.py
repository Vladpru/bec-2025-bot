from dataclasses import dataclass
from dotenv import load_dotenv 
import os

load_dotenv()

@dataclass
class Config:
    bot_token: str
    admin: str
    mongo_uri: str 

def load_config():
    return Config(
        bot_token=os.getenv("BOT_TOKEN"),
        admin=os.getenv("ADMIN"),
        mongo_uri=os.getenv("DBMONGO_URL"),
    )
