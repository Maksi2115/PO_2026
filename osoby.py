from abc import ABC, abstractmethod


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