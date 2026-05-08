from dataclasses import dataclass

from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@dataclass
class API:
    url: str

@dataclass
class Config:
    api: API

def load_config():
    env = Env()
    env_path = BASE_DIR / ".env"

    env.read_env(path=str(env_path))
    return Config(api=API(url=env.str("API_URL")))

config = load_config()