from local_ai_interpreter import LocalAIInterpreter

def test_simple_ai():
    """Test lokalnog AI tumača - jednostavna verzija"""
    print("🧪 Testiram lokalni AI tumač...")
    
    interpreter = LocalAIInterpreter()
    
    # Test planetarne pozicije
    print("\n📊 Test planetarne pozicije:")
    interpretation = interpreter.interpret_planetary_position('Sun', 'Lav')
    print(f"Sun u Lav: {interpretation}")
    
    interpretation = interpreter.interpret_planetary_position('Venus', 'Devica')
    print(f"Venus u Devica: {interpretation}")
    
    # Test ascendent
    print("\n🌅 Test ascendent:")
    asc_interpretation = interpreter.interpret_ascendant('Bik')
    print(f"Ascendent Bik: {asc_interpretation}")
    
    # Test ljubav
    print("\n💕 Test ljubav:")
    planets = {'Venus': 'Devica', 'Mars': 'Ovan', 'Moon': 'Rak'}
    love_interpretation = interpreter.generate_love_interpretation(planets, 'Bik')
    print(love_interpretation)
    
    print("\n✅ Test završen!")

if __name__ == '__main__':
    test_simple_ai() 