# Tech Challenge - API Embrapa Viticultura 🍇

Este projeto é uma API RESTful em Flask que consulta dados da Embrapa Vitibrasil diretamente dos arquivos CSV online.

Site: http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01

API: https://embrapa-api-alq8.onrender.com/

## Endpoints disponíveis
(não possuem subtipos):
- `/producao`
- `/comercializacao`
  
(possuem subtipos):
- `**Processamento** possui os subtipos: [viniferas, americanas, mesa e semclass].            Exemplo:  /processamento/viniferas`
- `**Importacao** possui os subtipos: [vinhos, espumantes, frescas, passas e suco]            Exemplo:  /importacao/vinhos`
- `**Exportacao** possui os subtipos: [vinho, espumantes, uva e suco]                         Exemplo:  /exportacao/suco`

(documentação - SWAGGER):
- `/apidocs`

> As rotas de processamento, importação e exportação **exigem** o parâmetro `subtipo`.

## Estrutura:

```txt
tech_challenge_api/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── embrapa_scraper.py
│   └── templates/
│       └── tabela.html
├── static/
│   ├── styles.css
│   ├── malha.js
│   └── imagens/
│       └── FIAP_logo.png
├── run.py
├── requirements.txt
├── render.yaml
└── README.md
```

## Testar localmente
```bash
pip install -r requirements.txt
python run.py
