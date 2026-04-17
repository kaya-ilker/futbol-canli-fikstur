import requests
import pandas as pd
import os
from datetime import datetime

api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# İstediğin Liglerin ID Listesi (SportAPI standartlarına göre)
ligler = {
    "Premier League": 17,
    "Serie A": 23,
    "Bundesliga": 35,
    "LaLiga": 8,
    "Trendyol Süper Lig": 52,
    "Champions League": 7,
    "Europa League": 679,
    "Conference League": 17012,
    "Euro 2024/2026": 1,
    "FIFA World Cup": 28
}

maclar = []

print("Fikstürler taranıyor...")

for lig_adi, lig_id in ligler.items():
    # Belirli bir lig için gelecek maçları çekiyoruz
    url = f"https://sportapi7.p.rapidapi.com/api/v1/tournament/{lig_id}/season/latest/matches/next/0"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if 'events' in data:
            for m in data['events']:
                # Unix zaman damgasını okunabilir tarihe çevirelim
                dt_obj = datetime.fromtimestamp(m.get('startTimestamp', 0))
                
                maclar.append({
                    "Lig": lig_adi,
                    "Tarih": dt_obj.strftime('%d.%m.%Y'),
                    "Saat": dt_obj.strftime('%H:%M'),
                    "Ev Sahibi": m.get('homeTeam', {}).get('name', '-'),
                    "Deplasman": m.get('awayTeam', {}).get('name', '-')
                })
    except Exception as e:
        print(f"{lig_adi} çekilirken hata oluştu: {e}")

# Excel'e aktar
if maclar:
    df = pd.DataFrame(maclar)
    df = df[["Lig", "Tarih", "Saat", "Ev Sahibi", "Deplasman"]]
    df.sort_values(by=["Tarih", "Saat"], inplace=True)
    df.to_excel("maclarim.xlsx", index=False)
    print("İşlem başarıyla tamamlandı.")
else:
    print("Hiç maç verisi bulunamadı.")
