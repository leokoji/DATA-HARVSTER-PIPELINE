import requests
from bs4 import BeautifulSoup
import textwrap
import sqlite3

conn = sqlite3.connect("wikihow.db")
conn.execute("CREATE TABLE IF NOT EXISTS artigos (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, titulo TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS secoes (id INTEGER PRIMARY KEY AUTOINCREMENT, artigo_id INTEGER, nome TEXT, FOREIGN KEY (artigo_id) REFERENCES artigos(id))")
conn.execute("CREATE TABLE IF NOT EXISTS passos (id INTEGER PRIMARY KEY AUTOINCREMENT, secao_id INTEGER, numero INTEGER, titulo TEXT, descricao TEXT, FOREIGN KEY (secao_id) REFERENCES secoes(id))")



url = 'https://pt.wikihow.com/Se-Tornar-um-Programador'

conn.execute("INSERT INTO artigos (url, titulo) VALUES (?,?)", ("https://pt.wikihow.com/Se-Tornar-um-Programador", "Como se tornar um programador"))
artigo_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]


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

    #gerador de documento
    c = int(1)
    with open('Texto_Teste.txt', 'w', encoding='utf-8') as arquivo:

        #ESCRIÇÃO DA CATEOGORIA PASSO
        container_passo = sopa.find('div', class_= "section steps steps_first sticky")
        conteudo_passo = container_passo.find_all('div', class_="step")
        c = 1

        arquivo.write(f"\n\npassos\n")
        
        conn.execute("INSERT INTO secoes (artigo_id, nome) VALUES (?,?)", (artigo_id, "Passos"))
        secao_id = conn.execute("SELECT last_insert_rowid()",).fetchone()[0]
        
        for conteudo in conteudo_passo:
                titulo_passo = container_passo.find('b', class_="whb").get_text().strip()
                titulo_tag = conteudo.find("b", class_="whb")
                if titulo_tag:
                    titulo_tag.decompose()
                passos = conteudo.get_text().strip()
                arquivo.write(f"\npasso: {c} - {titulo_passo}")
                arquivo.write(f"\n{textwrap.fill(passos,width=100)}")
                arquivo.write("\n=======================================================")

                #BANCO DADOS DA CATEGORIA PASSOS
           

                conn.execute("INSERT INTO passos (secao_id, numero, titulo, descricao) VALUES (?,?,?,?)", (secao_id, c, titulo_passo, passos))
                
                

                c+=1
        #ESCRIÇÃO DA CATEGORIA METODO
        container_metodo = sopa.find_all("div", class_ = "section steps sticky")

        for metodo in container_metodo:
            categoria_metodo = metodo.find("div", class_ = "altblock").get_text().strip()
            conteudo_metodo = metodo.find_all("div", class_ = "step")
            c = 1

            arquivo.write(f"\n\n{categoria_metodo}\n")

            #BANCO DE DADOS METODO TITULO
            conn.execute("INSERT INTO secoes (artigo_id, nome) VALUES (?,?)", (artigo_id, categoria_metodo))
            secao_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            for conteudo in conteudo_metodo:
                tagTitulo_metodo = conteudo.find_all("b", class_ = "whb")
                titulo_metodo = ""

                for parte in tagTitulo_metodo:
                    titulo_metodo += parte.get_text().strip() + " "
                titulo_metodo = titulo_metodo.strip()

                for tag in tagTitulo_metodo:
                    titulo_tag.decompose()

                passos = conteudo.get_text().strip()

                for palavra in titulo_metodo.split():
                    if passos.startswith(palavra):
                        passos = passos[len(palavra):].strip()
                    else:
                        break

                arquivo.write(f"\npasso {c} - {titulo_metodo}")
                arquivo.write(f"\n{passos}")
                arquivo.write("\n\n======================================================\n\n")

                #BANCO DE DADOS METODOS
                
                

                conn.execute("INSERT INTO passos (secao_id, numero, titulo, descricao) VALUES (?,?,?,?)", (secao_id, c, titulo_metodo, passos))

                c+=1

        conn.commit()
        conn.close()

else:
    print(f"Falha ao acessar. Codigo: {resposta.status_code}")
