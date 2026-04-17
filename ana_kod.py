import requests
import pandas as pd
from datetime import datetime, timedelta

def nihai_veri_cekici():
    # Bu kaynak, futbol verilerini ham metin olarak sunan ve bot engeli olmayan bir depodur.
    # Premier League için alternatif ve çok stabil bir URL kullanıyoruz.
    urls = {
        "Premier League": "https://fixturedownload.com/feed/json/epl-2025",
        "La Liga": "https://fixturedownload.com/feed/json/la-liga-2025",
        "Serie A": "https://fixturedownload.com/feed/json/serie-a-2025",
        "Bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025"
    }
    
    maclar = []
    bugun = datetime.now()
    otuz_gun_sonra = bugun + timedelta(days=30)
    
    print("Veri kanalları taranıyor...")

    for lig, url in urls.items():
        try:
            # JSON verisini çek
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for m in data:
                    # Tarihi işle: "2026-04-18T15:00:00Z" formatını okur
                    tarih_str = m['Date'].replace('Z', '')
                    t_obj = datetime.fromisoformat(tarih_str)
                    
                    # Sadece önümüzdeki 30 günün maçları
                    if bugun <= t_obj <= otuz_gun_sonra:
                        maclar.append({
                            "Lig": lig,
                            "Maç Tarihi": t_obj.strftime("%d.%m.%Y %H:%M"),
                            "Ev Sahibi": m['HomeTeam'],
                            "Deplasman": m['AwayTeam']
                        })
                print(f"{lig} verisi başarıyla alındı.")
        except Exception as e:
            print(f"{lig} çekilirken hata: {e}")

    return maclar

# Çalıştır
liste = nihai_veri_cekici()

if liste:
    df = pd.DataFrame(liste)
    # Tarihe göre sırala
    df['sort'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values('sort').drop('sort', axis=1)
    
    df.to_excel("maclarim.xlsx", index=False)
    print(f"BİTTİ! Toplam {len(df)} gerçek maç Excel'e yazıldı.")
else:
    print("Maç bulunamadı. Statik mod için bir önceki yedek planı devreye alabilirsiniz.")
