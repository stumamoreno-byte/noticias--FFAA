import requests
from bs4 import BeautifulSoup
import datetime

# Diccionario de fuentes con sus URLs específicas
urls = {
    "Ejército Argentino": "https://www.argentina.gob.ar/ejercito/noticias",
    "Armada Argentina": "https://www.argentina.gob.ar/armada/noticias",
    "Fuerza Aérea": "https://www.argentina.gob.ar/fuerzaaerea/noticias",
    "CAECOPAZ": "https://www.argentina.gob.ar/ejercito/caecopaz"
}

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor FFAA Argentina</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; padding: 20px; background-color: #f4f4f4; color: #333; }}
        .container {{ max-width: 900px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #1a2a3a; border-bottom: 3px solid #004a80; padding-bottom: 10px; }}
        .fuerza-seccion {{ margin-bottom: 30px; border-left: 6px solid #004a80; padding-left: 20px; }}
        h2 {{ color: #004a80; text-transform: uppercase; font-size: 1.4rem; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 12px; background: #f9f9f9; padding: 10px; border-radius: 4px; transition: 0.3s; }}
        li:hover {{ background: #f0f7ff; transform: translateX(5px); }}
        a {{ text-decoration: none; color: #333; font-weight: 600; display: block; }}
        .fecha {{ font-size: 0.9rem; color: #666; text-align: center; margin-bottom: 20px; }}
        .no-news {{ color: #999; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Actualidad de las Fuerzas Armadas</h1>
        <p class="fecha">Actualizado el: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} (Hora Local)</p>
"""

headers = {'User-Agent': 'Mozilla/5.0'}

for fuerza, url in urls.items():
    html_content += f"<div class='fuerza-seccion'><h2>{fuerza}</h2><ul>"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Intentamos buscar noticias en diferentes formatos posibles del sitio argentina.gob.ar
        items = soup.find_all('a', class_='panel-default') or \
                soup.find_all('a', class_='card') or \
                soup.select('.views-row a')

        encontradas = 0
        for item in items:
            if encontradas >= 5: break
            
            titulo_tag = item.find('h2') or item.find('h3') or item.find('h4') or item.find('div', class_='h3')
            if titulo_tag:
                titulo = titulo_tag.get_text(strip=True)
                href = item['href']
                link = href if href.startswith('http') else "https://www.argentina.gob.ar" + href
                
                html_content += f"<li><a href='{link}' target='_blank'>{titulo}</a></li>"
                encontradas += 1
        
        if encontradas == 0:
            html_content += "<li class='no-news'>No se encontraron noticias recientes en esta sección.</li>"
            
    except Exception as e:
        html_content += f"<li class='no-news'>Error al conectar con la fuente.</li>"
    
    html_content += "</ul></div>"

html_content += """
        <p style="text-align:center; font-size: 0.8rem; color: #aaa; margin-top: 40px;">Sistema Automático de Monitoreo - stumamoreno-byte</p>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
