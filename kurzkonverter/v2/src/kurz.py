import httpx
from config import config

res = httpx.get(config.api.url)
rows = res.text.split("\n")

rows = rows[2:-1]

def get_data(curr_to: str, curr_from: str):
    data = httpx.get(f"{config.api.url}/{curr_from}/{curr_to}")
    return data.json()
