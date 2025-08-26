from datetime import datetime, date, timedelta
from models.models import db, Horoscope, HoroscopeType

SIGNS = [
    'Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica',
    'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe'
]

# Tekstovi iz dnevni_horoskop_widget (bez HTML-a)
OPISI = [
    "Danas je dan za nove početke. Pratite svoje instinkte i ne bojte se promena. Ljubav: Otvorite srce za nova poznanstva, ali budite iskreni prema sebi. Posao: Prilike za napredak su pred vama, ali zahtevaju hrabrost i odlučnost. Zdravlje: Obratite pažnju na energiju, izbegavajte stres. Savet: Verujte u svoje sposobnosti i ne odustajte pred izazovima.",
    "Fokusirajte se na stabilnost i praktične zadatke. Ljubav: Partner može tražiti više pažnje, budite strpljivi. Posao: Finansijska situacija se poboljšava kroz upornost. Zdravlje: Prijatelji mogu doneti korisne savete za opuštanje. Savet: Veče je idealno za relaksaciju i planiranje narednih koraka.",
    "Komunikacija je ključ uspeha danas. Ljubav: Očekujte zanimljive vesti ili susrete, budite otvoreni za flert. Posao: Novi kontakti mogu doneti poslovne prilike. Zdravlje: Obratite pažnju na disanje i opuštanje. Savet: Budite radoznali i ne bojte se postavljati pitanja.",
    "Porodica i dom su u centru pažnje. Ljubav: Posvetite vreme najbližima, unesite harmoniju u odnose. Posao: Domaći zadaci i obaveze zahtevaju vašu pažnju. Zdravlje: Pronađite mir kroz meditaciju ili šetnju. Savet: Ne zaboravite na male radosti svakodnevnog života.",
    "Vaša energija je na vrhuncu! Ljubav: Strastveni susreti i nova poznanstva su mogući. Posao: Kreativni projekti donose uspeh, iskoristite inspiraciju. Zdravlje: Fizička aktivnost vam prija, ali ne preterujte. Savet: Slušajte svoje srce i budite otvoreni za promene.",
    "Detalji su važni. Ljubav: Razgovarajte iskreno sa partnerom o osećanjima. Posao: Organizacija i preciznost vode do velikih rezultata. Zdravlje: Obratite pažnju na ishranu i rutinu. Savet: Mali koraci danas donose velike promene sutra.",
    "Danas je dan za balans i diplomatiju. Ljubav: Rešavajte nesuglasice mirno, uživajte u umetnosti sa partnerom. Posao: Saradnja sa kolegama donosi napredak. Zdravlje: Pronađite vreme za relaksaciju i lepotu. Savet: Održavajte ravnotežu između posla i privatnog života.",
    "Intuicija je pojačana. Ljubav: Slušajte unutrašnji glas, veče donosi strastvene trenutke. Posao: Ne ulazite u nepotrebne rasprave, fokusirajte se na ciljeve. Zdravlje: Opuštanje i introspekcija su ključni. Savet: Verujte svojim osećajima i izbegavajte konflikte.",
    "Putovanja i učenje su naglašeni. Ljubav: Daljina može ojačati vezu, budite iskreni u komunikaciji. Posao: Prihvatite izazove sa optimizmom, širite znanje. Zdravlje: Aktivnosti na otvorenom vam prijaju. Savet: Proširite vidike i ne bojte se novih iskustava.",
    "Odgovornosti su u prvom planu. Ljubav: Partner očekuje podršku i razumevanje. Posao: Budite istrajni, ne odustajte od ciljeva. Zdravlje: Finansije zahtevaju pažnju, izbegavajte nepotrebne troškove. Savet: Planirajte dugoročno i budite dosledni.",
    "Društveni život je aktivan. Ljubav: Povežite se sa prijateljima, moguća su nova poznanstva. Posao: Budite otvoreni za nove ideje i timski rad. Zdravlje: Opuštanje u društvu pozitivno utiče na raspoloženje. Savet: Ne zaboravite na svoje hobije i interesovanja.",
    "Duhovnost i mašta su naglašeni. Ljubav: Posvetite vreme sebi i svojim snovima. Posao: Kreativni projekti donose zadovoljstvo. Zdravlje: Meditacija i umetnost pomažu u opuštanju. Savet: Snovi mogu biti inspirativni, zapišite ih i sledite intuiciju."
]

TYPES = {
    'dnevni': 'Dnevni horoskop',
    'nedeljni': 'Nedeljni horoskop',
    'mesecni': 'Mesečni horoskop',
    'godisnji': 'Godišnji horoskop'
}

def get_or_create_type(name, description):
    t = HoroscopeType.query.filter_by(name=name).first()
    if not t:
        t = HoroscopeType(name=name, description=description)
        db.session.add(t)
        db.session.commit()
        print(f"[DEBUG] Upisan tip horoskopa: {name}")
    else:
        print(f"[DEBUG] Tip horoskopa već postoji: {name}")
    return t

def seed_daily():
    today = date.today()
    t = get_or_create_type('dnevni', TYPES['dnevni'])
    for i, sign in enumerate(SIGNS):
        exists = Horoscope.query.filter_by(type_id=t.id, sign=sign, date=today).first()
        if not exists:
            opis = OPISI[i] if i < len(OPISI) else "Nema opisa."
            h = Horoscope(type_id=t.id, sign=sign, date=today, content=opis)
            db.session.add(h)
            print(f"[DEBUG] Upisan dnevni horoskop: {sign} {today}")
        else:
            print(f"[DEBUG] Dnevni horoskop već postoji: {sign} {today}")
    db.session.commit()

def seed_weekly():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    t = get_or_create_type('nedeljni', TYPES['nedeljni'])
    for i, sign in enumerate(SIGNS):
        exists = Horoscope.query.filter_by(type_id=t.id, sign=sign, date=monday).first()
        if not exists:
            opis = OPISI[i] if i < len(OPISI) else "Nema opisa."
            h = Horoscope(type_id=t.id, sign=sign, date=monday, content=opis)
            db.session.add(h)
    db.session.commit()

def seed_monthly():
    today = date.today()
    first = today.replace(day=1)
    t = get_or_create_type('mesecni', TYPES['mesecni'])
    for i, sign in enumerate(SIGNS):
        exists = Horoscope.query.filter_by(type_id=t.id, sign=sign, date=first).first()
        if not exists:
            opis = OPISI[i] if i < len(OPISI) else "Nema opisa."
            h = Horoscope(type_id=t.id, sign=sign, date=first, content=opis)
            db.session.add(h)
    db.session.commit()

def seed_yearly():
    today = date.today()
    first = today.replace(month=1, day=1)
    t = get_or_create_type('godisnji', TYPES['godisnji'])
    for i, sign in enumerate(SIGNS):
        exists = Horoscope.query.filter_by(type_id=t.id, sign=sign, date=first).first()
        if not exists:
            opis = OPISI[i] if i < len(OPISI) else "Nema opisa."
            h = Horoscope(type_id=t.id, sign=sign, date=first, content=opis)
            db.session.add(h)
    db.session.commit()

def seed_horoscopes():
    from app import app
    with app.app_context():
        seed_daily()
        seed_weekly()
        seed_monthly()
        seed_yearly()

if __name__ == "__main__":
    seed_horoscopes()
