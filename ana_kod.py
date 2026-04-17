import requests
import pandas as pd
import os

# GitHub Secrets'tan anahtarı alıyoruz
api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
}

# Bugünün futbol maçlarını getiren sorgu (Sadece Futbol için 'football')
url = "https://sportapi7.p.rapidapi.com/api/v1/sport/football/events/live"

try:
    r = requests.get(url, headers=headers)
    data = r.json()
    
    maclar = []
    # SportAPI verileri genellikle 'events' listesi altında sunar
    if 'events' in data:
        for m in data['events']:
            maclar.append({
                "Lig": m.get('tournament', {}).get('name', 'Bilinmiyor'),
                "Dakika": m.get('status', {}).get('description', '-'),
                "Ev Sahibi": m.get('homeTeam', {}).get('name', '-'),
                "Deplasman": m.get('awayTeam', {}).get('name', '-'),
                "Skor": f"{m.get('homeScore', {}).get('current', 0)} - {m.get('awayScore', {}).get('current', 0)}"
            })
    
    if not maclar:
        maclar = [{"Lig": "Canlı Maç Yok", "Dakika": "Şu an canlı maç bulunamadı", "Ev Sahibi": "-", "Deplasman": "-", "Skor": "-"}]

except Exception as e:
    maclar = [{"Lig": "Bağlantı Hatası", "Dakika": str(e), "Ev Sahibi": "-", "Deplasman": "-", "Skor": "-"}]

# Excel dosyasını oluştur
df = pd.DataFrame(maclar)
df.to_excel("maclarim.xlsx", index=False)
print("Excel başarıyla güncellendi!")
