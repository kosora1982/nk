from app import app, db
from models.models import Horoscope, HoroscopeType
from datetime import datetime, date, timedelta
import random

SIGNS = [
    'Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica',
    'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe'
]

# Detaljni horoskopi sa odvojenim sekcijama
DETAILED_HOROSCOPES = {
    'Ovan': {
        'dnevni': [
            {
                'general': 'Danas je dan za nove početke. Vaša energija je na vrhuncu i trebalo bi da je iskoristite za postavljanje novih ciljeva.',
                'ljubav': 'Otvorite srce za nova poznanstva. Spontanost će privući pažnju potencijalnih partnera. Ako ste u vezi, partner će ceniti vašu iskrenost i direktnost.',
                'zdravlje': 'Fokusirajte se na kardio vežbe. Vaša energija je idealna za trčanje ili brzo hodanje. Poboljšajte cirkulaciju kroz fizičke aktivnosti.',
                'posao': 'Prilike za napredak su pred vama. Budite direktni u komunikaciji sa kolegama. Novi projekti donose uspeh ako pokažete inicijativu.'
            },
            {
                'general': 'Vaša hrabrost i odlučnost će vam pomoći da prevaziđete sve prepreke. Danas je idealan dan za vođstvo.',
                'ljubav': 'Partner će ceniti vašu iskrenost i hrabrost. Ne bojte se da izrazite svoja osećanja direktno. Romantika može biti strastvena.',
                'zdravlje': 'Vaša glava i ramena su pod stresom. Probajte joga vežbe za opuštanje. Poboljšajte kvalitet sna kroz večernju rutinu.',
                'posao': 'Budite direktni u komunikaciji. Vaša odlučnost će biti cenjena. Možete očekivati pozitivne povratne informacije.'
            },
            {
                'general': 'Danas je idealan dan za fizičke aktivnosti. Vaša kreativnost je pojačana i trebalo bi da je iskoristite.',
                'ljubav': 'Spontanost će privući pažnju. Ne bojte se da budete svoj. Partner će ceniti vašu energiju i entuzijazam.',
                'zdravlje': 'Fokusirajte se na vežbe koje uključuju ruke i ramena. Vaša energija je idealna za sportove kao što su tenis ili boks.',
                'posao': 'Novi projekti donose uspeh. Vaša kreativnost će biti cenjena. Možete očekivati neočekivane prilike.'
            }
        ],
        'nedeljni': {
            'general': 'Ova nedelja donosi nove prilike i izazove. Vaša energija će biti na vrhuncu, posebno sredinom nedelje.',
            'ljubav': 'Očekujte neočekivane susrete. Spontanost će biti ključna za romantične uspehe. Ako ste u vezi, partner će ceniti vašu hrabrost.',
            'zdravlje': 'Fokusirajte se na kardio vežbe tokom cele nedelje. Vaša energija je idealna za trčanje, plivanje ili biciklizam.',
            'posao': 'Novi projekti će vam dati priliku da pokažete svoje sposobnosti. Budite spremni za neočekivane izazove.'
        },
        'mesecni': {
            'general': 'Ovaj mesec donosi nove početke i prilike za vođstvo. Vaša energija će biti na vrhuncu.',
            'ljubav': 'Očekujte strastvene susrete. Mesec je idealan za nove veze ili obnavljanje postojećih. Partner će ceniti vašu inicijativu.',
            'zdravlje': 'Mesec je idealan za nove sportske rutine. Fokusirajte se na vežbe koje uključuju celu telo.',
            'posao': 'Napredak u karijeri je moguć. Možete očekivati promocije ili nove pozicije.'
        },
        'godisnji': {
            'general': 'Godina novih početaka i prilika za vođstvo. Vaša energija će biti na vrhuncu.',
            'ljubav': 'Strastveni susreti su mogući. Godina je idealna za nove veze ili obnavljanje postojećih.',
            'zdravlje': 'Godina je idealna za nove sportske rutine i poboljšanje fizičke kondicije.',
            'posao': 'Napredak u karijeri je moguć. Možete očekivati promocije ili nove pozicije.'
        }
    },
    'Bik': {
        'dnevni': [
            {
                'general': 'Fokusirajte se na stabilnost i praktične zadatke. Vaša upornost će biti nagrađena.',
                'ljubav': 'Partner traži više pažnje i stabilnosti. Pokazujte svoju posvećenost kroz male gestove. Romantika je praktična ali duboka.',
                'zdravlje': 'Fokusirajte se na vežbe koje uključuju noge i donji deo tela. Hodanje i joga su idealni. Poboljšajte ishranu.',
                'posao': 'Finansijska situacija se poboljšava. Vaša upornost će biti cenjena. Dugoročni projekti donose rezultate.'
            },
            {
                'general': 'Danas je dan za relaksaciju i uživanje u malim radostima. Vaša strpljivost će biti testirana.',
                'ljubav': 'Intimnost je naglašena. Partner će ceniti vašu posvećenost i stabilnost. Romantika je duboka i trajna.',
                'zdravlje': 'Fokusirajte se na opuštanje i meditaciju. Vaša grlo i vrat su pod stresom. Probajte joga vežbe.',
                'posao': 'Postepeno napredovanje je moguće. Vaša strpljivost će biti nagrađena. Budite uporni u ciljevima.'
            },
            {
                'general': 'Vaša strpljivost će biti testirana, ali će biti nagrađena. Danas je idealan za praktične zadatke.',
                'ljubav': 'Stalnost u odnosima je ključna. Partner će ceniti vašu pouzdanost. Romantika je trajna i duboka.',
                'zdravlje': 'Fokusirajte se na vežbe koje uključuju noge. Hodanje i biciklizam su idealni. Poboljšajte ishranu.',
                'posao': 'Dugoročni planovi donose rezultate. Vaša upornost će biti cenjena. Finansijski napredak je moguć.'
            }
        ],
        'nedeljni': {
            'general': 'Nedelja fokusirana na stabilnost i materijalne stvari. Vaša upornost će biti nagrađena.',
            'ljubav': 'Partner će ceniti vašu posvećenost i stabilnost. Nedelja je idealna za dubinske razgovore.',
            'zdravlje': 'Fokusirajte se na vežbe koje uključuju noge. Hodanje i joga su idealni tokom cele nedelje.',
            'posao': 'Finansijski napredak je moguć. Vaša upornost će biti cenjena.'
        },
        'mesecni': {
            'general': 'Mesec fokusiran na materijalnu stabilnost i rast. Vaša upornost će biti nagrađena.',
            'ljubav': 'Dubina u odnosima je naglašena. Partner će ceniti vašu stabilnost i posvećenost.',
            'zdravlje': 'Mesec je idealan za nove sportske rutine koje uključuju noge. Fokusirajte se na stabilnost.',
            'posao': 'Finansijski napredak je moguć. Vaša upornost će biti nagrađena.'
        },
        'godisnji': {
            'general': 'Godina materijalne stabilnosti i rasta. Vaša upornost će biti nagrađena.',
            'ljubav': 'Dubina u odnosima je naglašena. Partner će ceniti vašu stabilnost i posvećenost.',
            'zdravlje': 'Godina je idealna za nove sportske rutine i poboljšanje fizičke kondicije.',
            'posao': 'Finansijski napredak je moguć. Vaša upornost će biti nagrađena.'
        }
    }
}

# Dodaj ostale znakove sa sličnim detaljnim strukturama
for sign in ['Blizanci', 'Rak', 'Lav', 'Devica', 'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe']:
    DETAILED_HOROSCOPES[sign] = {
        'dnevni': [
            {
                'general': f'Danas je pozitivan dan za {sign}. Fokusirajte se na svoje ciljeve i budite optimistični.',
                'ljubav': 'Komunikacija je ključna. Partner će ceniti vašu iskrenost. Očekujte pozitivne promene u ljubavnom životu.',
                'zdravlje': 'Fokusirajte se na vežbe koje odgovaraju vašem znaku. Poboljšajte kvalitet sna i ishranu.',
                'posao': 'Novi projekti donose uspeh. Vaša kreativnost će biti cenjena. Očekujte pozitivne povratne informacije.'
            },
            {
                'general': f'Vaša energija je na vrhuncu danas. {sign} će imati prilike za napredak.',
                'ljubav': 'Romantika je naglašena. Partner će ceniti vašu posvećenost. Očekujte strastvene trenutke.',
                'zdravlje': 'Fokusirajte se na vežbe koje uključuju celu telo. Poboljšajte cirkulaciju kroz fizičke aktivnosti.',
                'posao': 'Liderske pozicije su moguće. Vaša karizma će privući pažnju. Očekujte promocije.'
            },
            {
                'general': f'Danas je idealan dan za {sign} da pokaže svoje sposobnosti. Fokusirajte se na pozitivne stvari.',
                'ljubav': 'Intimnost je naglašena. Partner će ceniti vašu dubinu. Očekujte emotivne trenutke.',
                'zdravlje': 'Fokusirajte se na vežbe koje odgovaraju vašem znaku. Poboljšajte kvalitet sna.',
                'posao': 'Timski rad donosi rezultate. Vaša saradnja će biti cenjena. Očekujte pozitivne promene.'
            }
        ],
        'nedeljni': {
            'general': f'Ova nedelja će biti povoljna za {sign}. Očekujte pozitivne promene.',
            'ljubav': 'Nedelja je idealna za dubinske razgovore. Partner će ceniti vašu posvećenost.',
            'zdravlje': 'Fokusirajte se na vežbe koje odgovaraju vašem znaku tokom cele nedelje.',
            'posao': 'Novi projekti će vam dati priliku da pokažete svoje sposobnosti.'
        },
        'mesecni': {
            'general': f'Ovaj mesec će biti produktivan za {sign}. Fokusirajte se na svoje ciljeve.',
            'ljubav': 'Mesec je idealan za nove veze ili obnavljanje postojećih. Partner će ceniti vašu inicijativu.',
            'zdravlje': 'Mesec je idealan za nove sportske rutine. Fokusirajte se na poboljšanje fizičke kondicije.',
            'posao': 'Napredak u karijeri je moguć. Možete očekivati promocije ili nove pozicije.'
        },
        'godisnji': {
            'general': f'Ova godina će biti puna prilika za {sign}. Budite spremni za nove izazove.',
            'ljubav': 'Godina je idealna za nove veze ili obnavljanje postojećih. Partner će ceniti vašu inicijativu.',
            'zdravlje': 'Godina je idealna za nove sportske rutine i poboljšanje fizičke kondicije.',
            'posao': 'Napredak u karijeri je moguć. Možete očekivati promocije ili nove pozicije.'
        }
    }

def format_detailed_horoscope(sections):
    """Formatira detaljni horoskop sa odvojenim sekcijama"""
    formatted = sections['general'] + "\n\n"
    formatted += "💕 LJUBAV:\n" + sections['ljubav'] + "\n\n"
    formatted += "🏥 ZDRAVLJE:\n" + sections['zdravlje'] + "\n\n"
    formatted += "💼 POSAO:\n" + sections['posao']
    return formatted

def get_local_horoscope(sign, horoscope_type):
    """Generiše lokalni horoskop na osnovu tipa sa detaljnim sekcijama"""
    
    if horoscope_type == 'dnevni':
        horoscopes = DETAILED_HOROSCOPES.get(sign, {}).get('dnevni', [])
        if horoscopes:
            selected = random.choice(horoscopes)
            return format_detailed_horoscope(selected)
        else:
            return f"Danas je dobar dan za {sign}. Fokusirajte se na svoje ciljeve i budite optimistični."
    
    elif horoscope_type == 'nedeljni':
        sections = DETAILED_HOROSCOPES.get(sign, {}).get('nedeljni', {})
        if sections:
            return format_detailed_horoscope(sections)
        else:
            return f"Ova nedelja će biti povoljna za {sign}. Očekujte pozitivne promene."
    
    elif horoscope_type == 'mesecni':
        sections = DETAILED_HOROSCOPES.get(sign, {}).get('mesecni', {})
        if sections:
            return format_detailed_horoscope(sections)
        else:
            return f"Ovaj mesec će biti produktivan za {sign}. Fokusirajte se na svoje ciljeve."
    
    elif horoscope_type == 'godisnji':
        sections = DETAILED_HOROSCOPES.get(sign, {}).get('godisnji', {})
        if sections:
            return format_detailed_horoscope(sections)
        else:
            return f"Ova godina će biti puna prilika za {sign}. Budite spremni za nove izazove."
    
    else:
        return f"Pozitivan period za {sign}. Fokusirajte se na svoje ciljeve i budite optimistični."

def fill_local_horoscopes():
    """Puni bazu sa lokalnim horoskopima"""
    with app.app_context():
        print("🔮 Počinjem punjenje lokalnih horoskopa...")
        
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
                
                # Generiši lokalni horoskop
                print(f"  🔄 Generišem {sign} ({horoscope_type.name})...")
                content = get_local_horoscope(sign, horoscope_type.name)
                
                # Kreiraj novi horoskop
                horoscope = Horoscope(
                    type_id=horoscope_type.id,
                    sign=sign,
                    date=target_date,
                    content=content
                )
                db.session.add(horoscope)
            
            # Sačuvaj sve horoskope za ovaj tip
            db.session.commit()
            print(f"  💾 Sačuvano {len(SIGNS)} {horoscope_type.name} horoskopa")
        
        print("\n✅ Punjenje lokalnih horoskopa završeno!")

if __name__ == '__main__':
    fill_local_horoscopes() 