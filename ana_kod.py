import requests
import pandas as pd
import os

api_key = os.getenv('RAPIDAPI_KEY')
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

# Hem Türkiye (203) hem İngiltere (39) liglerini deneyelim
# Sezonu da 2025 ve 2026 olarak test edelim
ligler = [203, 39]
sezonlar = [2025, 2026]

maclar = []

for lig in ligler:
    for sezon in sezonlar:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={lig}&season={sezon}"
        try:
            r = requests.get(url, headers=headers)
            data = r.json()
            if 'response' in data and len(data['response']) > 0:
                for m in data['response']:
                    maclar.append({
                        "Lig": m['league']['name'],
                        "Tarih": m['fixture']['date'][:10],
                        "Ev": m['teams']['home']['name'],
                        "Dep": m['teams']['away']['name']
                    })
        except:
            continue

if not maclar:
    maclar = [{"Lig": "Hala veri yok", "Tarih": "API anahtarini kontrol et", "Ev": "-", "Dep": "-"}]

pd.DataFrame(maclar).to_excel("maclarim.xlsx", index=False)
print("Islem bitti.")
