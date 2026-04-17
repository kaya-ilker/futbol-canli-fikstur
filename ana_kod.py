import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fikstur_kaziyi_baslat():
    # Tarayıcı gibi görünmek için başlık bilgisi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Sky Sports'un genel fikstür sayfası
    url = "https://www.skysports.com/football-fixtures"
    
    maclar = []
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Sayfadaki tüm maç bloklarını buluyoruz
        for lig_blogu in soup.find_all('div', class_='fixres__item'):
            # Lig ismini bulmak için bir üstteki başlığa bakıyoruz
            lig_basligi = lig_blogu.find_previous('h5', class_='fixres__header2')
            lig_adi = lig_basligi.text.strip() if lig_basligi else "Bilinmiyor"
            
            # Sadece senin istediğin 5 ligi içerenleri alalım
            if any(l in lig_adi for l in ["Premier League", "Serie A", "Bundesliga", "La Liga", "Süper Lig"]):
                
                ev_sahibi = lig_blogu.find('span', class_='matches__participant--side1').text.strip()
                deplasman = lig_blogu.find('span', class_='matches__participant--side2').text.strip()
                saat = lig_blogu.find('span', class_='matches__date').text.strip()
                
                # Tarih bilgisi Sky Sports'ta genellikle üst başlıkta yer alır
                tarih_blogu = lig_blogu.find_previous('h4', class_='fixres__header1')
                tarih_metni = tarih_blogu.text.strip() if tarih_blogu else datetime.now().strftime("%d.%m.%Y")
                
                maclar.append({
                    "Lig": lig_adi,
                    "Maç Tarihi": f"{tarih_metni} {saat}",
                    "Ev Sahibi": ev_sahibi,
                    "Deplasman": deplasman
                })
    except Exception as e:
        print(f"Hata: {e}")
        
    return maclar

# Veriyi çek ve Excel'e dök
liste = fikstur_kaziyi_baslat()
if liste:
    df = pd.DataFrame(liste)
    # Sütunları düzenle
    df = df[["Lig", "Maç Tarihi", "Ev Sahibi", "Deplasman"]]
    df.to_excel("maclarim.xlsx", index=False)
    print("Gerçek fikstür verileri Excel'e başarıyla yazıldı!")
else:
    print("Eşleşen maç bulunamadı.")
