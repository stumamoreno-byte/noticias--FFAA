import requests
from bs4 import BeautifulSoup
import datetime

# Diccionario de fuentes
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
        :root {{
            --primario: #0b131a;
            --secundario: #1c2e3e;
            --acento: #daa520; /* Dorado militar para resaltar */
            --fondo: #121212;
            --tarjeta: #1e1e1e;
            --texto: #e0e0e0;
        }}
        body {{ 
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            background-color: var(--fondo); 
            margin: 0; padding: 0; color: var(--texto);
        }}
        header {{
            background: linear-gradient(180deg, var(--primario) 0%, #000 100%);
            color: white; padding: 50px 20px; text-align: center;
            border-bottom: 2px solid var(--acento);
        }}
        .container {{ max-width: 1200px; margin: -20px auto 50px; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
        .card {{ 
            background: var(--tarjeta); border-radius: 8px; overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5); border: 1px solid #333;
        }}
        .card-header {{
            background: var(--secundario); padding: 15px;
            border-bottom: 2px solid var(--acento);
        }}
        h2 {{ margin: 0; font-size: 1.1rem; letter-spacing: 1px; color: var(--acento); text-transform: uppercase; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ border-bottom: 1px solid #2a2a2a; transition: 0.2s; }}
        li:hover {{ background: #252525; }}
        li a {{ 
            display: block; padding: 18px 20px; color: #ccc; 
            text-decoration: none; font-size: 0.9rem; font-weight: 500;
        }}
        li a:hover {{ color: var(--acento); }}
        .footer {{ text-align: center; padding: 40px; color: #555; font-size: 0.8rem; }}
        .status {{ font-size: 0.7rem; color: #888; text-transform: uppercase; margin-top: 5px; }}
    </style>
</head>
<body>
    <header>
        <h1 style="margin:0; font-size: 2rem;">REPOSITORIO DE NOTICIAS FF.AA.</h1>
        <p style="color: var(--acento); font-weight: bold;">Historial Completo y Últimas Publicaciones</p>
        <div style="margin-top:15px; font-size: 0.8rem; color: #888;">
            Actualización del sistema: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
        </div>
    </header>

    <div class="container">
        <div class="grid">
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for fuerza, url in urls.items():
    html_content += f"""
            <div class="card">
                <div class="card-header">
                    <h2>{fuerza}</h2>
                    <div class="status">Últimas entradas detectadas</div>
                </div>
                <ul>"""
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Buscamos de forma agresiva cualquier link que parezca una noticia
        # argentina.gob.ar usa mucho 'panel-default' y 'card-title'
        items = soup.select('a.panel-default') or \
                soup.select('.views-row a') or \
                soup.select('.noticia a') or \
                soup.find_all('a', class_='card')

        count = 0
        for item in items:
            if count >= 6: break # Traemos hasta 6 noticias por sección
            
            # Buscamos el texto del título dentro del link o en sus hijos
            titulo_tag = item.find(['h2', 'h3', 'h4', 'div', 'p'])
            titulo = ""
            
            if titulo_tag:
                titulo = titulo_tag.get_text(strip=True)
            else:
                titulo = item.get_text(strip=True)

            # Si el título es muy corto o vacío, lo saltamos
            if len(titulo) < 10: continue

            href = item['href']
            link = href if href.startswith('http') else "https://www.argentina.gob.ar" + href
            
            html_content += f'<li><a href="{link}" target="_blank">{titulo}</a></li>'
            count += 1
        
        if count == 0:
            html_content += "<li><a href='#'>Sin noticias disponibles en el servidor en este momento.</a></li>"
            
    except Exception as e:
        html_content += f"<li><a href='#'>Error de conexión con la fuente oficial.</a></li>"
    
    html_content += "</ul></div>"

html_content += """
        </div>
        <div class="footer">
            SISTEMA AUTOMATIZADO DE SEGUIMIENTO DE DEFENSA NACIONAL<br>
            Acceso a información pública - República Argentina
        </div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
