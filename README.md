# Projekty pro přijímací zkoušky na Gymnázium Arabská

Tento repozitář byl vytvořen jako ukázka programátorských dovedností autora v rámci přípravy na srovnávací zkoušky na Gymnázium Arabská.

Repozitář obsahuje tři samostatné projekty:

1. **Konvertor měn v příkazové řádce**
2. **Hra Pexeso**
3. **Jednoduchý Cat Clicker vytvořený v Django**

---

# Instalace

Před spuštěním kteréhokoliv projektu doporučuji nainstalovat potřebné závislosti:

```bash
pip install -r requirements.txt
```
# 1. Konvertor měn

Aplikace slouží ke konverzi měn v příkazové řádce.

Projekt obsahuje dvě verze:

- **v1** — používá externí API poskytnuté vyučujícím
- **v2** — používá API vybrané autorem repozitáře a implementované speciálně pro něj

## Rychlé spuštění

Připravte .env: 

```bash
cp kurzkonverter/{v1 nebo v2}/.env_example kurzkonverter/{v1 nebo v2}/.env
```

Spusťte aplikaci:

```bash
python kurzkonverter/{v1 nebo v2}/src/main.py
```

---

# 2. Pexeso

Jednoduchá implementace populární paměťové hry Pexeso.

## Funkce

- 2 úrovně obtížnosti
- 2 různé vzhledy karet
- možnost nastavení počtu dvojic

## Rychlé spuštění

Otevřete soubor:

```text
pexeso/index.html
```

v libovolném webovém prohlížeči.

---

# 3. Cat Clicker (Django projekt)

Jednoduchá hra inspirovaná Cookie Clickerem vytvořená pomocí frameworku Django.

## Funkce

- registrace a přihlášení uživatelů
- obchod s vylepšeními
- pasivní získávání bodů
- systém upgradů

## Rychlé spuštění

```bash
docker-compose up --build
```

Aplikace bude spuštěna na portu http://127.0.0.1:8000/ nebo http://localhost:8000/.

---

# Použité technologie

- Python
- Django
- Redis
- SQLite
- HTML / CSS / JavaScript
- Docker
- REST API

---

# Autor

Projekt byl vytvořen jako studijní a demonstrační portfolio.


