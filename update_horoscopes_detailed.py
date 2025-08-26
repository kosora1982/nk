from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import date, timedelta
from local_horoscopes import get_local_horoscope, SIGNS

def update_horoscopes_with_detailed_content():
    """Ažurira postojeće horoskope sa detaljnim sadržajem"""
    with app.app_context():
        print("🔮 Počinjem ažuriranje horoskopa sa detaljnim sadržajem...")
        
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
            for sign in SIGNS:
                # Pronađi postojeći horoskop
                existing = Horoscope.query.filter_by(
                    type_id=horoscope_type.id, 
                    sign=sign, 
                    date=target_date
                ).first()
                
                if existing:
                    # Generiši novi detaljni horoskop
                    new_content = get_local_horoscope(sign, horoscope_type.name)
                    
                    # Ažuriraj sadržaj
                    existing.content = new_content
                    updated_count += 1
                    print(f"  🔄 Ažuriran {sign} ({horoscope_type.name})")
                else:
                    print(f"  ❌ Nije pronađen horoskop za {sign} ({horoscope_type.name})")
            
            # Sačuvaj promene
            db.session.commit()
            print(f"  💾 Ažurirano {updated_count} {horoscope_type.name} horoskopa")
        
        print("\n✅ Ažuriranje horoskopa završeno!")

if __name__ == '__main__':
    update_horoscopes_with_detailed_content() 