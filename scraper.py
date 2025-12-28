import requests
from bs4 import BeautifulSoup
import datetime

urls = {
    "Ejército": "https://www.argentina.gob.ar/ejercito/noticias",
    "Armada": "https://www.argentina.gob.ar/armada/noticias",
    "Fuerza Aérea": "https://www.argentina.gob.ar/fuerzaaerea/noticias",
    "CAECOPAZ": "https://www.argentina.gob.ar/ejercito/caecopaz"
}

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Noticias FFAA Argentina</title>
    <style>
        body {{ font-family: sans-serif; padding: 20px; background: #f0f2f5; }}
        .contenedor {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a2a3a; text-align: center; }}
        .fuerza {{ border-left: 5px solid #004a80; margin: 20px 0; padding-left: 15px; }}
        a {{ color: #004a80; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>Monitor de Fuerzas Armadas</h1>
        <p style="text-align:center">Última actualización: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
"""

for fuerza, url in urls.items():
    html_content += f"<div class='fuerza'><h2>{fuerza}</h2><ul>"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', class_='panel-default', limit=5)
        for l in links:
            titulo = l.get_text().strip()
            href = "https://www.argentina.gob.ar" + l['href']
            html_content += f"<li><a href='{href}' target='_blank'>{titulo}</a></li>"
    except:
        html_content += "<li>No se pudo obtener noticias hoy.</li>"
    html_content += "</ul></div>"

html_content += "</div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
