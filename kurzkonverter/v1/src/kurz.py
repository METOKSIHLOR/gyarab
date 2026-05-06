import httpx
from config import config

res = httpx.get(config.api.url)
rows = res.text.split("\n")

rows = rows[2:-1]

def get_data():
    data = {}
    for r in rows:
        cols = r.split("|")
        mena = cols[-2]
        mnozstvi = cols[-3]
        kurz = float(cols[-1].replace(",", "."))
        data[mena] = {"kurz": kurz, "mnozstvi": int(mnozstvi)}
    return data
