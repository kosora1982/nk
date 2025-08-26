from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import datetime, date, timedelta
import requests
import time

SIGNS = [
    'Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica',
    'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe'
]

def get_horoscope_from_api(sign, horoscope_type):
    """Dohvata horoskop sa API-ja"""
    try:
        # API endpoint za horoskop
        api_url = f"https://horoscope-api.herokuapp.com/horoscope/{horoscope_type}/{sign.lower()}"
        
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('horoscope', f"Nema dostupnog horoskopa za {sign} ({horoscope_type})")
        else:
            return f"Greška pri dohvatanju horoskopa za {sign} ({horoscope_type}): {response.status_code}"
    except Exception as e:
        return f"Greška pri dohvatanju horoskopa za {sign} ({horoscope_type}): {str(e)}"

def fill_horoscopes():
    with app.app_context():
        print("🔮 Počinjem punjenje horoskopa sa realnim podacima...")
        
        # Dohvati sve tipove horoskopa
        types = HoroscopeType.query.all()
        
        for horoscope_type in types:
            print(f"\n📅 Punim {horoscope_type.name} horoskope...")
            
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
            
            for sign in SIGNS:
                # Proveri da li već postoji
                existing = Horoscope.query.filter_by(
                    type_id=horoscope_type.id, 
                    sign=sign, 
                    date=target_date
                ).first()
                
                if existing:
                    print(f"  ✅ {sign} ({horoscope_type.name}) već postoji")
                    continue
                
                # Dohvati horoskop sa API-ja
                print(f"  🔄 Dohvatam {sign} ({horoscope_type.name})...")
                content = get_horoscope_from_api(sign, horoscope_type.name)
                
                # Kreiraj novi horoskop
                horoscope = Horoscope(
                    type_id=horoscope_type.id,
                    sign=sign,
                    date=target_date,
                    content=content
                )
                db.session.add(horoscope)
                
                # Pauza između zahteva da ne preopteretimo API
                time.sleep(0.5)
            
            # Sačuvaj sve horoskope za ovaj tip
            db.session.commit()
            print(f"  💾 Sačuvano {len(SIGNS)} {horoscope_type.name} horoskopa")
        
        print("\n✅ Punjenje horoskopa završeno!")

if __name__ == '__main__':
    fill_horoscopes() 