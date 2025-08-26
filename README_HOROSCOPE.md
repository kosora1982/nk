# 🔮 Horoskop Sistem - Uputstva

## 📋 Pregled

Ovaj sistem omogućava automatsko punjenje horoskopa sa **lokalnim podacima** za sve tipove horoskopa:
- **Dnevni horoskop** - ažurira se svaki dan
- **Nedeljni horoskop** - ažurira se svakog ponedeljka
- **Mesečni horoskop** - ažurira se prvog dana meseca
- **Godišnji horoskop** - ažurira se prvog dana godine

## 🚀 Kako koristiti

### 1. Kreiranje baze podataka
```bash
python create_db.py
```

### 2. Inicijalno punjenje horoskopa
```bash
python local_horoscopes.py
```

### 3. Ažuriranje horoskopa
```bash
python update_horoscopes.py
```

### 4. Provera horoskopa u bazi
```bash
python check_horoscopes.py
```

## 📊 Tipovi horoskopa

### Dnevni horoskop
- **Datum**: Današnji datum
- **Ažuriranje**: Svaki dan
- **Sadržaj**: Lokalno generisan sa 3 varijante po znaku

### Nedeljni horoskop
- **Datum**: Ponedeljak te nedelje
- **Ažuriranje**: Svakog ponedeljka
- **Sadržaj**: Lokalno generisan sa jedinstvenim sadržajem

### Mesečni horoskop
- **Datum**: Prvi dan meseca
- **Ažuriranje**: Prvog dana meseca
- **Sadržaj**: Lokalno generisan sa jedinstvenim sadržajem

### Godišnji horoskop
- **Datum**: Prvi dan godine
- **Ažuriranje**: Prvog dana godine
- **Sadržaj**: Lokalno generisan sa jedinstvenim sadržajem

## 🔧 Znakovi horoskopa

Sistem podržava sve 12 znakova:
- Ovan
- Bik
- Blizanci
- Rak
- Lav
- Devica
- Vaga
- Škorpija
- Strelac
- Jarac
- Vodolija
- Ribe

## 📈 Automatsko ažuriranje

### Cron job za Linux/Mac
```bash
# Dodaj u crontab -e
0 6 * * * cd /path/to/project && python update_horoscopes.py
```

### Windows Task Scheduler
1. Otvori Task Scheduler
2. Kreiraj Basic Task
3. Postavi da se pokreće svaki dan u 6:00
4. Akcija: Start a program
5. Program: `python`
6. Arguments: `update_horoscopes.py`
7. Start in: `C:\path\to\project`

## 🗄️ Baza podataka

### Tabele
- `horoscope_type` - Tipovi horoskopa
- `horoscope` - Sadržaj horoskopa

### Struktura horoscope tabele
```sql
CREATE TABLE horoscope (
    id INTEGER PRIMARY KEY,
    type_id INTEGER NOT NULL,
    sign VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Provera podataka

### Provera broja horoskopa
```python
from app import app, db
from models.models import Horoscope

with app.app_context():
    total = Horoscope.query.count()
    print(f"Ukupno horoskopa: {total}")
```

### Provera horoskopa za određeni datum
```python
from datetime import date
from models.models import Horoscope, HoroscopeType

with app.app_context():
    today = date.today()
    daily_type = HoroscopeType.query.filter_by(name='dnevni').first()
    horoscopes = Horoscope.query.filter_by(
        type_id=daily_type.id,
        date=today
    ).all()
    
    for h in horoscopes:
        print(f"{h.sign}: {h.content[:100]}...")
```

## ⚠️ Troubleshooting

### Problem: Baza podataka greška
- Obriši `cms.db` fajl
- Pokreni `python create_db.py`
- Pokreni `python local_horoscopes.py`

### Problem: Flask kontekst greška
- Uvek koristi `with app.app_context():` u skriptama
- Proveri da li je `app.py` u istom direktorijumu

### Problem: Nedostaju horoskopi
- Pokreni `python update_horoscopes.py` za ažuriranje
- Proveri sa `python check_horoscopes.py`

## 📝 Napomene

- **Lokalni podaci**: Sistem koristi lokalno generisane horoskope umesto API-ja
- **Realistični sadržaj**: Horoskopi su napisani na srpskom jeziku sa realističnim sadržajem
- **Varijabilnost**: Dnevni horoskopi imaju 3 različite varijante po znaku
- **Stari horoskopi**: Automatski se brišu horoskopi stariji od 30 dana
- **Sprečavanje duplikata**: Sistem sprečava duplikate za isti datum i znak
- **Ažuriranje**: Postojeći horoskopi se ažuriraju sa novim sadržajem

## 🎯 Prednosti lokalnog sistema

✅ **Nema zavisnosti od API-ja** - radi bez interneta  
✅ **Brzina** - trenutno generisanje  
✅ **Kontrola sadržaja** - možete prilagoditi horoskope  
✅ **Besplatno** - nema troškova za API pozive  
✅ **Pouzdanost** - nema grešaka sa spoljašnjim servisima  
✅ **Privatnost** - svi podaci su lokalni 