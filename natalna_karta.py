# Skripta za kreiranje natalne karte u 5 koraka
# Koristi osnovne Python biblioteke i pseudokod za astronomske proračune

# 1. Prikupljanje podataka o osobi
def prikupljanje_podataka():
    print("Unesite podatke za natalnu kartu:")
    ime = input("Ime: ")
    datum = input("Datum rođenja (YYYY-MM-DD): ")
    vreme = input("Vreme rođenja (HH:MM): ")
    mesto = input("Mesto rođenja: ")
    return ime, datum, vreme, mesto

# 2. Pretvaranje datuma i vremena u julijanski datum (pseudokod)
def izracunaj_julijanski_datum(datum, vreme):
    # Ovde bi išao pravi proračun
    print(f"Pretvaram {datum} {vreme} u julijanski datum...")
    julijanski_datum = 2451545.0  # Primer vrednosti
    return julijanski_datum

# 3. Izračunavanje položaja planeta (pseudokod)
def izracunaj_polozaje_planeta(julijanski_datum):
    print(f"Računam položaje planeta za JD {julijanski_datum} iz lld.txt...")
    planete = {}
    try:
        with open("lld.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                parts = line.split(";")
                if len(parts) != 3:
                    continue
                planeta, jd_str, pozicija = parts
                try:
                    jd_file = float(jd_str)
                except ValueError:
                    continue
                if abs(jd_file - julijanski_datum) < 0.01:  # tolerancija na zaokruživanje
                    planete[planeta] = pozicija
    except FileNotFoundError:
        print("Greška: lld.txt nije pronađen!")
    if not planete:
        print("Nema podataka za zadati julijanski datum u lld.txt!")
    return planete

# 4. Izračunavanje astroloških kuća (pseudokod)
def izracunaj_kuce(julijanski_datum, mesto):
    print(f"Računam astrološke kuće za JD {julijanski_datum} i mesto {mesto}...")
    kuce = {
        'Prva kuća': '5° Ovan',
        'Druga kuća': '12° Bik',
        # Dodati ostale kuće
    }
    return kuce

# 5. Generisanje i prikaz natalne karte
def prikazi_natalnu_kartu(ime, planete, kuce):
    print(f"\nNatalna karta za {ime}:")
    print("Planete:")
    for planeta, pozicija in planete.items():
        print(f"  {planeta}: {pozicija}")
    print("Kuće:")
    for kuca, pozicija in kuce.items():
        print(f"  {kuca}: {pozicija}")

if __name__ == "__main__":
    ime, datum, vreme, mesto = prikupljanje_podataka()
    jd = izracunaj_julijanski_datum(datum, vreme)
    planete = izracunaj_polozaje_planeta(jd)
    kuce = izracunaj_kuce(jd, mesto)
    prikazi_natalnu_kartu(ime, planete, kuce)
