import requests
from bs4 import BeautifulSoup
import datetime
import time

# URLs oficiales
urls = {
    "Estado Mayor Conjunto": "https://www.argentina.gob.ar/estado-mayor-conjunto-de-las-fuerzas-armadas/noticias",
    "Ejército Argentino": "https://www.argentina.gob.ar/ejercito/noticias",
    "Armada Argentina": "https://www.argentina.gob.ar/armada/noticias",
    "Fuerza Aérea": "https://www.argentina.gob.ar/fuerzaaerea/noticias",
    "CAECOPAZ": "https://www.argentina.gob.ar/ejercito/caecopaz"
}

# Inicio del HTML con el diseño que ya te gustó
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archivo Histórico FF.AA.</title>
    <style>
        :root {{ --primario: #0b131a; --secundario: #1c2e3e; --acento: #daa520; --fondo: #121212; --tarjeta: #1e1e1e; --texto: #e0e0e0; }}
        body {{ font-family: 'Segoe UI', sans-serif; background-color: var(--fondo); margin: 0; color: var(--texto); }}
        header {{ background: linear-gradient(180deg, var(--primario) 0%, #000 100%); padding: 50px 20px; text-align: center; border-bottom: 2px solid var(--acento); }}
        .container {{ max-width: 1200px; margin: -20px auto 50px; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
        .card {{ background: var(--tarjeta); border-radius: 8px; overflow: hidden; border: 1px solid #333; }}
        .card-header {{ background: var(--secundario); padding: 15px; border-bottom: 2px solid var(--acento); }}
        h2 {{ margin: 0; font-size: 1.1rem; color: var(--acento); text-transform: uppercase; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ border-bottom: 1px solid #2a2a2a; }}
        li a {{ display: block; padding: 18px 20px; color: #ccc; text-decoration: none; font-size: 0.9rem; line-height: 1.4; }}
        .footer {{ text-align: center; padding: 40px; color: #555; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <header>
        <h1 style="margin:0;">REPOSITORIO DE NOTICIAS FF.AA.</h1>
        <p style="color: var(--acento);">Sincronización: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </header>
    <div class="container"><div class="grid">
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'}

for fuerza, url in urls.items():
    html_content += f'<div class="card"><div class="card-header"><h2>{fuerza}</h2></div><ul>'
    try:
        # Intentamos obtener la página
        response = requests.get(url, headers=headers, timeout=30)
        # Forzamos la codificación correcta para evitar errores de tildes
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos todos los links de la página
        links = soup.find_all('a')
        count = 0
        
        for link in links:
            if count >= 6: break
            
            href = link.get('href', '')
            texto = link.get_text(" ", strip=True)
            
            # Filtro inteligente: solo links que parecen noticias (tienen texto largo)
            if len(texto) > 30 and ("/noticias" in href or "argentina.gob.ar" in href):
                full_url = href if href.startswith('http') else "https://www.argentina.gob.ar" + href
                html_content += f'<li><a href="{full_url}" target="_blank">{texto}</a></li>'
                count += 1
        
        if count == 0:
            html_content += "<li><a href='#'>No se hallaron entradas en esta sección.</a></li>"
            
    except Exception as e:
        # Si algo falla, el programa sigue con la siguiente fuerza en lugar de detenerse
        html_content += f"<li><a href='#'>Error al conectar con la fuente oficial.</a></li>"
    
    html_content += "</ul></div>"

html_content += "</div><div class='footer'>MONITOR DE DEFENSA NACIONAL</div></div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
