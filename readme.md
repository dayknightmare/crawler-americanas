# Crawler Americanas


Este é um simples projeto feito em Python que busca um terminado termo no site da [Americanas](https://www.americanas.com.br/) e coleta os dados da primeira página salvando-os num arquivo .csv.

Os dados salvos são:

    - Nome
    - Nota (valor ou '---' caso não tenha)
    - Link da imagem
    - Valor (valor ou -1 caso não tenha)

Para executar instale as dependências usando o comando abaixo:

```bash
pip install -r requirements.txt
```

e logo após execute o aquivo ```main.py```

```bash
python main.py
```