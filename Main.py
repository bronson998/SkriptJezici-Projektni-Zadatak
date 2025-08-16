from Bibliotekar import Bibliotekar
from Clan import Clan
from Knjiga import Knjiga
from Pozajmica import Pozajmica

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
        print("6. Izlaz")
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

if __name__ == "__main__":
    while True:
        login()
        nastavak = input("Da li zelite novo logovanje? (da/ne): ").lower()
        if nastavak != "da":
            break
    print("Kraj programa.")
