import requests
import pandas as pd
import os
from datetime import datetime

api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# Sadece hedeflediğimiz ana ligler
ligler = {
    "Premier League": 17,
    "Serie A": 23,
    "Bundesliga": 35,
    "LaLiga": 8,
    "Trendyol Süper Lig": 52
}

tum_fikstur = []
mevcut_ay = datetime.now().month
mevcut_yil = datetime.now().year

print(f"--- {mevcut_ay}. Ay Fikstür Taraması Başladı ---")

for lig_adi, lig_id in ligler.items():
    # 'events' kapısı yerine sezonluk tüm maçları getiren kapı
    url = f"https://sportapi7.p.rapidapi.com/api/v1/tournament/{lig_id}/season/latest/matches/next/0"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if 'events' in data:
            for m in data['events']:
                # Unix zaman damgasını tarihe çevir
                tarih_obj = datetime.fromtimestamp(m.get('startTimestamp', 0))
                
                # FİLTRE: Sadece bu ayın maçlarını veya gelecek maçları al
                if tarih_obj.year == mevcut_yil and tarih_obj.month == mevcut_ay:
                    tum_fikstur.append({
                        "Lig": lig_adi,
                        "Tarih": tarih_obj.strftime('%d.%m.%Y'),
                        "Saat": tarih_obj.strftime('%H:%M'),
                        "Ev Sahibi": m.get('homeTeam', {}).get('name', 'Bilinmiyor'),
                        "Deplasman": m.get('awayTeam', {}).get('name', 'Bilinmiyor'),
                        "Durum": "Planlandı" # Skor gelmesini engellemek için sabit yazı
                    })
    except Exception as e:
        print(f"{lig_adi} taranırken hata: {e}")

# Verileri düzenleme ve temizleme
if tum_fikstur:
    df = pd.DataFrame(tum_fikstur)
    # Gereksiz tüm yan verileri (hazırlık maçı vs.) temizlemek için lig adını kontrol et
    df = df[df['Lig'].isin(ligler.keys())] 
    
    # Tarihe göre kronolojik sırala
    df['Sıralama'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y')
    df = df.sort_values(by=['Sıralama', 'Saat']).drop(columns=['Sıralama'])
    
    df.to_excel("maclarim.xlsx", index=False)
    print(f"İşlem Tamam: {len(df)} maç listelendi.")
else:
    print("Kriterlere uygun maç bulunamadı.")
