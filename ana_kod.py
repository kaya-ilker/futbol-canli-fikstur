import requests
import pandas as pd
from datetime import datetime, timedelta

def nihai_esnek_cekici():
    kanallar = {
        "Premier League": "https://fixturedownload.com/feed/json/epl-2025",
        "La Liga": "https://fixturedownload.com/feed/json/la-liga-2025",
        "Serie A": "https://fixturedownload.com/feed/json/serie-a-2025",
        "Bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025"
    }
    
    maclar = []
    # Zaman filtresini genişletiyoruz: Dünden başla, 45 gün sonrasına git
    # Böylece saat farkı nedeniyle maç kaçırmayız.
    baslangic = datetime.now() - timedelta(days=1)
    bitis = datetime.now() + timedelta(days=45)
    
    print(f"Tarama aralığı: {baslangic.strftime('%d.%m')} - {bitis.strftime('%d.%m')}")

    for lig_adi, url in kanallar.items():
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                lig_mac_sayisi = 0
                for m in data:
                    ham_tarih = m.get('Date') or m.get('date')
                    ev = m.get('HomeTeam') or m.get('homeTeam')
                    dep = m.get('AwayTeam') or m.get('awayTeam')
                    
                    if ham_tarih and ev:
                        # Tarih formatını temizleme
                        t_temiz = ham_tarih.replace('Z', '').split('.')[0]
                        try:
                            t_obj = datetime.fromisoformat(t_temiz)
                            
                            # Filtre: Sadece belirlediğimiz aralıktaki maçlar
                            if baslangic <= t_obj <= bitis:
                                maclar.append({
                                    "Lig": lig_adi,
                                    "Maç Tarihi": t_obj.strftime("%d.%m.%Y %H:%M"),
                                    "Ev Sahibi": ev,
                                    "Deplasman": dep
                                })
                                lig_mac_sayisi += 1
                        except: continue
                print(f"{lig_adi}: {lig_mac_sayisi} maç bulundu.")
        except Exception as e:
            print(f"{lig_adi} hatası: {e}")

    return maclar

# Çalıştır
veriler = nihai_esnek_cekici()

if veriler:
    df = pd.DataFrame(veriler)
    # Tarih sıralaması
    df['sort'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values('sort').drop('sort', axis=1)
    
    # Excel'e yaz
    df.to_excel("maclarim.xlsx", index=False)
    print(f"İŞLEM TAMAM! {len(df)} maç Excel'e kaydedildi.")
else:
    print("Hala maç bulunamadı. Lütfen sistem tarihini kontrol edin.")
