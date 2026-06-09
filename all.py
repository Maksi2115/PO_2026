import datetime
from abc import ABC, abstractmethod
import json
import datetime
import os
import random

class Zwierze():
    def __init__(self, id, gatunek, rasa, imie, wiek, opis, stan_zdrowia, status, historia=None):
        if not str(id).strip():
            raise ValueError("ID zwierzęcia nie może być puste!")
        if not imie.strip():
            raise ValueError("Imię zwierzęcia nie może być puste!")
        if int(wiek) < 0:
            raise ValueError("Wiek zwierzęcia nie może być ujemny!")
        
        self.__id = id
        self.__gatunek = gatunek
        self.__rasa = rasa
        self.__imie = imie
        self.__wiek = int(wiek)
        self.__opis = opis
        self.__stan_zdrowia = stan_zdrowia
        self.__status = status
        self.__historia = historia if historia is not None else []   

    def get_info(self):
        message = f"ID: {self.__id}, {self.__gatunek} {self.__rasa} o imieniu {self.__imie}, {self.__wiek} lat, {self.__stan_zdrowia} {self.__opis}, obecnie: {self.__status}"
        return message
    
    def __str__(self):
        opis = self.__opis if len(self.__opis) <= 37 else self.__opis[:37] + "..."
        return f"{str(self.__id):<4} | {self.__gatunek:<8} | {self.__rasa:<10} | {self.__imie:<12} | {str(self.__wiek):<4} | {self.__stan_zdrowia:<25} | {opis:<40} | {self.__status:<15}"
    

    def zmien_status(self, pracownik, nowy_status):
        data = datetime.datetime.now()
        wpis = Wpis(data, self.__status, nowy_status, pracownik.id)
        self.__status = nowy_status
        self.__historia.append(wpis)
        print(wpis)

    @property
    def id(self):
        return self.__id
    
    @property
    def imie(self):
        return self.__imie
    
    @property
    def historia(self):
        return self.__historia

    @property
    def status(self):
        return self.__status
    
    def ustaw_stan_zdrowia(self, nowy_stan):
        self.__stan_zdrowia = nowy_stan

    def ustaw_opis(self, nowy_opis):
        self.__opis = nowy_opis

    def ustaw_wiek(self, nowy_wiek):
        if int(nowy_wiek) < 0:
            raise ValueError("wiek zwierzęcie nie morez być ujemny")
        self.__wiek = int(nowy_wiek)

    def to_dict(self):
        return {
            "id": self.__id, "gatunek": self.__gatunek, "rasa": self.__rasa,
            "imie": self.__imie, "wiek": self.__wiek, "opis": self.__opis,
            "stan_zdrowia": self.__stan_zdrowia, "status": self.__status,
            "historia": [w.to_dict() for w in self.__historia]
        }

    @classmethod
    def from_dict(cls, d):
        historia = [Wpis.from_dict(w) for w in d.get("historia", [])]
        return cls(d["id"], d["gatunek"], d["rasa"], d["imie"], d["wiek"], d["opis"], d["stan_zdrowia"], d["status"], historia)


class Adopcja():
    def __init__(self, data, zwierze_id, nowy_wlasciciel_pesel, pracownik_id=None):
        self.__data, self.__zwierze_id, self.__nowy_wlasciciel_pesel, self.__pracownik_id = data, zwierze_id, nowy_wlasciciel_pesel, pracownik_id

    def __str__(self):
        return f"{str(self.__data):<15} | {self.__zwierze_id:<15} | {self.__nowy_wlasciciel_pesel:<15} | {str(self.__pracownik_id):<15}"

    def to_dict(self):
        return {
            "data": self.__data, "zwierze_id": self.__zwierze_id,
            "nowy_wlasciciel_pesel": self.__nowy_wlasciciel_pesel, "pracownik_id": self.__pracownik_id
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(d["data"], d["zwierze_id"], d["nowy_wlasciciel_pesel"], d.get("pracownik_id"))

class Wpis():
    def __init__(self, data, stary_status, nowy_status, pracownik_id):
        self.__data, self.__stary_status, self.__nowy_status, self.__pracownik_id = data, stary_status, nowy_status, pracownik_id

    @property
    def data(self):
        return self.__data
    
    @property
    def stary_status(self):
        return self.__stary_status
    
    @property
    def nowy_status(self):
        return self.__nowy_status
    
    @property
    def pracownik_id(self):
        return self.__pracownik_id

    def __str__(self):
        message = f"{self.__data:%Y-%m-%d %H:%M:%S} - zmiana statusu z `{self.__stary_status}` na `{self.__nowy_status}`, wykonana przez pracownika {self.__pracownik_id}"    
        return message
    
    def to_dict(self):
        return {
            "data": self.__data, "stary_status": self.__stary_status,
            "nowy_status": self.__nowy_status, "pracownik_id": self.__pracownik_id
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(d["data"], d["stary_status"], d["nowy_status"], d["pracownik_id"])
    

class Osoba(ABC):
    def __init__(self, imie, nazwisko, pesel, telefon):
        if len(str(pesel)) != 11 or not str(pesel).isdigit():
            raise ValueError("PESEL musi mieć 11 znaków!")
        if not imie.strip() or not nazwisko.strip():
            raise ValueError("Imię i nazwisko nie mogą być puste!")
        self.__imie = imie
        self.__nazwisko = nazwisko
        self.__pesel = pesel
        self.__telefon = telefon

    @abstractmethod
    def typ_osoby(self):
        pass
    
    @property
    def imie(self):
        return self.__imie
    
    @property
    def nazwisko(self):
        return self.__nazwisko
    
    @property
    def pesel(self):
        return self.__pesel
    
    @property
    def telefon(self):
        return self.__telefon
    

class OsobaAdoptujaca(Osoba):
    def __init__(self, imie, nazwisko, pesel, telefon, warunki_mieszkaniowe, inne_zwierzeta):
        super().__init__(imie, nazwisko, pesel, telefon)
        self.__warunki_mieszkaniowe = warunki_mieszkaniowe
        self.__inne_zwierzeta = inne_zwierzeta

    def __str__(self):
        return f"{self.pesel:<11} | {self.imie:<10} | {self.nazwisko:<15} | {self.telefon:<15} | {self.__warunki_mieszkaniowe:<20} | {self.__inne_zwierzeta:<15}"
    
    def typ_osoby(self):
        return "Osoba Adoptujaca"
    
    def to_dict(self):
        return {
            "imie": self.imie, "nazwisko": self.nazwisko, "pesel": self.pesel,
            "telefon": self.telefon, "warunki_mieszkaniowe": self.__warunki_mieszkaniowe,
            "inne_zwierzeta": self.__inne_zwierzeta
        }
    
    def czy_moze_adoptowac(self):
        warunki = self.__warunki_mieszkaniowe.lower()

        if 'ulica' in warunki or 'brak' in warunki:
            return False, 'Nie odpowedznie warunki mieszkaniowe'
        
        if int(self.__inne_zwierzeta) > 3:
            return False, 'Posiada juz zbyt duzo zwierzat'
    
        return True, 'Spelnia kryteria adopcji'
        
    
    @classmethod
    def from_dict(cls, d):
        return cls(d["imie"], d["nazwisko"], d["pesel"], d["telefon"], d["warunki_mieszkaniowe"], d["inne_zwierzeta"])
    
 
class Pracownik(Osoba):
    def __init__(self, imie, nazwisko, pesel, telefon, id, stanowisko, haslo):
        super().__init__(imie, nazwisko, pesel, telefon)
        self.__id = id
        self.__stanowisko = stanowisko
        self.__haslo = haslo
    
    @property
    def id(self):
        return self.__id
    
    @property
    def stanowisko(self):
        return self.__stanowisko
    
    def ustaw_imie(self, nowe_imie):
        self.__imie = nowe_imie

    def ustaw_nazwisko(self, nowe_nazwisko):
        self.__nazwisko = nowe_nazwisko

    def ustaw_pesel(self, nowy_pesel):
        self.__pesel = nowy_pesel

    def ustaw_telefon(self, nowy_numer):
        self.__telefon = nowy_numer

    def ustaw_stanowisko(self, nowe_stanowisko):
        if not nowe_stanowisko.strip():
            raise ValueError("Stanowisko nie moze byc puste")
        self.__stanowisko = nowe_stanowisko

    def ustaw_haslo(self, nowe_haslo):
        self.__haslo = nowe_haslo
    
    def __str__(self):
        return f"{self.__id:<5} | {self.imie:<10} | {self.nazwisko:<15} | {self.stanowisko:<15}"
    
    def __repr__(self):
        return f"Pracownik(ID: {self.__id}, Imię: {self.imie}, Nazwisko: {self.nazwisko}, Stanowisko: {self.stanowisko})"
    
    def typ_osoby(self):
        return "Pracownik"
    
    def zweryfikuj_haslo(self, podane_haslo):
        return self.__haslo == podane_haslo
    
    def to_dict(self):
        return {
            "imie": self.imie, "nazwisko": self.nazwisko, "pesel": self.pesel,
            "telefon": self.telefon, "id_pracownika": self.__id, "stanowisko": self.__stanowisko, "haslo": self.__haslo
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(d["imie"], d["nazwisko"], d["pesel"], d["telefon"], d["id_pracownika"], d["stanowisko"], d["haslo"])


class Schronisko():
    def __init__(self, zwierzeta=None, pracownicy=None, historia_adopcji=None):
        self.__zwierzeta = zwierzeta if zwierzeta is not None else []
        self.__pracownicy = pracownicy if pracownicy is not None else []
        self.__historia_adopcji = historia_adopcji if historia_adopcji is not None else []
        self.__klienci = []

    @property
    def zwierzeta(self):
        return self.__zwierzeta
    
    @property
    def pracownicy(self):
        return self.__pracownicy
    
    @property
    def klienci(self):
        return self.__klienci
    
    @property
    def historia_adopcji(self):
        return self.__historia_adopcji

    def dodaj_zwierze(self, zwierze):
        if not isinstance(zwierze, Zwierze):
            raise TypeError("Możesz dodać tylko obiekt klasy Zwierze!")
        self.__zwierzeta.append(zwierze)
        print(f"Dodano zwierze: {zwierze.get_info()}")
    
    def dodaj_pracownika(self, pracownik):
        if not isinstance(pracownik, Pracownik):
            raise TypeError("Możesz dodać tylko obiekt klasy Pracownik!")
        self.__pracownicy.append(pracownik)
        print(f"Dodano pracownika: {pracownik.__repr__()}")

    def usun_pracownika(self, pracownik):
        if not pracownik in self.__pracownicy:
            raise TypeError("Nie ma takiego pracownika")
        self.__pracownicy.remove(pracownik)
        print(f'[SYSTEM] Usunieto pracownika: {pracownik.imie} {pracownik.nazwisko}')

    def dodaj_klienta(self, klient):
        if not isinstance(klient, OsobaAdoptujaca):
            raise TypeError("Możesz dodać tylko obiekt klasy OsobaAdoptujaca!")
        self.__klienci.append(klient)
        print(f"Dodano klienta: {klient}")

    def filtruj_zwierzeta(self, kategoria, wartosc):
        przefiltrowane_zwierzeta = []
        for z in self.__zwierzeta:
            dane = z.to_dict()
            if str(dane.get(kategoria, "")).lower() == str(wartosc).lower():
                przefiltrowane_zwierzeta.append(z)
        return przefiltrowane_zwierzeta

    def znajdz_zwierze_po_id(self, id_zwierzecia):
        for z in self.__zwierzeta:
            if str(z.id) == str(id_zwierzecia):
                return z
        return None
    
    def znajdz_pracownika_po_id(self, id_pracownika):
        for p in self.__pracownicy:
            if str(p.id) == str(id_pracownika):
                return p
        return None
    
    def znajdz_klienta_po_peselu(self, pesel):
        for k in self.__klienci:
            if str(k.pesel) == str(pesel):
                return k
        return None
    
    def adopcja(self, zwierze, osoba, zalogowany_pracownik, data=None):
        moze_adoptowac, powod = osoba.czy_moze_adoptowac()
        if not moze_adoptowac:
            return f'Adopcja niemozliwa. Powod {powod}'

        if data is None:
            data = datetime.datetime.now()
        if zwierze.status.lower() == "adoptowane":
            raise ValueError(f"Zwierzę o ID {zwierze.id} zostało już wcześniej adoptowane!")
        adopcja = Adopcja(data, zwierze.id, osoba.pesel, zalogowany_pracownik.id)
        self.__historia_adopcji.append(adopcja)
        zwierze.zmien_status(zalogowany_pracownik, "Adoptowany")
        return "Adopcja przebiegła pomyślnie!"

    def zapisz_dane(self):
        try:
            dane_do_zapisu = {
                "zwierzeta": [z.to_dict() for z in self.__zwierzeta],
                "pracownicy": [p.to_dict() for p in self.__pracownicy],
                "klienci": [k.to_dict() for k in self.__klienci],
                "adopcje": [a.to_dict() for a in self.__historia_adopcji]
            }
            with open("baza.json", "w", encoding="utf-8") as f:
                json.dump(dane_do_zapisu, f, indent=4, ensure_ascii=False)
            print("[SYSTEM] Dane zostały zapisane.")
        except Exception as e:
            print(f"[[SYSTEM] Błąd zapisu pliku]: {e}")

    def wczytaj_dane(self):
        if not os.path.exists("baza.json"):
            print("[SYSTEM] Brak pliku z danymi.")
            return
        try:
            with open("baza.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            self.__zwierzeta = [Zwierze.from_dict(z) for z in dane.get("zwierzeta", [])]
            self.__pracownicy = [Pracownik.from_dict(p) for p in dane.get("pracownicy", [])]
            self.__klienci = [OsobaAdoptujaca.from_dict(k) for k in dane.get("klienci", [])]
            self.__historia_adopcji = [Adopcja.from_dict(a) for a in dane.get("adopcje", [])]
            print(f"[SYSTEM] Wczytano {len(self.__zwierzeta)} zwierząt z pliku. {len(self.__pracownicy)} pracowników. {len(self.__klienci)} klientów. {len(self.__historia_adopcji)} adopcji.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[[SYSTEM] Błąd struktury danych pliku]: {e}")
        except Exception as e:
            print(f"[[SYSTEM] Błąd odczytu pliku]: {e}")

    def generuj_raport(self):
        liczba_psow = 0
        liczba_kotow = 0

        do_adopcji = 0
        w_leczeniu = 0
        kwarantanna = 0
        adoptowane = 0

        for zwierzak in self.__zwierzeta:
            dane = zwierzak.to_dict()

            if dane['gatunek'].lower() == 'pies':
                liczba_psow += 1
            elif dane['gatunek'].lower() == 'kot':
                liczba_kotow += 1
            
            if zwierzak.status.lower() == 'do adopcji':
                do_adopcji += 1
            elif zwierzak.status.lower() == 'w leczeniu':
                w_leczeniu += 1
            elif zwierzak.status.lower() == 'kwarantanna':
                kwarantanna += 1
            elif zwierzak.status.lower() == 'adoptowane':
                adoptowane += 1 
            
        adopcja_styczen = 0
        adopcja_luty = 0
        adopcja_marzec = 0
        adopcja_kwiecien = 0
        adopcja_maj = 0
        adopcja_czerwiec = 0
        adopcja_lipiec = 0
        adopcja_sierpien = 0
        adopcja_wrzesien = 0
        adopcja_pazdziernik = 0
        adopcja_listopad = 0
        adopcja_grudzien = 0

        for adopcja in self.__historia_adopcji:
            dane_adopcji = adopcja.to_dict()
            data = dane_adopcji['data']

            if "2026-01" in str(data):
                adopcja_styczen += 1
            elif "2026-02" in str(data):
                adopcja_luty += 1
            elif "2026-03" in str(data):
                adopcja_marzec += 1
            elif "2026-04" in str(data):
                adopcja_kwiecien += 1
            elif "2026-05" in str(data):
                adopcja_maj += 1
            elif "2026-06" in str(data):
                adopcja_czerwiec += 1
            elif "2026-07" in str(data):
                adopcja_lipiec += 1
            elif "2026-08" in str(data):
                adopcja_sierpien += 1
            elif "2026-09" in str(data):
                adopcja_wrzesien += 1
            elif "2026-10" in str(data):
                adopcja_pazdziernik += 1
            elif "2026-11" in str(data):
                adopcja_listopad += 1
            elif "2026-12" in str(data):
                adopcja_grudzien += 1            

        raport = "---------------------------------------------------\n"
        raport += "                RAPORT SCHRONISKA\n"
        raport += "---------------------------------------------------\n"
        raport += f"Ogólna liczba zwierząt: {len(self.__zwierzeta)}\n"
        raport += f" - Psy: {liczba_psow}\n"
        raport += f" - Koty: {liczba_kotow}\n\n"
        raport += "---------------------------------------------------\n"
        raport += "Statusy zwierząt:\n"
        raport += f" - Do adopcji: {do_adopcji}\n"
        raport += f" - W leczeniu: {w_leczeniu}\n"
        raport += f" - Kwarantanna: {kwarantanna}\n"
        raport += f" - Adoptowane: {adoptowane}\n\n"
        raport += "---------------------------------------------------\n"
        raport += "Adopcje w roku 2026:\n"
        raport += f" - Styczen: {adopcja_styczen}\n"
        raport += f" - Luty: {adopcja_luty}\n"
        raport += f" - Marzec: {adopcja_marzec}\n"
        raport += f" - Kwiecien: {adopcja_kwiecien}\n"
        raport += f" - Maj: {adopcja_maj}\n"
        raport += f" - Czerwiec: {adopcja_czerwiec}\n"
        raport += f" - Lipiec: {adopcja_lipiec}\n"
        raport += f" - Sierpien: {adopcja_sierpien}\n"
        raport += f" - Wrzesien: {adopcja_wrzesien}\n"
        raport += f" - Pazdziernik: {adopcja_pazdziernik}\n"
        raport += f" - Listopad: {adopcja_listopad}\n"
        raport += f" - Grudzien: {adopcja_grudzien}\n"
        raport += "---------------------------------------------------\n"

        print('Raport wygenerowano pomyslnie')

        with open("raport.txt", "w", encoding="utf-8") as plik:
            plik.write(raport)


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
        print("11. Wygeneruj raport")

        if zalogowany_pracownik.stanowisko.lower() == "administrator":
            print("12. [ADMIN] Zarządzaj pracownikami")
            opcje_msg = "Wybierz opcję (1-12): "
        else:
            opcje_msg = "Wybierz opcję (1-11): "

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
                
                if filtr_wybor == "7":
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
            print('Edycja zwierzaków')
            id_zwierzaka = input('Podaj id zwierzaka, ktorego chcezsz edytowac: ')
            zwierzak_szukany = moje_schronisko.znajdz_zwierze_po_id(id_zwierzaka)

            if not zwierzak_szukany:
                print(f'Nie znaleziono zwierzaka o id {id_zwierzaka}')
                continue

            print(f'Wybrano: {zwierzak_szukany.imie} (ID: {zwierzak_szukany.id})')
            print('1. Zmień stan zdrowia')
            print('2. Zmień opis')
            print('3. Zmień wiek')
            print('4. Zmień status')# z zapisem do historii
            print('5. Powrót')

            wybor_edycji = input("Wybierz opcje edycji zwierzaka: ").strip()

            try:
                if wybor_edycji == '1':
                    nowy_stan = input('Podaj nowy stan zdrowia: ').strip()
                    if nowy_stan:
                        zwierzak_szukany.ustaw_stan_zdrowia(nowy_stan)
                    else:
                        print("Wartość nie może być pusta!")
                        
                elif wybor_edycji == "2":
                    nowy_opis = input("Podaj nowy opis: ").strip()
                    if nowy_opis:
                        zwierzak_szukany.ustaw_opis(nowy_opis)
  
                    else:
                        print("Wartość nie może być pusta!")
                        
                elif wybor_edycji == "3":
                    nowy_wiek = input("Podaj nowy wiek: ").strip()
                    zwierzak_szukany.ustaw_wiek(nowy_wiek)
                    
                elif wybor_edycji == "4":
                    nowy_status = input("Podaj nowy status (np. Kwarantanna, W leczeniu, Do adopcji): ").strip()
                    if nowy_status:
                        zwierzak_szukany.zmien_status(zalogowany_pracownik, nowy_status)
                    else:
                        print("Status nie może być pusty!")

                print(f"Pomyślnie zaktualizowano.")
                moje_schronisko.zapisz_dane()   
            except ValueError as error:
                print(f"\n[BŁĄD WALIDACJI]: {error}")
            except Exception as error:
                print(f"\n[NIEOCZEKIWANY BŁĄD]: {error}")

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
                nowe_z = Zwierze(id_z, gatunek, rasa, imie, wiek, opis, stan, "Nowy")
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
            if len(pesel_o) != 11 or not pesel_o.isdigit():
                print("Niepoprawny PESEL. PESEL musi składać się z 11 cyfr.")
                continue
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
                inne_bool = 0 if inne.lower() == "nie" else 1
                try: 
                    # Próba utworzenia klienta (tu może paść błąd złego PESELu)
                    klient = OsobaAdoptujaca(imie_o, nazw_o, pesel_o, tel_o, warunki, inne_bool)
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
            historia_zwierzaka = moje_schronisko.zwierzeta
            id_zwierzaka = input("Podaj id zwierzaka: ").strip()
            zwierzak_szukany = moje_schronisko.znajdz_zwierze_po_id(id_zwierzaka)
            
            if zwierzak_szukany is None: 
                print('Nie znaleziono takie zwirzaka')           
            else:
                if not zwierzak_szukany.historia:
                    print(f"Zwierzak: {zwierzak_szukany.id}, {zwierzak_szukany.imie} nie ma histroii")
                else:
                    print(f"Historia: {zwierzak_szukany.imie}")
                    print('-'*40)
                    
                    for wpis in zwierzak_szukany.historia:
                        print(f'Data: {wpis.data}')
                        print(f'Stary status: {wpis.stary_status}')
                        print(f'Nowy status: {wpis.nowy_status}')
                        print(f'Pracownik: {wpis.pracownik_id}')
                        print('-'*40)

        # GENEROWANIE RAPORTU                
        elif wybor == "11":
            moje_schronisko.generuj_raport()

        # ZAPIS I WYJŚCIE
        elif wybor == "0":
            moje_schronisko.zapisz_dane()
            print("Zamykanie programu. Do widzenia!")
            break

        elif wybor == "12" and zalogowany_pracownik.stanowisko.lower() == "administrator":
            print("\n [ADMIN] ZARZĄDZANIE PRACOWNIKAMI")
            
            print("1. Dodaj pracownika")
            print("2. Edycja pracownika")
            print("3. Usun pracownika")

            wybor_admina = input("Wybierz kategorie: ")
            if wybor_admina == '1':
                print('Wpisz dane nowego pracownika')
                try:
                    imie_pracownika = input("Podaj imie pracownika ")
                    nazwisko_pracownika = input("Podaj nazwisko pracownika: ")
                    pesel_pracownika = input("Podaj pesel pracwonika: ")
                    telefon_pracownika = input("Podaj numer telefonu pracownika: ")
                    id_pracownika = f"P{int(moje_schronisko.pracownicy[-1].id[1:])+1}" if moje_schronisko.pracownicy else "P01"
                    stanowisko_pracownika = input("Podaj stanowisko pracownika: ")
                    liczby = "".join(str(x) for x in random.choices(range(1, 10), k=3))
                    nazwa = stanowisko_pracownika.lower().strip()[:3]
                    haslo_pracownika = f"{nazwa}{liczby}"

                    nowy = Pracownik(imie_pracownika, nazwisko_pracownika, pesel_pracownika, telefon_pracownika, id_pracownika, stanowisko_pracownika, haslo_pracownika)

                    moje_schronisko.dodaj_pracownika(nowy)
                    moje_schronisko.zapisz_dane()
                    print(f"Utworzono nowego pracownika: ID: {id_pracownika}, Hasło: {haslo_pracownika}")
                except ValueError as error:
                    print(f"\n[BŁĄD DANYCH]: Nie udało się dodać pracownika. Powód: {error}")
                except Exception as error:
                    print(f"\n[NIEOCZEKIWANY BŁĄD]: {error}")
                
            if wybor_admina == '2':
                print('Edycja pracownikow')
                wybor_edycji_id = input('Podaj id pracownika do edycj: ').strip()
                pracownik_do_edycji = moje_schronisko.znajdz_pracownika_po_id(wybor_edycji_id)

                if not pracownik_do_edycji:
                    print(f"Nie ma takiego pracownika o id {wybor_edycji_id}")

                print(f'Edycja: {pracownik_do_edycji.imie} {pracownik_do_edycji.nazwisko} (Id: {pracownik_do_edycji.id})')
                print("1. Edytuj imie")
                print("2. Edytuj nazwisko")
                print("3. Edytuj pesel")
                print("4. Edytuj numer telefonu")
                print("5. Edytuj stanowisko") # i samo sie zmeini haslo

                opcja_edycji = input("Podaj pole do edycji: ")
                try:
                    if opcja_edycji == "1":
                        nowe_imie = input("Podaj nowe imie: ").strip()
                        pracownik_do_edycji.ustaw_imie(nowe_imie)
                        moje_schronisko.zapisz_dane()
                        
                    elif opcja_edycji == "2":
                        nowe_nazwisko = input('Podaj nowe nazwisko: ').strip()
                        pracownik_do_edycji.ustaw_nazwisko(nowe_nazwisko)
                        moje_schronisko.zapisz_dane()                 
                    
                    elif opcja_edycji == "3":
                        nowy_pesel = input('Podaj nowy pesel: ').strip()
                        pracownik_do_edycji.ustaw_pesel(nowy_pesel)
                        moje_schronisko.zapisz_dane()

                    elif opcja_edycji == "4":
                        nowy_numer = input('Podaj nowy numer telefonu: ').strip()
                        pracownik_do_edycji.ustaw_telefon(nowy_numer)

                    elif opcja_edycji == "5":
                        nowe_stanowisko = input('Podaj nowe stanowisko: ').strip()
                        pracownik_do_edycji.ustaw_stanowisko(nowe_stanowisko)

                        liczby = "".join(str(x) for x in random.choices(range(1, 10), k=3))
                        nazwa = nowe_stanowisko.lower().strip()[:3]
                        haslo_nowe = f"{nazwa}{liczby}"
                        pracownik_do_edycji.ustaw_haslo(haslo_nowe)

                    moje_schronisko.zapisz_dane()
                    print('Edycja udana')
                except ValueError as error:
                    print(f"\n[BŁĄD WALIDACJI]: {error}")

            if wybor_admina == '3' :
                print('Usuwanie pracownika')
                wybor_usuniecia_id = input('Podaj id pracownika do usuniecia: ').strip()
                pracownik_do_usuniecia = moje_schronisko.znajdz_pracownika_po_id(wybor_usuniecia_id)

                if not pracownik_do_usuniecia:
                    print(f"Nie ma takiego pracownika o id {wybor_edycji_id}")
                
                potwierdzenie = input(f'Czy napweno chcesz ususnac pracownika: {pracownik_do_usuniecia.imie} {pracownik_do_usuniecia.nazwisko} (tak/nie)?')

                if potwierdzenie.lower() == 'tak':
                    moje_schronisko.usun_pracownika(pracownik_do_usuniecia)
                    moje_schronisko.zapisz_dane()
                    print('Pracownik usuniety')
                else:
                    print("Zla operacja")
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")

if __name__ == "__main__":
    uruchom_menu()

