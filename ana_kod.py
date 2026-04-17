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

# SADECE BU LİGLERİ KABUL ET (Korumalı Liste)
hedef_ligler = {
    "Premier League": 17,
    "Serie A": 23,
    "Bundesliga": 35,
    "LaLiga": 8,
    "Trendyol Süper Lig": 52
}

final_listesi = []
bugun = datetime.now()
otuz_gun_sonra = bugun + timedelta(days=30)

print("Ayıklama işlemi başladı... Gereksiz ligler ve canlı skorlar eleniyor.")

for lig_adi, lig_id in hedef_ligler.items():
    # Canlı maçlar yerine sezonluk fikstür endpoint'ini kullanıyoruz
    url = f"https://sportapi7.p.rapidapi.com/api/v1/tournament/{lig_id}/season/latest/matches/next/0"
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if 'events' in data:
            for m in data['events']:
                # KURAL 1: Sadece henüz başlamamış maçları al (Skorlu maçları engeller)
                status = m.get('status', {}).get('type', '')
                if status != 'notstarted': 
                    continue
                
                tarih_ts = m.get('startTimestamp', 0)
                tarih_obj = datetime.fromtimestamp(tarih_ts)
                
                # KURAL 2: Sadece önümüzdeki 30 gün içindeki maçları al
                if bugun <= tarih_obj <= otuz_gun_sonra:
                    final_listesi.append({
                        "Lig": lig_adi,
                        "Maç Tarihi": tarih_obj.strftime('%d.%m.%Y %H:%M'),
                        "Ev Sahibi": m.get('homeTeam', {}).get('name', 'Bilinmiyor'),
                        "Deplasman": m.get('awayTeam', {}).get('name', 'Bilinmiyor')
                    })
    except Exception as e:
        print(f"{lig_adi} taranırken hata: {e}")

# Veriyi İşleme
if final_listesi:
    df = pd.DataFrame(final_listesi)
    
    # Tarih sıralaması (En yakın maç en üstte)
    df['sort_date'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values(by='sort_date').drop(columns=['sort_date'])
    
    # SADECE İSTEDİĞİN 4 SÜTUN (Skor sütunu burada eleniyor)
    df = df[["Lig", "Maç Tarihi", "Ev Sahibi", "Deplasman"]]
    
    df.to_excel("maclarim.xlsx", index=False)
    print(f"Bitti! {len(df)} adet tertemiz fikstür verisi kaydedildi.")
else:
    print("Kriterlere uygun gelecek maç bulunamadı.")
