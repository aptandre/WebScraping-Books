import requests
import bs4
import pandas as pd

# Necessário porque se não a amazon nega meu bot
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
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

for i in range(50):
    print(f"Page {i + 1}")
    # Parte que faz a requisição e checa se houve algum erro durante a execução
    try:
        url = f'https://www.amazon.com.br/s?k=livros&page={i+1}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=361HK08KKEMSF&qid=1677164487&sprefix=livro%2Caps%2C300&ref=sr_pg_{i+1}'
        request = requests.get(url, headers=headers)
        request.raise_for_status()
        soup = bs4.BeautifulSoup(request.content, 'html.parser')
    except Exception as e:
        print(str(e))

    # Aqui eu pego todos os elementos de livros no html
    livros = soup.find_all('div', class_="a-section a-spacing-base")
    for livro in livros:
        titulo = f" Título: {livro.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()}"
        # Necessário pois alguns títulos não possuem preço, mas estão disponíveis no kindle unlimited
        try:
            preco = f" Preço: R$ {livro.find('span', class_='a-price-whole').get_text()}"
        except:
            preco = f" Título adquirível por assinatura"
        
        livros_dict['titulo'].append(titulo)
        livros_dict['preco'].append(preco)

# Cria um dataframe e salva em csv
dataframe = pd.DataFrame(livros_dict)
dataframe.to_csv('./precos_livros.csv', encoding='utf-8', sep=';')

