import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def gercek_fikstur_cek():
    # Botun gerçek bir kullanıcı gibi görünmesi için kimlik bilgisi
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124'}
    
    maclar = []
    # Dünya genelinde güvenilir bir fikstür kaynağı (Örn: FBRef veya benzeri veri tabanları)
    # Burada 5 büyük ligin toplu fikstürünü sunan bir yapı kullanıyoruz.
    url = "https://www.skysports.com/football-fixtures"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sayfadaki her bir maç bloğunu buluyoruz
        for block in soup.find_all('div', class_='fixres__item'):
            lig_ham = block.find_previous('h5', class_='fixres__header2')
            lig_adi = lig_ham.text.strip() if lig_ham else "Diğer"
            
            # Sadece senin istediğin 5 ligi filtrele
            if any(l in lig_adi for l in ["Premier League", "Serie A", "Bundesliga", "La Liga", "Süper Lig"]):
                ev_sahibi = block.find('span', class_='matches__participant--side1').text.strip()
                deplasman = block.find('span', class_='matches__participant--side2').text.strip()
                saat = block.find('span', class_='matches__date').text.strip()
                
                # Tarihi o günün tarihi olarak alıyoruz (SkySports günlük liste sunar)
                tarih = datetime.now().strftime("%d.%m.%Y")
                
                maclar.append({
                    "Lig": lig_adi,
                    "Maç Tarihi": f"{tarih} {saat}",
                    "Ev Sahibi": ev_sahibi,
                    "Deplasman": deplasman
                })
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return maclar

# Verileri çek ve Excel'e yaz
veriler = gercek_fikstur_cek()
if veriler:
    df = pd.DataFrame(veriler)
    df.to_excel("maclarim.xlsx", index=False)
    print("Gerçek verilerle Excel güncellendi!")
else:
    print("Maç bulunamadı, liste boş.")
