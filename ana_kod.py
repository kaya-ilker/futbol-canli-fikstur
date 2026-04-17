import requests
import pandas as pd
import os
from datetime import datetime

api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# Sadece senin istediğin 5 ana lig
ligler = {
    "Premier League": 17,
    "Serie A": 23,
    "Bundesliga": 35,
    "LaLiga": 8,
    "Trendyol Süper Lig": 52
}

tum_maclar = []

for lig_adi, lig_id in ligler.items():
    print(f"{lig_adi} fikstürü alınıyor...")
    # 'next/0' yerine tüm sezon fikstürünü çekmeye çalışan endpoint'i kullanalım
    url = f"https://sportapi7.p.rapidapi.com/api/v1/tournament/{lig_id}/season/latest/matches/next/0"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if 'events' in data:
            for m in data['events']:
                # Sadece henüz başlamamış (not_started) maçları filtreleyelim
                status = m.get('status', {}).get('type', '')
                if status == 'finished': continue # Biten maçları alma
                
                dt_obj = datetime.fromtimestamp(m.get('startTimestamp', 0))
                
                tum_maclar.append({
                    "Lig": lig_adi,
                    "Tarih": dt_obj.strftime('%d.%m.%Y'),
                    "Saat": dt_obj.strftime('%H:%M'),
                    "Ev Sahibi": m.get('homeTeam', {}).get('name', 'Bilinmiyor'),
                    "Deplasman": m.get('awayTeam', {}).get('name', 'Bilinmiyor')
                })
    except Exception as e:
        print(f"{lig_adi} hatası: {e}")

# Excel Oluşturma
if tum_maclar:
    df = pd.DataFrame(tum_maclar)
    # Tarih ve Saat'e göre sırala ki karmaşa olmasın
    df['Sıralama Tarihi'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y')
    df = df.sort_values(by=['Sıralama Tarihi', 'Saat']).drop(columns=['Sıralama Tarihi'])
    
    df.to_excel("maclarim.xlsx", index=False)
    print("Fikstür başarıyla hazırlandı.")
else:
    print("Veri çekilemedi, lütfen API aboneliğini ve anahtarı kontrol edin.")
