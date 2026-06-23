import requests
from bs4 import BeautifulSoup

url = 'https://pt.wikihow.com/Tornar-se-um-Programador'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

resposta = requests.get(url, headers=headers)

if resposta.status_code == 200:
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    
    elemento_titulo = sopa.find('h1', class_='section-title')
    
    if elemento_titulo:
        titulo = elemento_titulo.text
    else:
        titulo = "Título não encontrado"
        
    print(f"Título extraído: {titulo}")

else:
    print(f"Falha ao acessar. Código: {resposta.status_code}")