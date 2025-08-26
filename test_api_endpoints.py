import requests
import time

def test_api_endpoints():
    """Testira sve API endpointe za horoskope"""
    
    base_url = "https://horoscope-api.herokuapp.com/horoscope"
    signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    
    endpoints = [
        'daily',
        'weekly', 
        'monthly',
        'yearly'
    ]
    
    print("🔍 Testiram API endpointe za horoskope...")
    print("=" * 50)
    
    for endpoint in endpoints:
        print(f"\n📅 Testiram {endpoint.upper()} endpoint:")
        print("-" * 30)
        
        working_signs = []
        failed_signs = []
        
        for sign in signs:
            url = f"{base_url}/{endpoint}/{sign}"
            
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    horoscope_text = data.get('horoscope', 'Nema sadržaja')
                    print(f"  ✅ {sign}: {horoscope_text[:50]}...")
                    working_signs.append(sign)
                else:
                    print(f"  ❌ {sign}: HTTP {response.status_code}")
                    failed_signs.append(sign)
                    
            except Exception as e:
                print(f"  ❌ {sign}: Greška - {str(e)}")
                failed_signs.append(sign)
            
            # Pauza između zahteva
            time.sleep(0.2)
        
        print(f"\n📊 Rezultat za {endpoint}:")
        print(f"  ✅ Radi: {len(working_signs)} znakova")
        print(f"  ❌ Ne radi: {len(failed_signs)} znakova")
        
        if failed_signs:
            print(f"  Neuspešni znakovi: {', '.join(failed_signs)}")

if __name__ == '__main__':
    test_api_endpoints() 