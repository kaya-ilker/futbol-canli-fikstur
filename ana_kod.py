import requests
import pandas as pd
from datetime import datetime, timedelta

def veri_cek():
    # Bu yöntem, web sitesinin görselini değil, arka plandaki veri tabanını hedefler (daha garantidir)
    url = "https://fixturedownload.com/feed/json/epl-2025" # Örnek: Premier League
    maclar = []
    
    # Hedeflediğimiz 5 lig için farklı veri kanalları
    # Not: Bu kaynaklar ücretsiz ve herkese açık JSON beslemeleridir.
    kanallar = {
        "Premier League": "https://fixturedownload.com/feed/json/epl-2025",
        "La Liga": "https://fixturedownload.com/feed/json/la-liga-2025",
        "Serie A": "https://fixturedownload.com/feed/json/serie-a-2025",
        "Bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025"
    }
    
    bugun = datetime.now()
    bir_ay_sonra = bugun + timedelta(days=30)

    print("Veri kanallarına bağlanılıyor...")

    for lig_adi, url in kanallar.items():
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            
            for m in data:
                # Tarih formatını ayarla (2026-04-18T15:00:00Z formatında geliyor)
                mac_tarihi = datetime.strptime(m['Date'][:16], '%Y-%m-%dT%H:%M')
                
                # Sadece önümüzdeki 30 günün maçları
                if bugun <= mac_tarihi <= bir_ay_sonra:
                    maclar.append({
                        "Lig": lig_adi,
                        "Maç Tarihi": mac_tarihi.strftime('%d.%m.%Y %H:%M'),
                        "Ev Sahibi": m['HomeTeam'],
                        "Deplasman": m['AwayTeam']
                    })
        except Exception as e:
            print(f"{lig_adi} çekilirken hata oluştu: {e}")

    return maclar

# Çalıştır
sonuclar = veri_cek()

if sonuclar:
    df = pd.DataFrame(sonuclar)
    # Sadece istediğin 4 sütun
    df = df[["Lig", "Maç Tarihi", "Ev Sahibi", "Deplasman"]]
    df.to_excel("maclarim.xlsx", index=False)
    print(f"Başarılı! {len(sonuclar)} maç bulundu ve Excel güncellendi.")
else:
    print("Maç bulunamadı. Lütfen kanalları kontrol edin.")
