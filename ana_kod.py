import requests
import pandas as pd
from datetime import datetime, timedelta

def gercek_verileri_topla():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    # 5 büyük ligin SofaScore üzerindeki benzersiz ID'leri
    lig_idleri = {
        "Premier League": 17,
        "LaLiga": 8,
        "Serie A": 23,
        "Bundesliga": 35,
        "Trendyol Süper Lig": 52
    }
    
    maclar = []
    bugun = datetime.now()
    otuz_gun_sonra = bugun + timedelta(days=30)
    
    print("Gerçek takımlar çekiliyor...")

    for lig_adi, lig_id in lig_idleri.items():
        try:
            # API'den o ligin son/gelecek maçlarını çekiyoruz
            url = f"https://api.sofascore.com/api/v1/tournament/{lig_id}/season/latest/events/next/0"
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            
            if 'events' in data:
                for event in data['events']:
                    ts = event.get('startTimestamp')
                    mac_zamani = datetime.fromtimestamp(ts)
                    
                    # Sadece önümüzdeki 30 günün maçları
                    if bugun <= mac_zamani <= otuz_gun_sonra:
                        maclar.append({
                            "Lig": lig_adi,
                            "Maç Tarihi": mac_zamani.strftime("%d.%m.%Y %H:%M"),
                            "Ev Sahibi": event.get('homeTeam', {}).get('name', 'Bilinmiyor'),
                            "Deplasman": event.get('awayTeam', {}).get('name', 'Bilinmiyor')
                        })
        except Exception as e:
            print(f"{lig_adi} çekilirken hata: {e}")

    return maclar

# Çalıştır ve Kaydet
sonuc_listesi = gercek_verileri_topla()

if sonuc_listesi:
    df = pd.DataFrame(sonuc_listesi)
    # Tarihe göre sıralayalım
    df['temp_date'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values('temp_date').drop('temp_date', axis=1)
    
    # Excel'e yaz
    df.to_excel("maclarim.xlsx", index=False)
    print(f"BAŞARILI! {len(df)} adet gerçek maç Excel'e işlendi.")
else:
    print("Maç bulunamadı, liste güncellenmedi.")
