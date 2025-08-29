from Bibliotekar import Bibliotekar
from Clan import Clan
from Knjiga import Knjiga
from Pozajmica import Pozajmica
from collections import Counter
from datetime import datetime, date
import matplotlib.pyplot as plt

def login():
    print("Logovanje u sistem biblioteke")
    korisnickoIme = input("Korisnicko ime: ")
    sifra = input("Sifra: ")

    bibliotekar = Bibliotekar.pronadjiBibliotekaraPoKorisnickomImenu(korisnickoIme)
    if bibliotekar and bibliotekar.sifra == sifra:
        print(f"Ulogovan bibliotekar: {bibliotekar.ime} {bibliotekar.prezime}")
        meniBibliotekar(bibliotekar)
        return

    # Proveravamo da li je clan
    clan = Clan.pronadjiClanaPoKorisnickomImenu(korisnickoIme)
    if clan and clan.sifra == sifra:
        print(f"Ulogovan clan: {clan.ime} {clan.prezime}")
        meniClan(clan)
        return

    print("Neispravno korisnicko ime ili sifra.")

def meniBibliotekar(bibliotekar):
    while True:
        print("\n--- Meni bibliotekar ---")
        print("1. Prikazi sve knjige")
        print("2. Dodaj knjigu")
        print("3. Napravi pozajmicu za clana")
        print("4. Vrati knjigu od clana")
        print("5. Posalji opomene")
        print("6. Statistika")
        print("7. Izlaz")
        izbor = input("Izaberite opciju: ")

        if izbor == "1":
            Knjiga.ispisiSveKnjige()
        elif izbor == "2":
            naslov = input("Naslov knjige: ")
            autor = input("Autor: ")
            godina = int(input("Godina izdanja: "))
            primeraka = int(input("Broj primeraka: "))
            sve_knjige = Knjiga._ucitajKnjige()
            novi_broj = max([k.broj for k in sve_knjige], default=0) + 1
            nova_knjiga = Knjiga(novi_broj, naslov, autor, godina, primeraka)
            Bibliotekar.dodajKnjigu(nova_knjiga)
            print("Knjiga dodata.")
        elif izbor == "3":
            korisnickoImeClana = input("Korisnicko ime clana: ")
            naslovKnjige = input("Naslov knjige: ")
            try:
                Pozajmica.dodajPozajmicu(korisnickoImeClana, naslovKnjige)
                print("Pozajmica kreirana.")
            except ValueError as e:
                print(e)
        elif izbor == "4":
            korisnickoImeClana = input("Korisnicko ime clana: ")
            naslovKnjige = input("Naslov knjige: ")
            try:
                Pozajmica.vratiKnjigu(korisnickoImeClana, naslovKnjige)
                knjiga = next(
                (k for k in Knjiga._ucitajKnjige() if k.naslov.lower().strip() == naslovKnjige.lower().strip()),
                None
                )
                if knjiga is None:
                    print("Knjiga nije pronađena u biblioteci.")
                else:
                    print(f"Knjiga vracena. Trenutno slobodnih primeraka: {knjiga.slobodnihPrimeraka}")
            except ValueError as e:
                print(e)
        elif izbor == "5":
            Bibliotekar.posaljiOpomene()
        elif izbor == "6":
            prikazi_statistiku()
        elif izbor == "7":
            break
        else:
            print("Nepoznata opcija.")

def meniClan(clan):
    while True:
        print("\n--- Meni clan ---")
        print("1. Prikazi sve knjige")
        print("2. Pozajmi knjigu")
        print("3. Vrati knjigu")
        print("4. Izlaz")
        izbor = input("Izaberite opciju: ")

        if izbor == "1":
            Knjiga.ispisiSveKnjige()

        elif izbor == "2":
            naslovKnjige = input("Naslov knjige: ")
            try:
                pozajmica = Pozajmica.dodajPozajmicu(clan.korisnickoIme, naslovKnjige)
                knjiga = next(k for k in Knjiga._ucitajKnjige() 
                              if k.naslov.lower().strip() == naslovKnjige.lower().strip())
                print(f"Knjiga pozajmljena. Trenutno slobodnih primeraka: {knjiga.slobodnihPrimeraka}")
            except ValueError as e:
                print(e)

        elif izbor == "3":
            try:
                naslovKnjige = input("Naslov knjige: ")
                sve_pozajmice = Pozajmica._ucitajPozajmice()
                pozajmica = next(
                    (p for p in sve_pozajmice if p.korisnickoImeClana == clan.korisnickoIme
                     and p.naslovKnjige.lower() == naslovKnjige.lower()), 
                    None)
                if pozajmica is None:
                    print("Pozajmica ne postoji.")
                    continue
                naslovKnjige = pozajmica.naslovKnjige

                Pozajmica.vratiKnjigu(clan.korisnickoIme, naslovKnjige)
                knjiga = next(k for k in Knjiga._ucitajKnjige() 
                              if k.naslov.lower().strip() == naslovKnjige.lower().strip())
                print(f"Knjiga vracena. Trenutno slobodnih primeraka: {knjiga.slobodnihPrimeraka}")
            except ValueError as e:
                print(e)

        elif izbor == "4":
            break

        else:
            print("Nepoznata opcija.")

def prikazi_statistiku():
    def u_datum(s: str):
        return datetime.fromisoformat(s).date() if "T" in s else date.fromisoformat(s)

    naslovi, korisnicka_imena, datumi_vracanja = [], [], []

    try:
        with open("pozajmice.txt", "r", encoding="utf-8") as fajl:
            for linija in fajl:
                linija = linija.strip()
                if not linija:
                    continue
                delovi = linija.split("|")
                if len(delovi) < 6:
                    continue
                korisnicka_imena.append(delovi[1])
                naslovi.append(delovi[2])
                try:
                    datumi_vracanja.append(u_datum(delovi[4]))
                except Exception:
                    pass
    except FileNotFoundError:
        print("Nema fajla pozajmice.txt")
        return

    if not naslovi and not korisnicka_imena:
        print("Nema podataka u pozajmice.txt.")
        return

    def iscrtaj_grafikon(oznake, vrednosti, naslov, x_oznaka, y_oznaka):
        plt.figure()
        x = range(len(vrednosti))
        plt.bar(x, vrednosti)
        plt.title(naslov)
        plt.xlabel(x_oznaka)
        plt.ylabel(y_oznaka)
        plt.xticks(x, oznake, rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    gornja_granica = 20
    pozajmice_po_naslovu = Counter(naslovi).most_common(gornja_granica)
    if pozajmice_po_naslovu:
        oznake = [k for k, _ in pozajmice_po_naslovu]
        vrednosti = [v for _, v in pozajmice_po_naslovu]
        iscrtaj_grafikon(oznake, vrednosti, "Broj pozajmica po naslovu", "Naslov", "Pozajmica")

    pozajmice_po_clanu = Counter(korisnicka_imena).most_common(gornja_granica)
    if pozajmice_po_clanu:
        oznake = [k for k, _ in pozajmice_po_clanu]
        vrednosti = [v for _, v in pozajmice_po_clanu]
        iscrtaj_grafikon(oznake, vrednosti, "Broj pozajmica po clanu", "Korisnicko ime", "Pozajmica")

    if datumi_vracanja:
        danas = date.today()
        broj_prekoracenih = sum(1 for d in datumi_vracanja if d < danas)
        broj_aktivnih = len(datumi_vracanja) - broj_prekoracenih
        iscrtaj_grafikon(
            ["Aktivne", "Prekoracene"],
            [broj_aktivnih, broj_prekoracenih],
            "Status pozajmica",
            "Status",
            "Broj"
        )




if __name__ == "__main__":
    while True:
        login()
        nastavak = input("Da li zelite novo logovanje? (da/ne): ").lower()
        if nastavak != "da":
            break
    print("Kraj programa.")
