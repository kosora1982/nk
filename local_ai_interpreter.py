import random
from datetime import datetime

class LocalAIInterpreter:
    """Lokalni AI tumač horoskopa koji generiše tumačenja na osnovu pozicija planeta"""
    
    def __init__(self):
        self.planetary_aspects = {
            'Sun': {
                'positive': ['kreativnost', 'vođstvo', 'energiju', 'samopouzdanje', 'inicijativu'],
                'negative': ['egoizam', 'dominaciju', 'nestrpljenje', 'agresivnost'],
                'areas': ['ličnost', 'ego', 'vitalnost', 'muški princip']
            },
            'Moon': {
                'positive': ['intuiciju', 'osetljivost', 'emotivnost', 'maštu', 'porodične veze'],
                'negative': ['nestabilnost', 'promenljivost', 'osetljivost', 'emocionalne blokade'],
                'areas': ['emocije', 'intuicija', 'porodica', 'ženski princip']
            },
            'Mercury': {
                'positive': ['komunikaciju', 'intelekt', 'logiku', 'učenje', 'razumevanje'],
                'negative': ['nervozu', 'previše analize', 'kritičnost', 'komunikacijske probleme'],
                'areas': ['komunikacija', 'intelekt', 'učenje', 'trgovina']
            },
            'Venus': {
                'positive': ['ljubav', 'harmoniju', 'lepotu', 'umetnost', 'romantiku'],
                'negative': ['zavisnost', 'površnost', 'ljubomoru', 'hedonizam'],
                'areas': ['ljubav', 'umetnost', 'harmonija', 'vrednosti']
            },
            'Mars': {
                'positive': ['energiju', 'hrabrost', 'inicijativu', 'sport', 'akciju'],
                'negative': ['agresivnost', 'nestrpljenje', 'konflikte', 'impulsivnost'],
                'areas': ['energija', 'akcija', 'sport', 'seksualnost']
            },
            'Jupiter': {
                'positive': ['optimizam', 'ekspanziju', 'mudrost', 'sreću', 'razvoj'],
                'negative': ['prekomernost', 'optimizam', 'ekstravaganciju'],
                'areas': ['mudrost', 'religija', 'filozofija', 'putovanja']
            },
            'Saturn': {
                'positive': ['disciplinu', 'odgovornost', 'mudrost', 'stabilnost', 'strukturu'],
                'negative': ['ograničenja', 'strahove', 'blokade', 'pesimizam'],
                'areas': ['odgovornost', 'karijera', 'struktura', 'ograničenja']
            },
            'Uranus': {
                'positive': ['inovaciju', 'originalnost', 'revoluciju', 'slobodu', 'genijalnost'],
                'negative': ['nepredvidljivost', 'destabilizaciju', 'ekstremizam'],
                'areas': ['inovacije', 'tehnologija', 'sloboda', 'revolucija']
            },
            'Neptune': {
                'positive': ['intuiciju', 'duhovnost', 'umetnost', 'inspiraciju', 'idealizam'],
                'negative': ['iluzije', 'dezorijentaciju', 'eskapizam', 'zavisnosti'],
                'areas': ['duhovnost', 'umetnost', 'iluzije', 'inspiracija']
            },
            'Pluto': {
                'positive': ['transformaciju', 'moć', 'intenzitet', 'regeneraciju', 'dubinu'],
                'negative': ['destruktivnost', 'opsesije', 'ekstremizam', 'manipulaciju'],
                'areas': ['transformacija', 'moć', 'psihologija', 'tabu']
            }
        }
        
        self.zodiac_signs = {
            'Ovan': {'element': 'vatra', 'quality': 'kardinal', 'ruler': 'Mars'},
            'Bik': {'element': 'zemlja', 'quality': 'fiksni', 'ruler': 'Venus'},
            'Blizanci': {'element': 'vazduh', 'quality': 'promenljivi', 'ruler': 'Mercury'},
            'Rak': {'element': 'voda', 'quality': 'kardinal', 'ruler': 'Moon'},
            'Lav': {'element': 'vatra', 'quality': 'fiksni', 'ruler': 'Sun'},
            'Devica': {'element': 'zemlja', 'quality': 'promenljivi', 'ruler': 'Mercury'},
            'Vaga': {'element': 'vazduh', 'quality': 'kardinal', 'ruler': 'Venus'},
            'Škorpija': {'element': 'voda', 'quality': 'fiksni', 'ruler': 'Pluto'},
            'Strelac': {'element': 'vatra', 'quality': 'promenljivi', 'ruler': 'Jupiter'},
            'Jarac': {'element': 'zemlja', 'quality': 'kardinal', 'ruler': 'Saturn'},
            'Vodolija': {'element': 'vazduh', 'quality': 'fiksni', 'ruler': 'Uranus'},
            'Ribe': {'element': 'voda', 'quality': 'promenljivi', 'ruler': 'Neptune'}
        }
        
        self.aspects = {
            'conjunction': 'spoj',
            'opposition': 'opozicija',
            'trine': 'trigon',
            'square': 'kvadratura',
            'sextile': 'sekstil'
        }
    
    def interpret_planetary_position(self, planet, sign, house=None):
        """Tumači poziciju planete u znaku"""
        planet_info = self.planetary_aspects.get(planet, {})
        sign_info = self.zodiac_signs.get(sign, {})
        
        if not planet_info or not sign_info:
            return f"{planet} u {sign} donosi promene u vašem životu."
        
        # Odredi da li je pozicija harmonična ili teška
        is_harmonious = random.choice([True, False, True])  # 66% šanse za harmoničnu poziciju
        
        if is_harmonious:
            positive_traits = random.sample(planet_info['positive'], min(2, len(planet_info['positive'])))
            interpretation = f"{planet} u {sign} pojačava vašu {', '.join(positive_traits)}. "
            interpretation += f"Ova pozicija donosi pozitivne promene u oblasti {planet_info['areas'][0]}."
        else:
            negative_traits = random.sample(planet_info['negative'], min(1, len(planet_info['negative'])))
            interpretation = f"{planet} u {sign} može da izazove {', '.join(negative_traits)}. "
            interpretation += f"Budite svesni ovih izazova i radite na njihovom prevazilaženju."
        
        return interpretation
    
    def interpret_ascendant(self, asc_sign):
        """Tumači ascendent"""
        sign_info = self.zodiac_signs.get(asc_sign, {})
        if not sign_info:
            return f"Ascendent u {asc_sign} utiče na vaš pristup životu."
        
        interpretations = [
            f"Ascendent u {asc_sign} pokazuje da ste {sign_info['element']} osoba sa {sign_info['quality']} kvalitetom.",
            f"Vaš {asc_sign} ascendent utiče na to kako vas vide drugi i kako pristupate novim situacijama.",
            f"Sa {asc_sign} ascendentom, vaš pristup životu je karakterisan {sign_info['element']} elementom."
        ]
        
        return random.choice(interpretations)
    
    def generate_love_interpretation(self, planets, asc_sign):
        """Generiše tumačenje za ljubav"""
        love_planets = ['Venus', 'Mars', 'Moon']
        love_interpretations = []
        
        for planet in love_planets:
            if planet in planets:
                sign = planets[planet]
                interpretation = self.interpret_planetary_position(planet, sign)
                love_interpretations.append(f"💕 {planet} u {sign}: {interpretation}")
        
        if not love_interpretations:
            love_interpretations.append("💕 Vaš ljubavni život je pod uticajem trenutnih planetarnih pozicija.")
        
        return "\n".join(love_interpretations)
    
    def generate_health_interpretation(self, planets, asc_sign):
        """Generiše tumačenje za zdravlje"""
        health_planets = ['Mars', 'Saturn', 'Sun']
        health_interpretations = []
        
        for planet in health_planets:
            if planet in planets:
                sign = planets[planet]
                interpretation = self.interpret_planetary_position(planet, sign)
                health_interpretations.append(f"🏥 {planet} u {sign}: {interpretation}")
        
        if not health_interpretations:
            health_interpretations.append("🏥 Vaše zdravlje je pod uticajem trenutnih planetarnih pozicija.")
        
        return "\n".join(health_interpretations)
    
    def generate_career_interpretation(self, planets, asc_sign):
        """Generiše tumačenje za karijeru"""
        career_planets = ['Saturn', 'Jupiter', 'Mercury']
        career_interpretations = []
        
        for planet in career_planets:
            if planet in planets:
                sign = planets[planet]
                interpretation = self.interpret_planetary_position(planet, sign)
                career_interpretations.append(f"💼 {planet} u {sign}: {interpretation}")
        
        if not career_interpretations:
            career_interpretations.append("💼 Vaša karijera je pod uticajem trenutnih planetarnih pozicija.")
        
        return "\n".join(career_interpretations)
    
    def generate_comprehensive_interpretation(self, name, planets, asc_sign):
        """Generiše sveobuhvatno tumačenje natalne karte"""
        
        # Uvod
        introduction = f"🎯 NATALNA KARTA ZA {name.upper()}\n"
        introduction += f"📅 Datum analize: {datetime.now().strftime('%d.%m.%Y')}\n"
        introduction += "=" * 50 + "\n\n"
        
        # Opšte tumačenje
        general_interpretation = "🌟 OPŠTE TUMUČENJE:\n"
        general_interpretation += f"Vaša natalna karta pokazuje jedinstvenu kombinaciju planetarnih uticaja. "
        general_interpretation += f"Ascendent u {asc_sign} utiče na vaš pristup životu i kako vas vide drugi.\n\n"
        
        # Planetarna tumačenja
        planetary_interpretations = "🪐 PLANETARNE POZICIJE:\n"
        for planet, sign in planets.items():
            interpretation = self.interpret_planetary_position(planet, sign)
            planetary_interpretations += f"• {planet} u {sign}: {interpretation}\n"
        planetary_interpretations += "\n"
        
        # Ascendent tumačenje
        asc_interpretation = f"🌅 ASCENDENT:\n{self.interpret_ascendant(asc_sign)}\n\n"
        
        # Specifična tumačenja
        love_interpretation = "💕 LJUBAV I ODNOSI:\n" + self.generate_love_interpretation(planets, asc_sign) + "\n\n"
        health_interpretation = "🏥 ZDRAVLJE I VITALNOST:\n" + self.generate_health_interpretation(planets, asc_sign) + "\n\n"
        career_interpretation = "💼 KARIJERA I POSAO:\n" + self.generate_career_interpretation(planets, asc_sign) + "\n\n"
        
        # Zaključak
        conclusion = "🎯 ZAKLJUČAK:\n"
        conclusion += "Vaša natalna karta pokazuje potencijal za rast i razvoj. "
        conclusion += "Koristite ove uvide da bolje razumete sebe i svoje mogućnosti. "
        conclusion += "Pametno korišćenje ovih informacija može vam pomoći u svim oblastima života.\n\n"
        conclusion += "✨ Srećno na vašem astrološkom putovanju!"
        
        return (introduction + general_interpretation + planetary_interpretations + 
                asc_interpretation + love_interpretation + health_interpretation + 
                career_interpretation + conclusion)

def generate_local_ai_interpretation(name, planets, asc_sign):
    """Glavna funkcija za generisanje lokalnog AI tumačenja"""
    interpreter = LocalAIInterpreter()
    return interpreter.generate_comprehensive_interpretation(name, planets, asc_sign) 