# Do zrobienia na pewno: (zrobisz to usuń)(wpadniesz na coś dopisz):
# 
#   - OPCJE (4, 10, 11) - do dokończenia
#   - Zarządzanie pracownikami - opcja dostępna tylko dla administratora
#       - Dodawanie pracowników (z generowaniem ID (jest już u zwierząt))
#       - (?) generowanie hasła
#       - Usuwanie pracowników
#       - (?) Modyfikowanie danych pracowników (np. zmiana stanowiska) 
#   - (?) Własne wyjątki
#   - Raporty (np. liczba zwierząt, liczba adopcji w danym miesiącu, itp.)
#   - Coś dla OsobyAdpotującej (metoda)
#   - Modyfikacja danych zwierząt (np. aktualizacja stanu zdrowia, itp.)
#
from schronisko import Schronisko
from osoby import Pracownik, OsobaAdoptujaca
from zwierzeta import Zwierze


def logowanie(schronisko):
    print("--- LOGOWANIE DO SYSTEMU ---")
    while True:
        id = input("Podaj ID pracownika: ").strip()
        haslo = input("Podaj hasło: ").strip()
        pracownik = schronisko.znajdz_pracownika_po_id(id)
        if pracownik and pracownik.zweryfikuj_haslo(haslo):
            print(f"Zalogowano. Witaj, {pracownik.imie} {pracownik.nazwisko} ({pracownik.stanowisko})!")
            return pracownik
        else:
            print("Niepoprawne ID lub hasło. Spróbuj ponownie.\n")


def uruchom_menu():
    moje_schronisko = Schronisko()
    moje_schronisko.wczytaj_dane() # Automatyczne wczytanie przy starcie
    
    if moje_schronisko.pracownicy == [] or moje_schronisko.pracownicy is None: # Jeśli brak pracowników, tworzymy konto admina
        print("\n[System] Baza pracowników pusta! Tworzenie konta administratora.")
        admin = Pracownik("Jan", "Kowalski", "90010112345", "555-666", "P01", "Administrator", "admin123")
        moje_schronisko.dodaj_pracownika(admin)
        moje_schronisko.zapisz_dane()
        print("Utworzono konto administratora (ID: P01, Hasło: admin123)\n")

    zalogowany_pracownik = logowanie(moje_schronisko)

    while True:
        print(f"\n--- SYSTEM ZARZĄDZANIA SCHRONISKIEM --- (Zalogowany jako: {zalogowany_pracownik.id})")
        print("0. Zapisz i Wyjdź")
        print("1. Wyświetl zwierzęta do adopcji")
        print("2. Wyświetl wszystkie zwierzęta")
        print("3. Filtruj zwierzęta")
        print("4. Zmień dane zwierzęcia")
        print("5. Wyświetl pracowników")
        print("6. Wyświetl klientów")
        print("7. Wyświetl historię adopcji")
        print("8. Przyjmij nowe zwierzę")
        print("9. Przeprowadź adopcję")
        print("10. Sprawdź historię zwierzęcia")

        if zalogowany_pracownik.stanowisko.lower() == "administrator":
            print("11. [ADMIN] Zarządzaj pracownikami")
            opcje_msg = "Wybierz opcję (1-11): "
        else:
            opcje_msg = "Wybierz opcję (1-10): "

        wybor = input(opcje_msg).strip()
        print("-" * 40)
        # ZWIERZĘTA DO ADOPCJI
        if wybor == "1":
            do_adopcji = moje_schronisko.filtruj_zwierzeta("status", "Do adopcji")
            if not do_adopcji:
                print("Brak zwierząt do adopcji.")
            else:
                print("-" * 150)
                print(f"{'ID':<4} | {'Gatunek':<8} | {'Rasa':<10} | {'Imię':<12} | {'Wiek':<4} | {'Stan zdrowia':<25} | {'Opis':<40} | {'Status':<15}")
                print("-" * 150)
                for z in do_adopcji:
                    print(z)

        # WSZYSTKIE ZWIERZĘTA
        elif wybor == "2":
            wszystkie = moje_schronisko.zwierzeta
            if not wszystkie:
                print("Brak zwierząt w schronisku.")
            else:
                print("-" * 150)
                print(f"{'ID':<4} | {'Gatunek':<8} | {'Rasa':<10} | {'Imię':<12} | {'Wiek':<4} | {'Stan zdrowia':<25} | {'Opis':<40} | {'Status':<15}")
                print("-" * 150)
                for z in wszystkie:
                    print(z)

        # FILTROWANIE ZWIERZĄT
        elif wybor == "3":
            while True:
                print("\n-- FILTROWANIE ZWIERZĄT --")
                print("1. Gatunek")
                print("2. Rasa")
                print("3. Imię")
                print("4. Wiek")
                print("5. Stan zdrowia")
                print("6. Status")
                print("7. Powrót do menu głównego")
                filtr_wybor = input("Wybierz kategorię (1-7): ").strip()
                
                if filtr_wybor == "6":
                    break
                elif filtr_wybor in ["1", "2", "3", "4", "5", "6"]:
                    kategorie = {"1": "gatunek", "2": "rasa", "3": "imie", "4": "wiek", "5": "stan_zdrowia", "6": "status"}
                    kategoria = kategorie[filtr_wybor]
                    wartosc = input(f"Podaj wartość dla {kategoria}: ").strip()
                    przefiltrowane = moje_schronisko.filtruj_zwierzeta(kategoria, wartosc)
                    if not przefiltrowane:
                        print(f"Brak zwierząt z {kategoria} '{wartosc}'.")
                    else:
                        print("-" * 150)
                        print(f"{'ID':<4} | {'Gatunek':<8} | {'Rasa':<10} | {'Imię':<12} | {'Wiek':<4} | {'Stan zdrowia':<25} | {'Opis':<40} | {'Status':<15}")
                        print("-" * 150)
                        for z in przefiltrowane:
                            print(z)
                else:
                    print("Niepoprawny wybór kategorii. Spróbuj ponownie.")
        
        # ZMIANA DANYCH ZWIERZĘCIA
        elif wybor == "4":
            continue
            # DO DOKOŃCZENIA

        # PRACOWNICY
        elif wybor == "5":
            pracownicy = moje_schronisko.pracownicy
            if not pracownicy:
                print("Brak pracowników w schronisku.")
            else:
                print("-" * 50)
                print(f"{'ID':<5} | {'Imię':<10} | {'Nazwisko':<15} | {'Stanowisko':<15}")
                print("-" * 50)
                for p in pracownicy:
                    print(p)

        # KLIENCI
        elif wybor == "6":
            klienci = moje_schronisko.klienci
            if not klienci:
                print("Brak klientów w systemie.")
            else:
                print("-" * 100)
                print(f"{'PESEL':<11} | {'Imię':<10} | {'Nazwisko':<15} | {'Telefon':<15} | {'Warunki mieszkaniowe':<20} | {'Inne zwierzęta':<15}")
                print("-" * 100)
                for k in klienci:
                    print(k)

        # HISTORIA ADOPCJI
        elif wybor == "7":
            historia = moje_schronisko.historia_adopcji
            if not historia:
                print("Brak historii adopcji.")
            else:
                print("-" * 80)
                print(f"{'Data':<15} | {'ID Zwierzęcia':<15} | {'PESEL Osoby':<15} | {'ID Pracownika':<15}")
                print("-" * 80)
                for a in historia:
                    print(a)

        # DODANIE NOWEGO ZWIERZĘCIA
        elif wybor == "8":
            print("Wpisz dane nowego zwierzęcia:")
            # Blok try-except wyłapie błędy parsowania int lub błędy walidacji z klasy Zwierze
            try:
                id_z = f"Z{int(moje_schronisko.zwierzeta[-1].id[1:]) + 1}" if moje_schronisko.zwierzeta else "Z01" # Generowanie ID (autoinkrementacja)
                gatunek = input("Gatunek (np. Pies): ").strip()
                rasa = input("Rasa: ").strip()
                imie = input("Imię: ").strip()
                wiek = input("Wiek: ").strip()
                opis = input("Opis zachowania: ").strip()
                stan = input("Stan zdrowia: ").strip()

                # Próba utworzenia obiektu (tu może wyskoczyć ValueError)
                nowe_z = Zwierze(id_z, gatunek, rasa, imie, wiek, opis, stan, "Zapisany w systemie")
                moje_schronisko.dodaj_zwierze(nowe_z)
                nowe_z.zmien_status(zalogowany_pracownik, "Do adopcji") # Dodaj wpis do historii statusu
                print(f"Sukces! Dodano zwierzę {imie}.")

            except ValueError as e:
                print(f"\n[BŁĄD DANYCH]: Nie udało się dodać zwierzęcia. Powód: {e}")
            except Exception as e:
                print(f"\n[NIEOCZEKIWANY BŁĄD]: {e}")


        elif wybor == "9":
            id_z = input("Podaj ID zwierzęcia do adopcji: ").strip()
            zwierze = moje_schronisko.znajdz_zwierze_po_id(id_z)
            
            if not zwierze:
                print(f"Nie znaleziono zwierzęcia o ID: {id_z}")
                continue
            
            pesel_o = input("Podaj PESEL osoby adoptującej: ").strip()
            klient = moje_schronisko.znajdz_klienta_po_peselu(pesel_o)
            if klient:
                print(f"Znaleziono klienta: {klient.imie} {klient.nazwisko} (PESEL: {klient.pesel})")
            else:
                print("[SYSTEM] Nowy klient. Podaj pozostałe dane:")
                imie_o = input("Imię: ").strip()
                nazw_o = input("Nazwisko: ").strip()
                tel_o = input("Telefon: ").strip()
                warunki = input("Warunki mieszkaniowe (np. Mieszkanie, Dom): ").strip()
                inne = input("Czy są inne zwierzęta w domu? (Tak/Nie): ").strip()
                try: 
                    # Próba utworzenia klienta (tu może paść błąd złego PESELu)
                    klient = OsobaAdoptujaca(imie_o, nazw_o, pesel_o, tel_o, warunki, inne)
                    moje_schronisko.dodaj_klienta(klient)
                except ValueError as e:
                    print(f"\n[BŁĄD DANYCH KLIENTA]: Operacja przerwana. Powód: {e}")
                    continue
            try:
                # Próba adopcji (tu może paść błąd, jeśli zwierzę jest już adoptowane)
                wynik = moje_schronisko.adopcja(zwierze, klient, zalogowany_pracownik)
                print(wynik)
            except ValueError as e:
                print(f"\n[BŁĄD ADOPCJI]: {e}")

        # HISTORIA ZWIERZĘCIA
        elif wybor == "10":
            # DO DOKOŃCZENIA
            continue

        # ZAPIS I WYJŚCIE
        elif wybor == "0":
            moje_schronisko.zapisz_dane()
            print("Zamykanie programu. Do widzenia!")
            break

        elif wybor == "11" and zalogowany_pracownik.stanowisko.lower() == "administrator":
            print("\n [ADMIN] ZARZĄDZANIE PRACOWNIKAMI")
            # DO DOKOŃCZENIA

        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


if __name__ == "__main__":
    uruchom_menu()
