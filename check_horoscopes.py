from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import date, timedelta

def check_horoscopes():
    with app.app_context():
        print("🔍 Proveravam horoskope u bazi podataka...")
        
        # Proveri tipove horoskopa
        types = HoroscopeType.query.all()
        print(f"\n📋 Tipovi horoskopa ({len(types)}):")
        for t in types:
            print(f"  - {t.name}: {t.description}")
        
        # Proveri horoskope po tipovima
        today = date.today()
        
        for horoscope_type in types:
            print(f"\n📅 {horoscope_type.name.upper()} horoskopi:")
            
            # Odredi datum na osnovu tipa
            if horoscope_type.name == 'dnevni':
                target_date = today
            elif horoscope_type.name == 'nedeljni':
                target_date = today - timedelta(days=today.weekday())
            elif horoscope_type.name == 'mesecni':
                target_date = today.replace(day=1)
            elif horoscope_type.name == 'godisnji':
                target_date = today.replace(month=1, day=1)
            else:
                continue
            
            horoscopes = Horoscope.query.filter_by(
                type_id=horoscope_type.id,
                date=target_date
            ).all()
            
            print(f"  Datum: {target_date}")
            print(f"  Broj horoskopa: {len(horoscopes)}")
            
            if horoscopes:
                print("  Znakovi:")
                for h in horoscopes:
                    content_preview = h.content[:50] + "..." if len(h.content) > 50 else h.content
                    print(f"    - {h.sign}: {content_preview}")
            else:
                print("  ⚠️  Nema horoskopa za ovaj datum!")
        
        # Ukupan broj horoskopa
        total_horoscopes = Horoscope.query.count()
        print(f"\n📊 Ukupno horoskopa u bazi: {total_horoscopes}")

if __name__ == '__main__':
    check_horoscopes() 