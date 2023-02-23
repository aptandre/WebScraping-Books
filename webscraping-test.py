import requests
import bs4
from time import sleep
import pandas as pd

url = 'https://www.amazon.com.br/s?k=livros&page=2&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=361HK08KKEMSF&qid=1677164487&sprefix=livro%2Caps%2C300&ref=sr_pg_1'

# Necessário porque a amazon não aceita requisições sem o user-agent
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "macOS",
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Sec-Fetch-Dest': 'document',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

livros_dict = {'titulo': [], 'preco': []}

for i in range(3):
    print(f"loop {i+1}")
    url = f'https://www.amazon.com.br/s?k=livros&page={i+1}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=361HK08KKEMSF&qid=1677164487&sprefix=livro%2Caps%2C300&ref=sr_pg_{i+1}'
    request = requests.get(url, headers=headers)
    request.raise_for_status()
    soup = bs4.BeautifulSoup(request.content, 'html.parser')


    livros = soup.find_all('div', class_="a-section a-spacing-base")
    # while len(livros) == 0:
    #     print("cheguei aqui bbr")
    #     sleep(0.5)
    #     livros = soup.find_all('div', class_="a-section a-spacing-base")
        
    cont = 1
    for livro in livros:
        print(cont)
        cont += 1
        titulo = f"Título: {livro.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()}"
        print("passou do titulo")
        try:
            preco = f"Preço: R$ {livro.find('span', class_='a-price-whole').get_text()}"
        except:
            pass
        print("passou do preco")
        
        livros_dict['titulo'].append(titulo)
        if preco is None:
            livros_dict['preco'].append("Título disponível por assinatura")
        else:
            livros_dict['preco'].append(preco)

dataframe = pd.DataFrame(livros_dict)
dataframe.to_csv('./precos_livros.csv', encoding='utf-8', sep='|')

