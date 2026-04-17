import requests
import pandas as pd
import os

# GitHub Secrets'tan anahtarı alıyoruz
api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# Bugünün tüm futbol etkinliklerini getiren sorgu
url = "https://sportapi7.p.rapidapi.com/api/v1/sport/football/events/live"

try:
    r = requests.get(url, headers=headers)
    data = r.json()
    
    maclar = []
    if 'events' in data:
        for m in data['events']:
            # Verileri senin istediğin başlıklarla topluyoruz
            maclar.append({
                "Lig": m.get('tournament', {}).get('name', 'Diğer'),
                "Tarih": m.get('status', {}).get('description', 'Belirsiz'), # Canlıysa dakika, değilse durum yazar
                "Ev Sahibi": m.get('homeTeam', {}).get('name', '-'),
                "Deplasman": m.get('awayTeam', {}).get('name', '-'),
                "Skor": f"{m.get('homeScore', {}).get('current', 0)} - {m.get('awayScore', {}).get('current', 0)}"
            })
    
    if not maclar:
        maclar = [{"Lig": "Maç Bulunamadı", "Tarih": "-", "Ev Sahibi": "Şu an aktif maç yok", "Deplasman": "-", "Skor": "-"}]

except Exception as e:
    maclar = [{"Lig": "Hata", "Tarih": "-", "Ev Sahibi": f"Bağlantı Sorunu: {str(e)}", "Deplasman": "-", "Skor": "-"}]

# Excel dosyasını tam istediğin formatta oluşturuyoruz
df = pd.DataFrame(maclar)
# Sütun sırasını belirleyelim
df = df[["Lig", "Tarih", "Ev Sahibi", "Deplasman", "Skor"]]

df.to_excel("maclarim.xlsx", index=False)
print("İstediğin formatta Excel başarıyla oluşturuldu!")
