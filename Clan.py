from Pozajmica import Pozajmica
from Knjiga import Knjiga

class Clan:
    def __init__(self, broj, ime, prezime, korisnickoIme, sifra):
        self.broj = broj
        self.ime = ime
        self.prezime = prezime
        self.korisnickoIme = korisnickoIme
        self.sifra = sifra

    @classmethod
    def _ucitajClanove(cls):
        clanovi = []
        filename = "clanovi.txt"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    clanovi.append(cls.str2clan(line))
        except FileNotFoundError:
            pass
        return clanovi

    @classmethod
    def _sacuvajClanove(cls, clanovi):
        filename = "clanovi.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for c in clanovi:
                file.write(c.clan2str() + "\n")

    @classmethod
    def dodajClana(cls, ime, prezime, korisnickoIme, sifra):
        clanovi = cls._ucitajClanove()
        if clanovi:
            maxBroj = max(c.broj for c in clanovi)
        else:
            maxBroj = 0
        for c in clanovi:
            if c.korisnickoIme == korisnickoIme:
                print("Clan sa tim korisnickim imenom vec postoji!")
                return None
        novi = cls(maxBroj + 1, ime, prezime, korisnickoIme, sifra)
        clanovi.append(novi)
        cls._sacuvajClanove(clanovi)
        return novi

    @classmethod
    def pronadjiClanaPoKorisnickomImenu(cls, korisnickoIme):
        clanovi = cls._ucitajClanove()
        for c in clanovi:
            if c.korisnickoIme == korisnickoIme:
                return c
        return None

    @classmethod
    def izmeniClana(cls, korisnickoIme, ime=None, prezime=None, sifra=None):
        clanovi = cls._ucitajClanove()
        for c in clanovi:
            if c.korisnickoIme == korisnickoIme:
                if ime: c.ime = ime
                if prezime: c.prezime = prezime
                if sifra: c.sifra = sifra
                cls._sacuvajClanove(clanovi)
                return c
        return None

    @classmethod
    def obrisiClana(cls, korisnickoIme):
        clanovi = cls._ucitajClanove()
        for c in clanovi:
            if c.korisnickoIme == korisnickoIme:
                clanovi.remove(c)
                cls._sacuvajClanove(clanovi)
                return c
        return None

    @classmethod
    def ispisiSveClanove(cls):
        clanovi = cls._ucitajClanove()
        if not clanovi:
            print("Nema unetih clanova.")
            return
        print(f"{'Broj':<5}|{'Ime':<15}|{'Prezime':<15}|{'Korisnicko Ime':<20}|{'Sifra':<15}")
        print("-" * 70)
        for c in clanovi:
            print(f"{c.broj:<5}|{c.ime:<15}|{c.prezime:<15}|{c.korisnickoIme:<20}|{c.sifra:<15}")

    @classmethod
    def str2clan(cls, line):
        tmp = line.strip().split("|")
        return Clan(int(tmp[0]), tmp[1], tmp[2], tmp[3], tmp[4])

    def clan2str(self):
        return f"{self.broj}|{self.ime}|{self.prezime}|{self.korisnickoIme}|{self.sifra}"

    def __str__(self):
        return f"Broj: {self.broj}, Ime: {self.ime}, Prezime: {self.prezime}, Korisnicko ime: {self.korisnickoIme}, Sifra: {self.sifra}"

    # --- operacije sa knjigama ---
    @staticmethod
    def vidiSveKnjige():
        Knjiga.ispisiSveKnjige()

    def pozajmiKnjigu(self, naslovKnjige, brojDana=20):
        return Pozajmica.dodajPozajmicu(self.korisnickoIme, naslovKnjige, brojDana)

    def vratiKnjigu(self, brojPozajmice):
        return Pozajmica.vratiKnjigu(brojPozajmice)
