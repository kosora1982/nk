from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import datetime, date, timedelta
import random
from local_horoscopes import get_local_horoscope

SIGNS = [
    'Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica',
    'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe'
]

def update_horoscopes():
    with app.app_context():
        print("🔄 Počinjem ažuriranje horoskopa sa lokalnim podacima...")
        
        # Dohvati sve tipove horoskopa
        types = HoroscopeType.query.all()
        
        for horoscope_type in types:
            print(f"\n📅 Ažuriram {horoscope_type.name} horoskope...")
            
            # Odredi datum na osnovu tipa
            today = date.today()
            if horoscope_type.name == 'dnevni':
                target_date = today
            elif horoscope_type.name == 'nedeljni':
                target_date = today - timedelta(days=today.weekday())  # Ponedeljak
            elif horoscope_type.name == 'mesecni':
                target_date = today.replace(day=1)  # Prvi dan meseca
            elif horoscope_type.name == 'godisnji':
                target_date = today.replace(month=1, day=1)  # Prvi dan godine
            else:
                continue
            
            updated_count = 0
            created_count = 0
            
            for sign in SIGNS:
                # Proveri da li već postoji
                existing = Horoscope.query.filter_by(
                    type_id=horoscope_type.id, 
                    sign=sign, 
                    date=target_date
                ).first()
                
                # Generiši novi lokalni horoskop
                print(f"  🔄 Generišem {sign} ({horoscope_type.name})...")
                content = get_local_horoscope(sign, horoscope_type.name)
                
                if existing:
                    # Ažuriraj postojeći
                    existing.content = content
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                    print(f"    ✅ Ažuriran postojeći horoskop")
                else:
                    # Kreiraj novi
                    horoscope = Horoscope(
                        type_id=horoscope_type.id,
                        sign=sign,
                        date=target_date,
                        content=content
                    )
                    db.session.add(horoscope)
                    created_count += 1
                    print(f"    ➕ Kreiran novi horoskop")
            
            # Sačuvaj promene
            db.session.commit()
            print(f"  💾 Ažurirano: {updated_count}, Kreirano: {created_count}")
        
        print("\n✅ Ažuriranje horoskopa završeno!")

def clean_old_horoscopes():
    """Briše stare horoskope (starije od 30 dana)"""
    with app.app_context():
        print("🧹 Čistim stare horoskope...")
        
        cutoff_date = date.today() - timedelta(days=30)
        old_horoscopes = Horoscope.query.filter(Horoscope.date < cutoff_date).all()
        
        if old_horoscopes:
            for horoscope in old_horoscopes:
                db.session.delete(horoscope)
            
            db.session.commit()
            print(f"🗑️  Obrisano {len(old_horoscopes)} starih horoskopa")
        else:
            print("✅ Nema starih horoskopa za brisanje")

if __name__ == '__main__':
    # Prvo očisti stare horoskope
    clean_old_horoscopes()
    
    # Zatim ažuriraj postojeće i dodaj nove
    update_horoscopes() 