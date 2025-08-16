from datetime import datetime, timedelta
from Knjiga import Knjiga

class Pozajmica:
    def __init__(self, brojPozajmice, korisnickoImeClana, naslovKnjige, datumPozajmice, datumVracanja, opomena=False):
        self.brojPozajmice = brojPozajmice
        self.korisnickoImeClana = korisnickoImeClana
        self.naslovKnjige = naslovKnjige
        self.datumPozajmice = datumPozajmice
        self.datumVracanja = datumVracanja
        self.opomena = opomena

    def pozajmica2str(self):
        # Svi datumi se snimaju u ISO formatu
        return f"{self.brojPozajmice}|{self.korisnickoImeClana}|{self.naslovKnjige}|{self.datumPozajmice.isoformat()}|{self.datumVracanja.isoformat()}|{self.opomena}"

    @classmethod
    def str2pozajmica(cls, line):
        delovi = line.strip().split("|")
        return cls(
            int(delovi[0]),
            delovi[1],
            delovi[2],
            datetime.fromisoformat(delovi[3]),
            datetime.fromisoformat(delovi[4]),
            delovi[5].lower() == "true"
        )

    @classmethod
    def _ucitajPozajmice(cls):
        pozajmice = []
        filename = "pozajmice.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    pozajmice.append(cls.str2pozajmica(line))
        except FileNotFoundError:
            pass
        return pozajmice

    @classmethod
    def _sacuvajPozajmice(cls, pozajmice):
        filename = "pozajmice.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for p in pozajmice:
                f.write(p.pozajmica2str() + "\n")

    @classmethod
    def dodajPozajmicu(cls, korisnickoIme, naslovKnjige):
        knjige = Knjiga._ucitajKnjige()
        for knjiga in knjige:
            if knjiga.naslov.lower().strip() == naslovKnjige.lower().strip():
                if knjiga.slobodnihPrimeraka > 0:
                    knjiga.slobodnihPrimeraka -= 1
                    Knjiga._sacuvajKnjige(knjige)

                    pozajmice = cls._ucitajPozajmice()
                    broj = len(pozajmice) + 1
                    datumUzimanja = datetime.now()
                    datumVracanja = datetime.now() + timedelta(days=14)
                    nova = cls(broj, korisnickoIme, naslovKnjige, datumUzimanja, datumVracanja)
                    pozajmice.append(nova)
                    cls._sacuvajPozajmice(pozajmice)
                    return
                else:
                    raise ValueError("Nema slobodnih primeraka.")
        raise ValueError("Knjiga nije pronađena.")

    @classmethod
    def vratiKnjigu(cls, korisnickoIme, naslovKnjige):
        pozajmice = cls._ucitajPozajmice()
        pozajmica_za_brisanje = None

        for p in pozajmice:
            if p.korisnickoImeClana == korisnickoIme and p.naslovKnjige.lower().strip() == naslovKnjige.lower().strip():
                pozajmica_za_brisanje = p
                break

        if not pozajmica_za_brisanje:
            raise ValueError("Ova knjiga nije pozajmljena od strane ovog clana.")

        # Uvećavamo broj slobodnih primeraka
        knjige = Knjiga._ucitajKnjige()
        for knjiga in knjige:
            if knjiga.naslov.lower().strip() == naslovKnjige.lower().strip():
                knjiga.slobodnihPrimeraka += 1
                break
        Knjiga._sacuvajKnjige(knjige)

        pozajmice.remove(pozajmica_za_brisanje)
        cls._sacuvajPozajmice(pozajmice)

    @classmethod
    def proveriOpomene(cls):
        danas = datetime.now()
        return [p for p in cls._ucitajPozajmice() if p.datumVracanja < danas]
