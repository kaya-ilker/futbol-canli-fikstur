import requests
import pandas as pd
from datetime import datetime, timedelta

def gercek_fikstur_cek():
    # Bot engeline takılmayan ham veri kaynağı
    url = "https://fixturedownload.com/feed/json/epl-2025"
    ligler = {
        "Premier League": "https://fixturedownload.com/feed/json/epl-2025",
        "La Liga": "https://fixturedownload.com/feed/json/la-liga-2025",
        "Serie A": "https://fixturedownload.com/feed/json/serie-a-2025",
        "Bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025"
    }
    
    final_maclar = []
    bugun = datetime.now()
    otuz_gun_sonra = bugun + timedelta(days=30)

    for lig_adi, link in ligler.items():
        try:
            r = requests.get(link, timeout=10)
            data = r.json()
            for m in data:
                # Tarih formatını ayarla (Örn: 2026-04-18T15:00:00Z)
                tarih_str = m['Date'].replace('Z', '')
                t_obj = datetime.fromisoformat(tarih_str)
                
                # Sadece gelecek 30 günün maçlarını al
                if bugun <= t_obj <= otuz_gun_sonra:
                    final_maclar.append({
                        "Lig": lig_adi,
                        "Maç Tarihi": t_obj.strftime("%d.%m.%Y %H:%M"),
                        "Ev Sahibi": m['HomeTeam'],
                        "Deplasman": m['AwayTeam']
                    })
        except:
            continue

    return final_maclar

# Çalıştır ve Kaydet
mac_listesi = gercek_fikstur_cek()
if mac_listesi:
    df = pd.DataFrame(mac_listesi)
    df.to_excel("maclarim.xlsx", index=False)
    print(f"BİTTİ! {len(df)} adet GERÇEK maç verisi yüklendi.")
else:
    print("Veri çekilemedi, lütfen internet bağlantısını kontrol edin.")
