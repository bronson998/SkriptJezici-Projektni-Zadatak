from Pozajmica import Pozajmica
from Knjiga import Knjiga

class Bibliotekar:
    def __init__(self, broj, ime, prezime, korisnickoIme, sifra):
        self.broj = broj
        self.ime = ime
        self.prezime = prezime
        self.korisnickoIme = korisnickoIme
        self.sifra = sifra

    @classmethod
    def _ucitajBibliotekare(cls):
        bibliotekari = []
        filename = "bibliotekari.txt"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    bibliotekari.append(cls.str2bibliotekar(line))
        except FileNotFoundError:
            pass
        return bibliotekari

    @classmethod
    def _sacuvajBibliotekare(cls, bibliotekari):
        filename = "bibliotekari.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for b in bibliotekari:
                file.write(b.bibliotekar2str() + "\n")

    @classmethod
    def dodajBibliotekara(cls, ime, prezime, korisnickoIme, sifra):
        bibliotekari = cls._ucitajBibliotekare()
        if bibliotekari:
            maxBroj = max(b.broj for b in bibliotekari)
        else:
            maxBroj = 0
        noviBroj = maxBroj + 1
        for b in bibliotekari:
            if b.korisnickoIme == korisnickoIme:
                print("Bibliotekar sa tim korisnickim imenom vec postoji!")
                return None
        novi = cls(noviBroj, ime, prezime, korisnickoIme, sifra)
        bibliotekari.append(novi)
        cls._sacuvajBibliotekare(bibliotekari)
        return novi

    @classmethod
    def pronadjiBibliotekaraPoKorisnickomImenu(cls, korisnickoIme):
        bibliotekari = cls._ucitajBibliotekare()
        for b in bibliotekari:
            if b.korisnickoIme == korisnickoIme:
                return b
        return None

    @classmethod
    def izmeniBibliotekara(cls, korisnickoIme, ime=None, prezime=None, sifra=None):
        bibliotekari = cls._ucitajBibliotekare()
        for b in bibliotekari:
            if b.korisnickoIme == korisnickoIme:
                if ime: b.ime = ime
                if prezime: b.prezime = prezime
                if sifra: b.sifra = sifra
                cls._sacuvajBibliotekare(bibliotekari)
                return b
        return None

    @classmethod
    def obrisiBibliotekara(cls, korisnickoIme):
        bibliotekari = cls._ucitajBibliotekare()
        for b in bibliotekari:
            if b.korisnickoIme == korisnickoIme:
                bibliotekari.remove(b)
                cls._sacuvajBibliotekare(bibliotekari)
                return b
        return None

    @classmethod
    def ispisiSveBibliotekare(cls):
        bibliotekari = cls._ucitajBibliotekare()
        if not bibliotekari:
            print("Nema unetih bibliotekara.")
            return
        print(f"{'Broj':<5}|{'Ime':<15}|{'Prezime':<15}|{'Korisnicko Ime':<20}|{'Sifra':<15}")
        print("-" * 70)
        for b in bibliotekari:
            print(f"{b.broj:<5}|{b.ime:<15}|{b.prezime:<15}|{b.korisnickoIme:<20}|{b.sifra:<15}")

    @classmethod
    def str2bibliotekar(cls, line):
        tmp = line.strip().split("|")
        return Bibliotekar(int(tmp[0]), tmp[1], tmp[2], tmp[3], tmp[4])

    def bibliotekar2str(self):
        return f"{self.broj}|{self.ime}|{self.prezime}|{self.korisnickoIme}|{self.sifra}"

    def __str__(self):
        return f"Broj: {self.broj}, Ime: {self.ime}, Prezime: {self.prezime}, Korisnicko ime: {self.korisnickoIme}, Sifra: {self.sifra}"

    # --- operacije nad knjigama ---
    @staticmethod
    def dodajKnjigu(knjiga):
        knjige = Knjiga._ucitajKnjige()
        knjige.append(knjiga)
        Knjiga._sacuvajKnjige(knjige)

    @staticmethod
    def pozajmiKnjiguClanu(korisnickoImeClana, naslovKnjige, brojDana=20):
        return Pozajmica.dodajPozajmicu(korisnickoImeClana, naslovKnjige, brojDana)

    @staticmethod
    def vratiKnjiguOdClana(brojPozajmice):
        return Pozajmica.vratiKnjigu(brojPozajmice)

    @staticmethod
    def posaljiOpomene():
        opomene = Pozajmica.proveriOpomene()
        if not opomene:
            print("Nema clanova sa kasnjenjem.")
        else:
            for p in opomene:
                print(f"Opomena poslata clanu {p.korisnickoImeClana} za knjigu {p.naslovKnjige} (pozajmica {p.brojPozajmice})")
