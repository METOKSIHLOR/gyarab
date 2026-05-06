from pprint import pprint
from kurz import get_data
from colorama import Fore, Style, init

def sent_correct_currency(data, mena):
    if mena not in data.keys():
        return False
    return True

def konvertovat_do_czk(castka, mena, data):
    mnozstvi = float(data[mena]["mnozstvi"])
    kurz = data[mena]["kurz"]
    vysledek = round(castka / (mnozstvi / kurz), 2)
    print(Fore.GREEN + f"Vysledna castka je {vysledek} CZK" + Style.BRIGHT)

def konvertovat_z_czk(castka, mena, data):
    mnozstvi = float(data[mena]["mnozstvi"])
    kurz = data[mena]["kurz"]
    vysledek = round((mnozstvi / kurz) * castka, 2)
    print(Fore.GREEN + f"Vysledna castka je {vysledek} {mena}" + Style.BRIGHT)

def main():
    while True:
        vyber = input(Fore.CYAN + 'Stisknete "1" pokud chcete konvertovat z jine meny do CZK. '
                                'Pokud chcete konvertovat z CZK do jine meny stisknete "2".\n')

        if vyber not in ['1', '2']:
            print(Fore.RED + "Neplatna volba. Zkuste to znovu.")
            continue

        data = get_data()
        print(Fore.MAGENTA + "\nAktuální kurzy měn:\n")
        pprint(data)

        mena = input(Fore.YELLOW + "Zadejte prosim menu, se kterou chcete pracovat (např. USD):\n").upper()

        if not sent_correct_currency(data=data, mena=mena):
            print(Fore.RED + "Zadal jste spatnou menu. Zkuste prosim jeste jednou")
            continue

        try:
            castka = float(input(Fore.GREEN + "Zadejte castku meny, kterou chcete konvertovat:\n"))
        except ValueError:
            print(Fore.RED + "Neplatna castka. Zkuste prosim zadat cislo.")
            continue

        if castka < 0:
            print(Fore.RED + "Castka musi byt kladne cislo. Zkuste prosim jeste jednou")
            continue

        if vyber == "1":
            konvertovat_do_czk(castka=castka, mena=mena, data=data)
            break
        elif vyber == "2":
            konvertovat_z_czk(castka=castka, mena=mena, data=data)
            break


if __name__ == "__main__":
    main()