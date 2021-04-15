from bs4 import BeautifulSoup
import requests
import json
import csv
import re
import os


class CSVRepo:
    def __init__(self, name: str):
        if not os.path.exists('csv'):
            os.mkdir('csv')

        self.name = name
        self.f = open(f'csv/{name}.csv', 'w')
        self.writer = csv.DictWriter(self.f, quoting=csv.QUOTE_NONNUMERIC, delimiter=';', quotechar='"', fieldnames=[
            "Nome", 
            "Nota",
            "Imagem",
            "Valor"
        ])

        self.writer.writeheader()


    def save(self, data: dict):
        self.writer.writerow({
            "Nome": data['name'],
            "Nota": data['aggregateRating']['ratingValue'] if 'aggregateRating' in data else '---',
            'Imagem': data['image'],
            'Valor': data['offers']['lowPrice'] if "offers" in data else -1
        })


    def close_file(self):
        self.f.close()


class Crawler:
    def request_america(self, url: str, name: str):
        self.name = name

        result = requests.get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': 'www.americanas.com.br',
            'Refer': 'https://www.americanas.com.br/busca/fantasia-de-sereia-infantil?chave_search=acterm',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            "Cookie": '_dd_s=rum=1&id=e8c1e4dd-3111-4f39-bf9f-4fc8c4a4ab10&created=1618442326560&expire=1618443999963; _ga=GA1.3.775499586.1618442327; _gid=GA1.3.1983627728.1618442327; s_cc=true; _hjIncludedInSessionSample=0; _gat_UA-97626372-1=1; b2wChannel=ACOM; bm_sv=205565451BF34A09DC86E14E119F4C68~ZOXxCPYno4tPPHSOY+iwz5bvsKWBq121GCm4wX73Fjvr4OuZ/jGh4nKp4/QTIxIYz5JC0X+x9+5OT38tkba4DQHjxfoLUpGA/sLj41KuASNDXE2xlRtkoCq4vKNsoOl93FjRgHx+4hgQ/GI9KQxDXYFV4HSg1fnb1BHCDyzy5a4=; cto_bundle=skQopl9BVFVOVGlROUZTSHFQQ2xVWElxNlp3UWRoSU1PRldmMlRSVXduRTYwaXVsODA4dkNBVERKd2RLNnNZOFAzQ1BvRiUyRmczaWJlJTJCVFFQa0FsWTNVb0hJeGlnTTVuajgzdTdYQW5CbFR6RGFDejlvOVAybDBKdXdNZW9qdDJlWm8lMkZ1R3c1cVNVdXFuckZ5SFhXJTJCJTJCaVZKWmRUVnM1UTBaQUJLS3JrdERwbW8wZnRVJTNE; s_sq=%5B%5BB%5D%5D; feather.rank=%7B%22search%22%3A%22aquario%20para%20tartaruga%E2%86%871%E2%86%88fantasia%20de%20sereia%20infantil%E2%86%871%E2%86%88fantasia%20homem%20aranha%E2%86%871%22%7D; AMCV_14B422CE52782FA90A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C18732%7CMCMID%7C40656804690396441841122350017919819663%7CMCAAMLH-1619047127%7C4%7CMCAAMB-1619047127%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1618449530s%7CNONE%7CMCSYNCSOP%7C411-18739%7CMCAID%7CNONE%7CvVersion%7C5.2.0; _gcl_au=1.1.1094308167.1618442329; _hjAbsoluteSessionInProgress=0; _hjTLDTest=1; _hjid=5eaa0783-be3f-4c79-8a3d-9b353942991d; AMCVS_14B422CE52782FA90A490D4D%40AdobeOrg=1; B2W-SID=987.4575020572972021143201873; B2W-UID=va_2021143201847_319.7915348472531; __gads=ID=159190ffc486ec80-22051bedb2b900d0:T=1618442327:RT=1618442327:S=ALNI_MZ1usK9uM0eChSpg1EZ_VCOcuISQQ; ak_bmsc=E7F02D77C08562FE21FC7E9A570ECA396858CD1FD4190000567877602BA08048~plMipENQBfOXLCUWyFkLMzPq5zUICd8zzpl5ERze9JZVvzomoFi/VG3b1IP6/FsgbEwetYtL1qLS7QpKdYiJWZUNB/yq641q+FciNqNVcDf1G94e2DQ/2N6JuofqeywW57v8cAZgge9gRly5B1US0H/dmNLDOVuyoJ8/9UvjJXoFg1awKo3Sw71OejRo6jAPDoqwuedKeCQRKo7LsAfFCNz2szlTGdlpLtmrVvFHiYeYyB8vKAtarWPo4mfVETMNyI; B2W-IU=false; B2W-PID=1618442326538.0.47727892053505516; MobileOptOut=1; b2wDevice=eyJvcyI6Ik1hYyBPUyBYIiwib3NWZXJzaW9uIjoiMTAuMTUiLCJ2ZW5kb3IiOiJBcHBsZSIsInR5cGUiOiJkZXNrdG9wIiwibWt0TmFtZSI6IiIsIm1vZGVsIjoiU2FmYXJpIiwibW9iaWxlT3B0T3V0IjoiZmFsc2UifQ==; b2wDeviceType=desktop; searchTestAB=old'
        })

        self.parse_data(result.content)


    def parse_data(self, result: str):
        bs = BeautifulSoup(result, features='html.parser')
        products = str(bs.select('div.src__Wrapper-sc-1uorjk3-0.fEPVJM script')[0])
        tags = re.compile('<.*?>')
        
        js = json.loads(re.sub(tags, '', products).encode())
        self.save_data(js["@graph"][4]['itemListElement'])


    def save_data(self, data: dict):
        cs = CSVRepo(self.name)

        for i in data:
            cs.save(i)

        cs.close_file()
        

if __name__ == "__main__":
    cr = Crawler()

    while True:
        subject = input("Digite um termo para pesquisar na americanas: \n>>> ")
        filename = input("Digite o nome do arquivo csv a ser gerado (sem o .csv): \n>>> ")

        cr.request_america(f"https://www.americanas.com.br/busca/{subject.lower().replace(' ', '-')}?chave_search=acterm", filename)

        s = input("\nDigite 's' para pesquisar mais um item ou qualquer outro para sair: \n>>> ")

        if s.lower() != 's':
            break