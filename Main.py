import requests
from bs4 import BeautifulSoup
import textwrap
import sqlite3

url = 'https://pt.wikihow.com/Se-Tornar-um-Programador'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

resposta = requests.get(url, headers=headers)

conn = sqlite3.connect("WikiHow.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS passos_wikihow (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT)")
sql_insert = "INSERT INTO passos_wikihow (texto) VALUES (?)"

print(f"Codigo de status: {resposta.status_code}")

if resposta.status_code != 200:
    print("Trecho HTML recebido (erro): ")
    print(resposta.text[:500])
    
elif resposta.status_code == 200:
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    
    elemento_titulo = sopa.find('h1', class_='title_md')
    titulo = elemento_titulo.get_text() if elemento_titulo else ""
        
    print(f"Título extraído: {titulo}")

    corpo = sopa.find('div', {'class': 'mf-section-0'})
    texto_resumo = corpo.get_text(separator=' ', strip=True) if corpo else ""

    container_passos = sopa.find('div', id = "passos")
    passos_filtrados = container_passos.find_all("div", class_="step")

    texto_passos = ' '
    for i in passos_filtrados:
        texto_parte = i.get_text(separator=' ') if passos_filtrados else " "
        texto_passos += texto_parte

    texto_final = f"{titulo} \n\n{textwrap.fill(texto_resumo, width=80)}\n\n{texto_passos}"

    with open('Texto_Extraido.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto_final)

    for passo in passos_filtrados:
        insert = passo.get_text(separator = ' ') if passos_filtrados else " "
        cursor.execute(sql_insert, (insert,))
        print(f"Salvando no banco: {insert[:50]}...")
    
    conn.commit()
    conn.close()

    print("Extração e salvamento Concluidos com sucesso!")
    print(f"Encontrei {len(passos_filtrados)} passos para salvar.")
    

else:
    print(f"Falha ao acessar. Codigo: {resposta.status_code}")

