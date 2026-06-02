# Do zrobienia na pewno: (zrobisz to usuń)(wpadniesz na coś dopisz):
# 
#   - logowanie?
#   - zapis/odczyt z pliku dla innych danych niż zwierzęta
#
from abc import ABC, abstractmethod
import datetime
import json

class Schronisko():
    def __init__(self, zwierzeta=None, pracownicy=None, historia_adopcji=None):
        self.__zwierzeta = zwierzeta if zwierzeta is not None else []
        self.__pracownicy = pracownicy if pracownicy is not None else []
        self.__historia_adopcji = historia_adopcji if historia_adopcji is not None else []

    def dodaj_zwierze(self, zwierze):
        if not isinstance(zwierze, Zwierze):
            raise TypeError("Możesz dodać tylko obiekt klasy Zwierze!")
        self.__zwierzeta.append(zwierze)
        print(f"Dodano zwierze: {zwierze}")
    
    def dodaj_pracownika(self, pracownik):
        if not isinstance(pracownik, Pracownik):
            raise TypeError("Możesz dodać tylko obiekt klasy Pracownik!")
        self.__pracownicy.append(pracownik)
        print(f"Dodano pracownika: {pracownik}")

    def filtruj_zwierzeta_do_adopcji(self):
        return [z for z in self.__zwierzeta if z.status.lower() != "adoptowany"]

    def znajdz_zwierze_po_id(self, id_zwierzecia):
        for z in self.__zwierzeta:
            if str(z.id) == str(id_zwierzecia):
                return z
        return None
    
    def adopcja(self, zwierze, osoba, data=None):
        if data is None:
            data = datetime.datetime.now()
        if zwierze.status.lower() == "adoptowane":
            raise ValueError(f"Zwierzę o ID {zwierze.id} zostało już wcześniej adoptowane!")
        adopcja = Adopcja(data, zwierze, osoba)
        self.__historia_adopcji.append(adopcja)
        zwierze.adoptowane()
        print(adopcja)

    def zapisz_dane(self, plik_zwierzeta="zwierzeta.json"):
        try:
            dane = [z.to_dict() for z in self.__zwierzeta]
            with open(plik_zwierzeta, "w", encoding="utf-8") as f:
                json.dump(dane, f, indent=4, ensure_ascii=False)
            print("[System] Dane zostały zapisane.")
        except IOError as e:
            print(f"[Błąd zapisu pliku]: {e}")

    def wczytaj_dane(self, plik_zwierzeta="zwierzeta.json"):
        try:
            with open(plik_zwierzeta, "r", encoding="utf-8") as f:
                dane = json.load(f)
            self.__zwierzeta = [Zwierze.from_dict(d) for d in dane]
            print(f"[System] Wczytano {len(self.__zwierzeta)} zwierząt z pliku.")
        except FileNotFoundError:
            print("[System] Brak pliku z danymi. Inicjalizacja pustej bazy.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Błąd struktury danych pliku]: {e}")

    
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
        return self.get_info()
    
    def adoptowane(self):
        self.__status = "adoptowane"

    def zmien_status(self, pracownik, nowy_status):
        data = datetime.datetime.now()
        wpis = Wpis(data, self.__status, nowy_status, pracownik)
        self.__status = nowy_status
        self.__historia.append(wpis)
        print(wpis)

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    def to_dict(self):
        return {
            "id": self.__id, "gatunek": self.__gatunek, "rasa": self.__rasa,
            "imie": self.__imie, "wiek": self.__wiek, "opis": self.__opis,
            "stan_zdrowia": self.__stan_zdrowia, "status": self.__status
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["gatunek"], d["rasa"], d["imie"], d["wiek"], d["opis"], d["stan_zdrowia"], d["status"])

class Adopcja():
    def __init__(self, data, zwierze, nowy_wlasciciel):
        self.__data, self.__zwierze, self.__nowy_wlasciciel = data, zwierze, nowy_wlasciciel  

    def __str__(self):
        message = f"Zwierze o ID: {self.__zwierze.id} adoptowano w dniu: {self.__data:%Y-%m-%d}. Nowy właściciel - {self.__nowy_wlasciciel.imie} {self.__nowy_wlasciciel.nazwisko}"
        return message


class Wpis():
    def __init__(self, data, stary_status, nowy_status, pracownik):
        self.__data, self.__stary_status, self.__nowy_status, self.__pracownik = data, stary_status, nowy_status, pracownik

    def __str__(self):
        message = f"{self.__data:%Y-%m-%d %H:%M:%S} - zmiana statusu z `{self.__stary_status}` na `{self.__nowy_status}`, wykonana przez pracownika {self.__pracownik.id}"    
        return message
    
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
    
class OsobaAdoptujaca(Osoba):
    def __init__(self, imie, nazwisko, pesel, telefon, warunki_mieszkaniowe, inne_zwierzeta):
        super().__init__(imie, nazwisko, pesel, telefon)
        self.__warunki_mieszkaniowe = warunki_mieszkaniowe
        self.__inne_zwierzeta = inne_zwierzeta
    
    def typ_osoby(self):
        return "Osoba Adoptujaca"
    
 
class Pracownik(Osoba):
    def __init__(self, imie, nazwisko, pesel, telefon, id, stanowisko):
        super().__init__(imie, nazwisko, pesel, telefon)
        self.__id = id
        self.__stanowisko = stanowisko
    
    @property
    def id(self):
        return self.__id
    
    def typ_osoby(self):
        return "Pracownik"
    
def uruchom_menu():
    moje_schronisko = Schronisko()
    moje_schronisko.wczytaj_dane() # Automatyczne wczytanie przy starcie
    
    # Tworzymy domyślnego pracownika do obsługi zgłoszeń
    admin = Pracownik("Jan", "Kowalski", "90010112345", "555-666", "P01", "Starszy Opiekun")
    moje_schronisko.dodaj_pracownika(admin)

    while True:
        print("\n--- SYSTEM ZARZĄDZANIA SCHRONISKIEM ---")
        print("1. Wyświetl zwierzęta do adopcji")
        print("2. Przyjmij nowe zwierzę")
        print("3. Przeprowadź adopcję")
        print("4. Zapisz i Wyjdź")
        
        wybor = input("Wybierz opcję (1-4): ").strip()
        print("-" * 40)

        if wybor == "1":
            zwierzeta = moje_schronisko.filtruj_zwierzeta_do_adopcji()
            if not zwierzeta:
                print("Aktualnie nie ma żadnych zwierząt w schronisku.")
            for z in zwierzeta:
                print(z)

        elif wybor == "2":
            print("Wpisz dane nowego zwierzęcia:")
            # Blok try-except wyłapie błędy parsowania int lub błędy walidacji z klasy Zwierze
            try:
                id_z = input("Podaj ID: ").strip()
                gatunek = input("Gatunek (np. Pies): ").strip()
                rasa = input("Rasa: ").strip()
                imie = input("Imię: ").strip()
                wiek = input("Wiek: ").strip()
                opis = input("Opis zachowania: ").strip()
                stan = input("Stan zdrowia: ").strip()

                # Próba utworzenia obiektu (tu może wyskoczyć ValueError)
                nowe_z = Zwierze(id_z, gatunek, rasa, imie, wiek, opis, stan, "Do adopcji")
                moje_schronisko.dodaj_zwierze(nowe_z)
                nowe_z.zmien_status(admin, "Zarejestrowany w bazie")
                print(f"Sukces! Dodano zwierzę {imie}.")

            except ValueError as e:
                # Zamiast crashu, program wypisze ładny komunikat i wróci do menu
                print(f"\n[BŁĄD DANYCH]: Nie udało się dodać zwierzęcia. Powód: {e}")
            except Exception as e:
                print(f"\n[NIEOCZEKIWANY BŁĄD]: {e}")

        elif wybor == "3":
            try:
                id_z = input("Podaj ID zwierzęcia do adopcji: ").strip()
                zwierze = moje_schronisko.znajdz_zwierze_po_id(id_z)
                
                if not zwierze:
                    print(f"Nie znaleziono zwierzęcia o ID: {id_z}")
                    continue

                print(f"Wybrano: {zwierze.get_info()}")
                print("\nPodaj dane osoby adoptującej:")
                imie_o = input("Imię: ").strip()
                nazw_o = input("Nazwisko: ").strip()
                pesel_o = input("PESEL (11 cyfr): ").strip()
                tel_o = input("Telefon: ").strip()

                # Próba utworzenia klienta (tu może paść błąd złego PESELu)
                klient = OsobaAdoptujaca(imie_o, nazw_o, pesel_o, tel_o, "Mieszkanie", "Brak")
                
                # Próba adopcji (tu może paść błąd, jeśli zwierzę jest już adoptowane)
                wynik = moje_schronisko.adopcja(zwierze, klient)
                print(wynik)

            except ValueError as e:
                print(f"\n[BŁĄD ADOPCJI]: Operacja przerwana. Powód: {e}")

        elif wybor == "4":
            moje_schronisko.zapisz_dane()
            print("Zamykanie programu. Do widzenia!")
            break
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")

if __name__ == "__main__":
    uruchom_menu()