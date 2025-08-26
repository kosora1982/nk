from local_ai_interpreter import generate_local_ai_interpretation

def test_local_ai():
    """Test lokalnog AI tumača"""
    print("🧪 Testiram lokalni AI tumač...")
    
    # Test podaci
    name = "Mladen"
    planets = {
        'Sun': 'Lav',
        'Moon': 'Rak',
        'Mercury': 'Lav',
        'Venus': 'Devica',
        'Mars': 'Ovan',
        'Jupiter': 'Vaga',
        'Saturn': 'Jarac',
        'Uranus': 'Vodolija',
        'Neptune': 'Ribe',
        'Pluto': 'Škorpija'
    }
    asc_sign = 'Bik'
    
    print(f"\n📊 Test podaci:")
    print(f"Ime: {name}")
    print(f"Ascendent: {asc_sign}")
    print("Planete:")
    for planet, sign in planets.items():
        print(f"  {planet}: {sign}")
    
    print("\n" + "="*60)
    print("🎯 REZULTAT LOKALNOG AI TUMUČENJA:")
    print("="*60)
    
    # Generiši tumačenje
    interpretation = generate_local_ai_interpretation(name, planets, asc_sign)
    print(interpretation)
    
    print("\n✅ Test završen!")

if __name__ == '__main__':
    test_local_ai() 