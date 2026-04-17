import requests
import pandas as pd
from datetime import datetime, timedelta

def esnek_veri_cek():
    # En stabil 4 lig kaynağı (JSON)
    kanallar = {
        "Premier League": "https://fixturedownload.com/feed/json/epl-2025",
        "La Liga": "https://fixturedownload.com/feed/json/la-liga-2025",
        "Serie A": "https://fixturedownload.com/feed/json/serie-a-2025",
        "Bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025"
    }
    
    maclar = []
    bugun = datetime.now()
    otuz_gun_sonra = bugun + timedelta(days=30)
    
    print("Veri kanalları esnek modda taranıyor...")

    for lig_adi, url in kanallar.items():
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for m in data:
                    # ANAHTAR KONTROLÜ: 'Date' veya 'date' hangisi varsa onu al
                    ham_tarih = m.get('Date') or m.get('date')
                    ev_sahibi = m.get('HomeTeam') or m.get('homeTeam')
                    deplasman = m.get('AwayTeam') or m.get('awayTeam')
                    
                    if ham_tarih and ev_sahibi:
                        # Tarih formatını temizle (Z harfini ve milisaniyeleri at)
                        tarih_temiz = ham_tarih.replace('Z', '').split('.')[0]
                        try:
                            t_obj = datetime.fromisoformat(tarih_temiz)
                            
                            # Sadece önümüzdeki 30 gün
                            if bugun <= t_obj <= otuz_gun_sonra:
                                maclar.append({
                                    "Lig": lig_adi,
                                    "Maç Tarihi": t_obj.strftime("%d.%m.%Y %H:%M"),
                                    "Ev Sahibi": ev_sahibi,
                                    "Deplasman": deplasman
                                })
                        except:
                            continue # Tarih formatı uymazsa pas geç
                print(f"{lig_adi} başarıyla tarandı.")
        except Exception as e:
            print(f"{lig_adi} kanalında sorun: {e}")

    return maclar

# Çalıştır
liste = esnek_veri_cek()

if liste:
    df = pd.DataFrame(liste)
    # Tarihe göre sırala
    df['sort'] = pd.to_datetime(df['Maç Tarihi'], format='%d.%m.%Y %H:%M')
    df = df.sort_values('sort').drop('sort', axis=1)
    
    df.to_excel("maclarim.xlsx", index=False)
    print(f"TEBRİKLER! {len(df)} maç bulundu ve Excel güncellendi.")
else:
    print("DİKKAT: Hiç maç bulunamadı. Kaynaklar geçici olarak kapalı olabilir.")
