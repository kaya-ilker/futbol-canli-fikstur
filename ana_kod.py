import requests
import pandas as pd
import os

api_key = os.getenv('RAPIDAPI_KEY')
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

# Test için Türkiye Süper Ligi (203) ve 2025 sezonu
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?league=203&season=2025"

maclar = []
hata_notu = ""

try:
    r = requests.get(url, headers=headers)
    data = r.json()
    
    # API'den gelen mesajı kontrol et
    if 'errors' in data and data['errors']:
        hata_notu = str(data['errors'])
    elif 'response' in data and len(data['response']) > 0:
        for m in data['response']:
            maclar.append({
                "Lig": m['league']['name'],
                "Tarih": m['fixture']['date'][:10],
                "Ev": m['teams']['home']['name'],
                "Dep": m['teams']['away']['name']
            })
    else:
        hata_notu = "API bağlandı ama bu lig/sezon için maç bulunamadı."

except Exception as e:
    hata_notu = f"Bağlantı hatası: {str(e)}"

# Eğer maç yoksa hatayı Excel'e yaz
if not maclar:
    maclar = [{"Lig": "HATA RAPORU", "Tarih": hata_notu, "Ev": "-", "Dep": "-"}]

df = pd.DataFrame(maclar)
df.to_excel("maclarim.xlsx", index=False)
