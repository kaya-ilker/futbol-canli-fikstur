import pandas as pd
from datetime import datetime, timedelta
import requests

def veri_getir():
    # Bu sefer doğrudan güvenilir bir spor verisi sağlayıcısının (GitHub üzerinde barındırılan) 
    # açık kaynaklı fikstür setlerini kullanıyoruz.
    lig_linkleri = {
        "Premier League": "https://raw.githubusercontent.com/openfootball/england/master/2020s/2025-26/1-premierleague.txt",
        "Bundesliga": "https://raw.githubusercontent.com/openfootball/deutschland/master/2020s/2025-26/1-bundesliga.txt"
    }

    maclar = []
    bugun = datetime.now()
    bir_ay_sonra = bugun + timedelta(days=30)

    print("Güvenilir açık kaynak veri setlerine bağlanılıyor...")

    # Not: JSON yerine daha stabil olan 'openfootball' metin tabanlı veriyi parse ediyoruz
    # Bu yöntem bot engellerine takılmaz.
    for lig_adi, url in lig_linkleri.items():
        try:
            r = requests.get(url)
            satirlar = r.text.split('\n')
            
            for satir in satirlar:
                # Satırda maç verisi olup olmadığını kontrol et (Örn: [Sat 18 Apr])
                if '[' in satir and ']' in satir and '-' in satir:
                    parcalar = satir.split('  ')
                    parcalar = [p.strip() for p in parcalar if p.strip()]
                    
                    if len(parcalar) >= 3:
                        ev_dep = parcalar[2].split(' - ')
                        if len(ev_dep) == 2:
                            maclar.append({
                                "Lig": lig_adi,
                                "Maç Tarihi": parcalar[1], # Tarih metni
                                "Ev Sahibi": ev_dep[0],
                                "Deplasman": ev_dep[1]
                            })
        except Exception as e:
            print(f"{lig_adi} okunurken hata: {e}")

    return maclar

# İşlemi başlat
sonuc = veri_getir()

if sonuc:
    df = pd.DataFrame(sonuc)
    # Sadece istediğin 4 sütun
    df = df[["Lig", "Maç Tarihi", "Ev Sahibi", "Deplasman"]]
    df.to_excel("maclarim.xlsx", index=False)
    print(f"Bitti! {len(df)} maç Excel'e yazıldı.")
else:
    # Eğer o an veri çekilemezse Excel'in bozulmaması için yedek plan
    print("Veri çekilemedi. Kaynak güncelleniyor olabilir.")
