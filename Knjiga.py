class Knjiga:
    def __init__(self, broj, naslov, autor, godina, slobodnihPrimeraka):
        self.broj = broj
        self.naslov = naslov
        self.autor = autor
        self.godina = godina
        self.slobodnihPrimeraka = slobodnihPrimeraka

    @classmethod
    def _ucitajKnjige(cls):
        knjige = []
        filename = "knjige.txt"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    knjige.append(cls.str2knjiga(line))
        except FileNotFoundError:
            print("Fajl sa imenom", filename, "ne postoji!")
        return knjige

    @classmethod
    def _sacuvajKnjige(cls, knjigeLista=None):
        if knjigeLista is None:
            knjigeLista = cls._ucitajKnjige()
        filename = "knjige.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for k in knjigeLista:
                file.write(k.knjiga2str() + "\n")

    @classmethod
    def ispisiSveKnjige(cls):
        knjige = cls._ucitajKnjige()
        if not knjige:
            print("Nema unetih knjiga.")
            return

        print(f"{'Broj':<5}|{'Naslov':<25}|{'Autor':<20}|{'Godina Izdanja':<15}|{'Slobodnih Primeraka':<20}")
        print("-" * 90)

        for k in knjige:
            print(f"{k.broj:<5}|{k.naslov:<25}|{k.autor:<20}|{k.godina:<15}|{k.slobodnihPrimeraka:<20}")

    def mozeSePozajmiti(self):
        return self.slobodnihPrimeraka > 0

    def pozajmiPrimerak(self):
        if self.slobodnihPrimeraka <= 0:
            raise ValueError("Nema slobodnih primeraka!")
        self.slobodnihPrimeraka -= 1
        Knjiga._sacuvajKnjige()

    def vratiPrimerak(self):
        self.slobodnihPrimeraka += 1
        Knjiga._sacuvajKnjige()

    @classmethod
    def str2knjiga(cls, line):
        tmp = line.strip().split("|")
        return Knjiga(
            int(tmp[0]),
            tmp[1],
            tmp[2],
            int(tmp[3]),
            int(tmp[4])
        )

    def knjiga2str(self):
        return f"{self.broj}|{self.naslov}|{self.autor}|{self.godina}|{self.slobodnihPrimeraka}"

    def __str__(self):
        return f"Broj: {self.broj}, Naslov: {self.naslov}, Autor: {self.autor}, Godina izdanja: {self.godina}, Broj primeraka: {self.slobodnihPrimeraka}"

    @classmethod
    def nadjiKnjiguPoNaslovu(cls, naslov):
        knjige = cls._ucitajKnjige()
        for k in knjige:
            if k.naslov.lower() == naslov.lower():
                return k
        return None
