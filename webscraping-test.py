import requests
import bs4
import re
import pandas as pd

url = 'https://www.amazon.com.br/s?k=livros&page=2&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=361HK08KKEMSF&qid=1677164487&sprefix=livro%2Caps%2C300&ref=sr_pg_1'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

request = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(request.content, 'html.parser')

livros_dict = {'titulo': [], 'preco': []}

livros = soup.find_all('div', class_="a-section a-spacing-base")
for livro in livros:
    titulo = livro.find('span', class_="a-size-base-plus a-color-base a-text-normal").get_text()
    preco = f"R$ {livro.find('span', class_='a-price-whole').get_text()}"
    
    livros_dict['titulo'].append(titulo)
    livros_dict['preco'].append(preco)

dataframe = pd.DataFrame(livros_dict)
dataframe.to_csv('./precos_livros.csv', encoding='utf-8', sep=';')

