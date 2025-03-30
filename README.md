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
tech_challenge_api/
├── app/
│   ├── __init__.py              # Inicializa o app Flask
│   ├── routes.py                # Todas as rotas e documentação Swagger
│   └── embrapa_scraper.py       # Lógica de scraping e leitura dos CSVs
├── run.py                       # Arquivo principal para rodar o Flask
├── requirements.txt             # Dependências do projeto
├── render.yaml                  # Script de deploy automático no Render
└── README.md                    # Documentação do projeto

## Testar localmente
```bash
pip install -r requirements.txt
python run.py
