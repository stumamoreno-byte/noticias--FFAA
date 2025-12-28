import requests
from bs4 import BeautifulSoup
import datetime
import time
import random

# URLs oficiales
urls = {
    "Estado Mayor Conjunto": "https://www.argentina.gob.ar/estado-mayor-conjunto-de-las-fuerzas-armadas/noticias",
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
    <title>Archivo Histórico FF.AA.</title>
    <style>
        :root {{ --primario: #0b131a; --secundario: #1c2e3e; --acento: #daa520; --fondo: #121212; --tarjeta: #1e1e1e; --texto: #e0e0e0; }}
        body {{ font-family: 'Segoe UI', sans-serif; background-color: var(--fondo); margin: 0; color: var(--texto); }}
        header {{ background: linear-gradient(180deg, var(--primario) 0%, #000 100%); padding: 50px 20px; text-align: center; border-bottom: 2px solid var(--acento); }}
        .container {{ max-width: 1200px; margin: -20px auto 50px; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
        .card {{ background: var(--tarjeta); border-radius: 8px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.5); border: 1px solid #333; }}
        .card-header {{ background: var(--secundario); padding: 15px; border-bottom: 2px solid var(--acento); }}
        h2 {{ margin: 0; font-size: 1.1rem; color: var(--acento); text-transform: uppercase; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ border-bottom: 1px solid #2a2a2a; }}
        li a {{ display: block; padding: 18px 20px; color: #ccc; text-decoration: none; font-size: 0.9rem; font-weight: 500; line-height: 1.4; }}
        li a:hover {{ background: #252525; color: var(--acento); }}
        .footer {{ text-align: center; padding: 40px; color: #555; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <header>
        <h1 style="margin:0;">REPOSITORIO DE NOTICIAS FF.AA.</h1>
        <p style="color: var(--acento);">Historial Completo y Últimas Publicaciones</p>
        <div style="margin-top:15px; font-size: 0.8rem;">Sincronización: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </header>
    <div class="container"><div class="grid">
"""

# Simulamos ser un navegador humano real y moderno
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.google.com/'
}

for fuerza, url in urls.items():
    html_content += f'<div class="card"><div class="card-header"><h2>{fuerza}</h2></div><ul>'
    try:
        # Pausa aleatoria para no parecer un robot (entre 2 y 4 segundos)
        time.sleep(random.uniform(2, 4))
        
        session = requests.Session()
        r = session.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        noticias = []
        
        # Estrategia 1: Buscar en los paneles de Argentina.gob.ar
        for item in soup.find_all(['a'], class_=['panel-default', 'card']):
            titulo = item.get_text(" ", strip=True)
            link = item.get('href', '')
            if len(titulo) > 20 and link:
                full_link = link if link.startswith('http') else "https://www.argentina.gob.ar" + link
                if full_link not in [n['url'] for n in noticias]:
                    noticias.append({'titulo': titulo, 'url': full_link})

        # Estrategia 2: Si la 1 falla, buscar cualquier link con texto largo en áreas de noticias
        if len(noticias) < 2:
            for a in soup.select('div.views-row a, div.item-list a'):
                titulo = a.get_text(" ", strip=True)
                link = a.get('href', '')
                if len(titulo) > 25:
                    full_link = link if link.startswith('http') else "https://www.argentina.gob.ar" + link
                    if full_link not in [n['url'] for n in noticias]:
                        noticias.append({'titulo': titulo, 'url': full_link})

        count = 0
        for n in noticias[:6]:
            html_content += f'<li><a href="{n["url"]}" target="_blank">{n["titulo"]}</a></li>'
            count += 1
            
        if count == 0:
            html_content += "<li><a href='#'>No se detectaron entradas nuevas. Refrescar manualmente.</a></li>"
            
    except Exception:
        html_content += "<li><a href='#'>Fuente protegida temporalmente. Reintentando...</a></li>"
    
    html_content += "</ul></div>"

html_content += "</div><div class='footer'>ACCESO A INFORMACIÓN PÚBLICA - REPÚBLICA ARGENTINA</div></div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
