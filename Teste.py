import requests
from bs4 import BeautifulSoup
import textwrap
import sqlite3

url = 'https://pt.wikihow.com/Se-Tornar-um-Programador'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

resposta = requests.get(url, headers=headers)

print(f"Codigo de status: {resposta.status_code}")

if resposta.status_code != 200:
    print("Trecho HTML recebido (erro): ")
    print(resposta.text[:500])
    
elif resposta.status_code == 200:
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    
    #EXTRATOR DE TITULOS
    titulo_passos = sopa.find_all('b', class_='whb')
    titulo_passos_tratado = []
    buffer = ""

    for passo in titulo_passos:
        for sup in passo.find_all('sup'):
            sup.decompose()

        texto = passo.get_text().strip()

        if not texto:
            continue

        if not texto[0].isupper() and buffer:
            buffer += " " + texto
        else:
            if buffer:
                titulo_passos_tratado.append(buffer)
            buffer = texto
    if buffer:
        titulo_passos_tratado.append(buffer)

    #EXTRATOR DE CATEGORIAS



    #EXTRATOR DE CONTAINER
    container_passo = sopa.find('div', class_= "section steps steps_first sticky")
    categoria_passo = container_passo.find('span', class_="mw-headline").get_text()
    conteudo_passo = container_passo.find_all('div', class_="step")

    #gerador de documento
    c = int(1)
    with open('Texto_Teste.txt', 'w', encoding='utf-8') as arquivo:

        #TITULOS
        for titulo in titulo_passos_tratado:
            arquivo.write(f"{c} - {titulo}\n")
            c+=1

        #CATEGORIAS

        #CONTAINER
        c = 1
        arquivo.write(f"\n\n{categoria_passo}\n")
        for conteudo in conteudo_passo:
            passos = conteudo.get_text().strip()
            passos = passos.replace(' ', '\n -')
            arquivo.write(f"\npasso: {c}")
            arquivo.write(f"\n{textwrap.fill(passos,width=100)}")
            #arquivo.write(f"\n{passos}")
            c+=1
            arquivo.write("\n=======================================================")



else:
    print(f"Falha ao acessar. Codigo: {resposta.status_code}")

