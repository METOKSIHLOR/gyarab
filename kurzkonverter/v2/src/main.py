from kurz import get_data
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

def main():
    while True:
        vyber = input(Fore.CYAN + 'Stisknete "1" pokud chcete konvertovat z jine meny do CZK. '
                                'Pokud chcete konvertovat z CZK do jine meny stisknete "2".' +
            Fore.GREEN + '\n>>> ' + Style.RESET_ALL).strip()
        if vyber not in ['1', '2']:
            continue

        mena = input(Fore.YELLOW + "Zadejte prosim kod meny (napr. USD), se kterou chcete pracovat:" +
            Fore.GREEN + '\n>>> ' + Style.RESET_ALL).strip().upper()

        if vyber == "1":
            data = get_data(curr_from=mena, curr_to="CZK")
        else:
            data = get_data(curr_from="CZK", curr_to=mena)

        if "status" in data.keys() and data["status"] in [404, 422]:
            print(Fore.RED + "Zadal jste spatnou menu. Mena musi byt ve formatu ISO 4217, napr. USD. Zkuste jeste jednou")
            continue

        try:
            castka = float(input(Fore.BLUE + "Zadejte prosim castku meny, kterou chcete konvertovat" +
            Fore.GREEN + '\n>>> ' + Style.RESET_ALL).strip())
        except ValueError:
            print(Fore.RED + "Neplatna castka. Zkuste prosim jeste jednou")
            continue

        if castka < 0:
            print(Fore.RED + "Castka musi byt kladne cislo. Zkuste prosim jeste jednou")
            continue

        result = round(castka * data["rate"], 2)
        print(Fore.MAGENTA + f"Vysledna castka je {result} {data["quote"]}" + Style.BRIGHT)
        break


if __name__ == "__main__":
    main()