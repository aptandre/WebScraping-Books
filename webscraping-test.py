import requests
import bs4
import pandas as pd
from time import sleep

# Necessário porque se não a amazon nega meu bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
}

livros_dict = {
    'autores':[],
    'titulo': [],
    'preco': [],
    }

for i in range(50):
    sleep(2)
    print(f"Pág. {i + 1}")
    # Parte que faz a requisição e checa se houve algum erro durante a execução
    try:
        url = f'https://www.amazon.com.br/s?k=livros&page={i+1}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=361HK08KKEMSF&qid=1677164487&sprefix=livro%2Caps%2C300&ref=sr_pg_{i+1}'
        request = requests.get(url, headers=headers)
        request.raise_for_status()
        soup = bs4.BeautifulSoup(request.content, 'html.parser')
    except Exception as e:
        print(str(e))
        pass

    # Aqui eu pego todos os elementos de livros no html
    livros = soup.find_all('div', class_="a-section a-spacing-base")
    for livro in livros:
        autores = f"Autor(es): {livro.find('div', class_='a-row a-size-base a-color-secondary').get_text()}"
        titulo = f" Título: {livro.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()}"
        # Necessário pois alguns títulos não possuem preço, mas estão disponíveis no kindle unlimited
        try:
            preco = f" Preço: R$ {livro.find('span', class_='a-price-whole').get_text()}"
        except:
            preco = f" Título adquirível por assinatura"
        
        livros_dict['autores'].append(autores)
        livros_dict['titulo'].append(titulo)
        livros_dict['preco'].append(preco)

# Cria um dataframe e salva em csv
dataframe = pd.DataFrame(livros_dict)
dataframe.to_csv('./precos_livros.csv', encoding='utf-8', sep=';')

