import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin  




def LerArquivo():
    with open('seeds.txt', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

listaPages = {}
ler = LerArquivo()
for link in ler.splitlines():
    page = urllib.request.urlopen(link)
    html = str(page.read().decode('utf-8'))
    soup = BeautifulSoup(html, 'lxml')
    Titulo = soup.title.string
    imagem = []
    for img in soup.find_all('img'):
        src = img.attrs.get("src")
        if src:
            url_completa = urljoin(link, src)
            imagem.append(url_completa)

    listaPages[Titulo] = imagem

html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Galeria de Imagens</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
        .card { background: white; margin-bottom: 20px; padding: 15px; border-radius: 8px; shadow: 0 2px 5px rgba(0,0,0,0.1); }
        img { max-width: 200px; display: inline-block; margin: 10px; border: 1px solid #ddd; border-radius: 4px; }
        h2 { color: #333; border-bottom: 2px solid #eee; }
    </style>
</head>
<body>
    <h1>Resultados do Scraping</h1>
"""

for titulo, imagens in listaPages.items():
    titulo_limpo = titulo.strip()
    html_template += f"<div class='card'>\n<h2>{titulo_limpo}</h2>\n"
    
    if not imagens or imagens == [None]:
        html_template += "<p>Nenhuma imagem encontrada.</p>"
    else:
        for img_url in imagens:
            if img_url:
                html_template += f'<img src="{img_url}" alt="Imagem de {titulo_limpo}" onerror="this.style.display=\'none\'">\n'
    
    html_template += "</div>\n"

html_template += "</body>\n</html>"

with open("resultado.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Arquivo 'resultado.html' gerado com sucesso!")

