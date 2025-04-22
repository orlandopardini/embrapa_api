from flask import Blueprint, jsonify, request, render_template
from flasgger import swag_from
from .embrapa_scraper import get_producao, get_comercializacao, get_subtipo

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("tabela.html", tipo='', subtipo='', dados=[], anos=[], subtipos=[], ano='')

@main.route('/producao')
@swag_from({
    'tags': ['Produção'],
    'description': 'Retorna dados da produção vitivinícola do Brasil. O arquivo original é separado por ponto e vírgula e contém os anos como colunas. Cada linha é reorganizada para o formato Produto, Ano e Quantidade (L). A acentuação dos produtos é corrigida.',
    'responses': {
        200: {
            'description': 'Lista com produtos e quantidades em litros',
            'examples': {
                'application/json': [
                    {"Produto": "VINHO DE MESA - Tinto", "Ano": 2023, "Quantidade (L)": 139320884},
                    {"Produto": "VINHO DE MESA - Branco", "Ano": 2023, "Quantidade (L)": 27910299}
                ]
            }
        }
    }
})
def producao():
    ano = request.args.get("ano")
    dados = get_producao()
    dados_filtrados = filtrar_dados_por_ano(dados, ano)
    for d in dados_filtrados:
        d.pop('Id', None)
    anos = get_anos_unicos(dados)
    return render_template("tabela.html", tipo='producao', subtipo='todos', dados=dados_filtrados, anos=anos, subtipos=[], ano=ano)

@main.route('/comercializacao')
@swag_from({
    'tags': ['Comercialização'],
    'description': 'Retorna dados de comercialização de vinhos e derivados. O arquivo original é separado por ponto e vírgula, contendo colunas de anos. Cada linha é transformada no formato Produto, Ano, Quantidade (L). A acentuação é tratada.',
    'responses': {
        200: {
            'description': 'Lista com produtos e volumes comercializados',
            'examples': {
                'application/json': [
                    {"Produto": "Espumante - Branco", "Ano": 2023, "Quantidade (L)": 1234567},
                    {"Produto": "Suco de Uva", "Ano": 2023, "Quantidade (L)": 4567890}
                ]
            }
        }
    }
})
def comercializacao():
    ano = request.args.get("ano")
    dados = get_comercializacao()
    dados_filtrados = filtrar_dados_por_ano(dados, ano)
    for d in dados_filtrados:
        d.pop('Id', None)
    anos = get_anos_unicos(dados)
    return render_template("tabela.html", tipo='comercializacao', subtipo='todos', dados=dados_filtrados, anos=anos, subtipos=[], ano=ano)

def filtrar_dados_por_ano(dados, ano):
    if ano and ano.isdigit():
        return [d for d in dados if 'Ano' in d and str(d['Ano']).strip().isdigit() and int(d['Ano']) == int(ano)]
    return dados

def get_anos_unicos(dados):
    return sorted({str(d.get("Ano")) for d in dados if "Ano" in d and str(d.get("Ano")).strip()})

def get_subtipos_por_tipo(tipo):
    return {
        'processamento': ['viniferas', 'americanas', 'mesa', 'semclass'],
        'importacao': ['vinhos', 'espumantes', 'frescas', 'passas', 'suco'],
        'exportacao': ['vinho', 'espumantes', 'uva', 'suco']
    }.get(tipo, [])

@main.route('/<tipo>/<subtipo>')
@swag_from({
    'tags': ['Importação', 'Exportação', 'Processamento'],
    'description': 'Retorna dados com base no tipo (importacao, exportacao, processamento) e subtipo informado.\n\n- **Importação e Exportação**: os arquivos possuem colunas duplicadas por ano, como `1970` e `1970.1`, representando Quantidade (Kg) e Valor (US$) respectivamente.\n- **Processamento**: os arquivos possuem colunas por ano, com quantidade em Kg e coluna `cultivar` tratada para corrigir caracteres.\n- A acentuação de `País` e `Cultivar` é corrigida.',
    'parameters': [
        {'name': 'tipo', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Tipo de dado'},
        {'name': 'subtipo', 'in': 'path', 'type': 'string', 'required': True, 'description': 'Subtipo do dado'},
        {'name': 'ano', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Ano (opcional) para filtrar'}
    ],
    'responses': {
        200: {
            'description': 'Dados retornados com sucesso',
            'examples': {
                'application/json': [
                    {"País": "Argentina", "Ano": 2023, "Quantidade (Kg)": 123456, "Valor (US$)": 78910},
                    {"Cultivar": "Bordo", "Ano": 2023, "Quantidade (Kg)": 654321}
                ]
            }
        },
        400: {'description': 'Tipo ou subtipo inválido'}
    }
})
def dados_tipo_subtipo(tipo, subtipo):
    subtipo = subtipo.lower().strip()
    tipo = tipo.lower().strip()

    subtipos_validos = get_subtipos_por_tipo(tipo)
    if subtipo not in subtipos_validos:
        return jsonify({'erro': f"Subtipo inválido '{subtipo}' para tipo '{tipo}'"}), 400

    ano = request.args.get("ano", "").strip()
    dados = get_subtipo(tipo, subtipo)
    dados_filtrados = filtrar_dados_por_ano(dados, ano)
    for d in dados_filtrados:
        d.pop('Id', None)
    anos = get_anos_unicos(dados)
    return render_template("tabela.html", tipo=tipo, subtipo=subtipo, dados=dados_filtrados, anos=anos, subtipos=subtipos_validos, ano=ano)
