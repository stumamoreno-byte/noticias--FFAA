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

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archivo Histórico y Actualidad - FF.AA. Argentina</title>
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
        li a {{ display: block; padding: 18px 20px; color: #ccc; text-decoration: none; font-size: 0.9rem; font-weight: 500; }}
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

# Headers más potentes para que no nos bloqueen
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

for fuerza, url in urls.items():
    html_content += f'<div class="card"><div class="card-header"><h2>{fuerza}</h2></div><ul>'
    try:
        time.sleep(1) # Pausa de 1 segundo para no saturar
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # BUSQUEDA ULTRA-AGRESIVA: Buscamos cualquier enlace que esté dentro de un div con clase "views-row", "card", o "panel"
        # O que simplemente sea un link grande con texto largo.
        links_encontrados = []
        
        # Opción 1: Estructura estándar de argentina.gob.ar
        for a in soup.find_all('a', href=True):
            # Filtramos para que el link tenga un título adentro y sea una noticia
            texto = a.get_text(strip=True)
            link_url = a['href']
            
            # Si el link tiene más de 20 caracteres de texto, es probable que sea un título de noticia
            if len(texto) > 25 and "/noticias/" in link_url or "/ejercito/" in link_url or "/armada/" in link_url:
                if link_url not in [l['url'] for l in links_encontrados]:
                    full_link = link_url if link_url.startswith('http') else "https://www.argentina.gob.ar" + link_url
                    links_encontrados.append({'titulo': texto, 'url': full_link})

        if not links_encontrados:
            # Opción 2: Buscar títulos específicos si la anterior falla
            for hf in soup.find_all(['h2', 'h3']):
                parent_a = hf.find_parent('a')
                if parent_a and parent_a.get('href'):
                    texto = hf.get_text(strip=True)
                    link_url = parent_a['href']
                    full_link = link_url if link_url.startswith('http') else "https://www.argentina.gob.ar" + link_url
                    links_encontrados.append({'titulo': texto, 'url': full_link})

        count = 0
        for item in links_encontrados[:6]: # Mostramos los últimos 6
            html_content += f'<li><a href="{item["url"]}" target="_blank">{item["titulo"]}</a></li>'
            count += 1
            
        if count == 0:
            html_content += "<li><a href='#'>Servidor en mantenimiento. Intente refrescar en unos minutos.</a></li>"
            
    except Exception as e:
        html_content += f"<li><a href='#'>Error de conexión.</a></li>"
    
    html_content += "</ul></div>"

html_content += "</div><div class='footer'>ACCESO A INFORMACIÓN PÚBLICA - REPÚBLICA ARGENTINA</div></div></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
