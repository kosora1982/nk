from app import app, db
from models.models import HoroscopeType, Horoscope
from datetime import date, timedelta

def check_horoscope_types():
    """Proverava tipove horoskopa u bazi"""
    with app.app_context():
        print("🔍 Proveravam tipove horoskopa...")
        
        types = HoroscopeType.query.all()
        print(f"\n📋 Tipovi horoskopa ({len(types)}):")
        for t in types:
            print(f"  - ID: {t.id}, Name: {t.name}, Description: {t.description}")
        
        # Proveri sve horoskope za danas
        today = date.today()
        print(f"\n📅 Horoskopi za danas ({today}):")
        horoscopes = Horoscope.query.filter_by(date=today).all()
        for h in horoscopes:
            print(f"  - {h.sign} ({h.type.name}): {h.content[:100]}...")

if __name__ == '__main__':
    check_horoscope_types() 