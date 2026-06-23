import requests
from bs4 import BeautifulSoup

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

    with open ("html_real.txt", "w", encoding="utf-8") as debug_file:
        debug_file.write(resposta.text)
    
    elemento_titulo = sopa.find('h1', class_='title_md')
    
    if elemento_titulo:
        titulo = elemento_titulo.text
    else:
        titulo = "Título não encontrado"
        
    print(f"Título extraído: {titulo}")

    corpo = sopa.find('div', {'class': 'mf-section-0'})
    texto_resumo = corpo.get_text(separator=' ', strip=True) if corpo else ""

    container_passos = sopa.find('div', id='step-id-00')

    texto_passos = ''

    if container_passos:
        paragrafos = container_passos.find_all('p')

        for p in paragrafos:
            texto_passos += p.text.strip() + "\n"
    
    else:
        print("AVISO: Container de passos não encontrada.")
    
    texto_final = f"{titulo} \n\n{texto_resumo}\n\n{texto_passos}"

    with open('Texto_Extraido.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto_final)

    print("Extração e salvamento Concluidos com sucesso!")

else:
    print(f"Falha ao acessar. Codigo: {resposta.status_code}")