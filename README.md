# Tech Challenge - API Embrapa Viticultura 🍇

Este projeto é uma API RESTful em Flask que consulta dados da Embrapa Vitibrasil diretamente dos arquivos CSV online.

Site: http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01

## Endpoints disponíveis
(não possuem subtipos):
- `/producao`
- `/comercializacao`
(possuem subtipos):
- `/processamento?subtipo=viniferas`
- `/importacao?subtipo=vinhos`
- `/exportacao?subtipo=suco`

> As rotas de processamento, importação e exportação **exigem** o parâmetro `subtipo`.

## Estrutura:

```txt
tech_challenge_api/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── embrapa_scraper.py
├── run.py
├── requirements.txt
├── render.yaml
└── README.md
```

## Testar localmente
```bash
pip install -r requirements.txt
python run.py