import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# API Ayarları
api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# Hedef Ligler
ligler = {
    "Premier League": 17,
    "Serie A": 23,
    "Bundesliga": 35,
    "LaLiga": 8,
    "Trendyol Süper Lig": 52
}

maclar_listesi = []
bugun = datetime.now()
bir_ay_sonra = bugun + timedelta(days=30)

print(f"{bugun.strftime('%d.%m.%Y')} - {bir_ay_sonra.strftime('%d.%m.%Y')} arası taranıyor...")

for lig_adi, lig_id in ligler.items():
    # Sezonun tüm maçlarını içeren endpoint
    url = f"https://sportapi7.p.rapidapi.com/api/v1/tournament/{lig_id}/season/latest/matches/next/0"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if 'events' in data:
            for m in data['events']:
                tarih_ts = m.get('startTimestamp', 0)
                tarih_obj = datetime.fromtimestamp(tarih_ts)
                
                # FİLTRE: Sadece önümüzdeki 30 gün içindeki maçlar
                if bugun <= tarih_obj <= bir_ay_sonra:
                    maclar_listesi.append({
                        "Lig": lig_adi,
                        "Maç Tarihi": tarih_obj.strftime('%d.%m.%Y %H:%M'),
                        "Ev Sahibi": m.get('homeTeam', {}).get('name', 'Bilinmiyor'),
                        "Deplasman": m.get('awayTeam', {}).get('name', 'Bilinmiyor')
                    })
    except Exception as e:
        print(f"{lig_adi} çekilirken bir sorun oluştu: {e}")

# Veriyi İşleme ve Excel'e Yazma
if maclar_listesi:
    df = pd.DataFrame(maclar_listesi)
    
    # Tarihe göre sıralama yapalım
    df['temp_date'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values(by='temp_date').drop(columns=['temp_date'])
    
    # Excel'e kaydet
    df.to_excel("maclarim.xlsx", index=False)
    print(f"Başarılı! {len(df)} adet maç Excel'e eklendi.")
else:
    print("Belirtilen tarih aralığında maç bulunamadı.")
