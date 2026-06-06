import datetime

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
    def status(self):
        return self.__status

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