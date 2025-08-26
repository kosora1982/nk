from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import date, timedelta

def check_detailed_horoscope():
    """Proverava detaljni horoskop za specifičan znak"""
    with app.app_context():
        print("🔍 Proveravam detaljni horoskop...")
        
        # Proveri dnevni horoskop za Ovan
        today = date.today()
        horoscope = Horoscope.query.filter_by(
            type_id=5,  # dnevni
            sign='Ovan',
            date=today
        ).first()
        
        if horoscope:
            print(f"\n📅 DNEVNI HOROSKOP ZA OVAN ({today}):")
            print("=" * 50)
            print(horoscope.content)
            print("=" * 50)
        else:
            print("❌ Nije pronađen horoskop za Ovan")
        
        # Proveri nedeljni horoskop za Bik
        monday = today - timedelta(days=today.weekday())
        weekly_horoscope = Horoscope.query.filter_by(
            type_id=6,  # nedeljni
            sign='Bik',
            date=monday
        ).first()
        
        if weekly_horoscope:
            print(f"\n📅 NEDELJNI HOROSKOP ZA BIK ({monday}):")
            print("=" * 50)
            print(weekly_horoscope.content)
            print("=" * 50)
        else:
            print("❌ Nije pronađen nedeljni horoskop za Bik")

if __name__ == '__main__':
    check_detailed_horoscope() 