import json
import datetime
import os
from zwierzeta import Zwierze, Adopcja
from osoby import Pracownik, OsobaAdoptujaca


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
        if data is None:
            data = datetime.datetime.now()
        if zwierze.status.lower() == "adoptowane":
            raise ValueError(f"Zwierzę o ID {zwierze.id} zostało już wcześniej adoptowane!")
        adopcja = Adopcja(data, zwierze.id, osoba.pesel, zalogowany_pracownik.id)
        self.__historia_adopcji.append(adopcja)
        zwierze.zmien_status(zalogowany_pracownik.id, "Adoptowany")
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
  