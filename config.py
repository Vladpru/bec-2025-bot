from dataclasses import dataclass
from dotenv import load_dotenv 
import os

load_dotenv()

@dataclass 
class Config:
    bot_token: str = os.getenv("BOT_TOKEN")

def load_config():
    return Config()

