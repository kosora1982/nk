import requests

def test_api_availability():
    """Testira da li je API uopšte dostupan"""
    
    base_url = "https://horoscope-api.herokuapp.com"
    
    print("🔍 Testiram dostupnost API-ja...")
    print("=" * 40)
    
    # Test 1: Osnovni endpoint
    try:
        response = requests.get(base_url, timeout=10)
        print(f"📡 Osnovni endpoint: HTTP {response.status_code}")
        if response.status_code == 200:
            print("  ✅ API je dostupan")
        else:
            print("  ❌ API nije dostupan")
    except Exception as e:
        print(f"  ❌ Greška: {str(e)}")
    
    # Test 2: Horoscope endpoint
    try:
        response = requests.get(f"{base_url}/horoscope", timeout=10)
        print(f"📡 Horoscope endpoint: HTTP {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Horoscope endpoint radi")
        else:
            print("  ❌ Horoscope endpoint ne radi")
    except Exception as e:
        print(f"  ❌ Greška: {str(e)}")
    
    # Test 3: Pokušaj sa drugim endpoint-om
    try:
        response = requests.get(f"{base_url}/horoscope/today/aries", timeout=10)
        print(f"📡 Today endpoint: HTTP {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Today endpoint radi")
            data = response.json()
            print(f"  📝 Sadržaj: {data}")
        else:
            print("  ❌ Today endpoint ne radi")
    except Exception as e:
        print(f"  ❌ Greška: {str(e)}")

if __name__ == '__main__':
    test_api_availability() 