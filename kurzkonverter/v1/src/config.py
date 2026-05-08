from dataclasses import dataclass

from environs import Env

@dataclass
class API:
    url: str

@dataclass
class Config:
    api: API

def load_config():
    env = Env()
    env.read_env(path="kurzkonverter/v1/.env")
    return Config(api=API(url=env.str("API_URL")))

config = load_config()