import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fikstur_cek():
    # Bot engellerini aşmak için daha detaylı başlıklar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    # Sky Sports'un fikstür sayfası
    url = "https://www.skysports.com/football-fixtures"
    maclar = []
    
    try:
        print(f"Bağlantı kuruluyor: {url}")
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Maçların olduğu ana gövdeyi bul
        items = soup.find_all('div', class_='fixres__item')
        print(f"Toplam {len(items)} potansiyel maç bulundu. Filtreleme başlıyor...")

        for item in items:
            # Lig adını bul (H5 başlıkları)
            lig_header = item.find_previous('h5', class_='fixres__header2')
            lig_adi = lig_header.text.strip() if lig_header else "Bilinmiyor"
            
            # Senin istediğin 5 ligi kontrol et
            hedef_ligler = ["Premier League", "Serie A", "Bundesliga", "La Liga", "Süper Lig"]
            
            if any(lig in lig_adi for lig in hedef_ligler):
                ev = item.find('span', class_='matches__participant--side1')
                dep = item.find('span', class_='matches__participant--side2')
                saat = item.find('span', class_='matches__date')
                
                if ev and dep:
                    maclar.append({
                        "Lig": lig_adi,
                        "Maç Tarihi": saat.text.strip() if saat else "Belirsiz",
                        "Ev Sahibi": ev.text.strip(),
                        "Deplasman": dep.text.strip()
                    })
        
        print(f"Filtreleme sonrası {len(maclar)} maç listeye eklendi.")

    except Exception as e:
        print(f"Hata detayı: {e}")
        
    return maclar

# Çalıştırma ve Kaydetme
sonuclar = fikstur_cek()

if sonuclar:
    df = pd.DataFrame(sonuclar)
    df.to_excel("maclarim.xlsx", index=False)
    print("Excel dosyası başarıyla güncellendi ve kaydedildi.")
else:
    # Eğer veri bulunamazsa boş dosya gitmesin diye kontrol ekliyoruz
    print("DİKKAT: Hiç maç bulunamadı! Veri kaynağı botu engellemiş olabilir.")
