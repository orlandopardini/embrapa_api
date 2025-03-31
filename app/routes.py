from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .embrapa_scraper import (
    get_producao, get_comercializacao, get_subtipo
)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({'message': 'API Flask rodando com sucesso!'})

@main.route('/producao')
@swag_from({
    'tags': ['Produção'],
    'description': 'Retorna dados da produção vitivinícola do Brasil',
    'responses': {
        200: {
            'description': 'Lista com produtos e quantidades em litros',
            'examples': {
                'application/json': [
                    {"Produto": "VINHO DE MESA - Tinto", "Quantidade (L.)": "139.320.884"},
                    {"Produto": "VINHO DE MESA - Branco", "Quantidade (L.)": "27.910.299"}
                ]
            }
        }
    }
})
def producao():
    return jsonify(get_producao())

@main.route('/comercializacao')
@swag_from({
    'tags': ['Comercialização'],
    'description': 'Retorna dados de comercialização de vinhos e derivados',
    'responses': {
        200: {
            'description': 'Lista com produtos e volumes comercializados',
            'examples': {
                'application/json': [
                    {"Produto": "Espumante - Branco", "Quantidade (L.)": "1.234.567"},
                    {"Produto": "Suco de Uva", "Quantidade (L.)": "4.567.890"}
                ]
            }
        }
    }
})
def comercializacao():
    return jsonify(get_comercializacao())

@main.route('/processamento')
@swag_from({
    'tags': ['Processamento'],
    'description': 'Retorna dados de uvas processadas. Subtipos: viniferas, americanas, mesa, semclass',
    'parameters': [
        {'name': 'subtipo', 'in': 'query', 'type': 'string', 'required': True,
         'description': 'Subtipo obrigatório: viniferas, americanas, mesa, semclass'}
    ],
    'responses': {
        200: {'description': 'Dados retornados com sucesso'},
        400: {'description': 'Subtipo não especificado ou inválido'}
    }
})
def processamento():
    subtipo = request.args.get('subtipo')
    if not subtipo:
        return jsonify({'erro': 'Subtipo obrigatorio (viniferas, americanas, mesa, semclass), ou seja, você precisa especificar como no exemplo --> processamento?subtipo=viniferas'}), 400
    return jsonify(get_subtipo('processamento', subtipo))


@main.route('/importacao')
@swag_from({
    'tags': ['Importação'],
    'description': 'Retorna dados de importação. Subtipos: vinhos, espumantes, frescas, passas, sucos',
    'parameters': [
        {'name': 'subtipo', 'in': 'query', 'type': 'string', 'required': True,
         'description': 'Subtipo obrigatório: vinhos, espumantes, frescas, passas, sucos'}
    ],
    'responses': {
        200: {'description': 'Dados retornados com sucesso'},
        400: {'description': 'Subtipo não especificado ou inválido'}
    }
})
def importacao():
    subtipo = request.args.get('subtipo')
    if not subtipo:
        return jsonify({'erro': 'Subtipo obrigatorio (vinhos, espumantes, frescas, passas, suco), ou seja, você precisa especificar como no exemplo --> importacao?subtipo=suco'}), 400
    return jsonify(get_subtipo('importacao', subtipo))


@main.route('/exportacao')
@swag_from({
    'tags': ['Exportação'],
    'description': 'Retorna dados de exportação. Subtipos: vinho, espumantes, uva, suco',
    'parameters': [
        {'name': 'subtipo', 'in': 'query', 'type': 'string', 'required': True,
         'description': 'Subtipo obrigatório: vinho, espumantes, uva, suco'}
    ],
    'responses': {
        200: {'description': 'Dados retornados com sucesso'},
        400: {'description': 'Subtipo não especificado ou inválido'}
    }
})
def exportacao():
    subtipo = request.args.get('subtipo')
    if not subtipo:
        return jsonify({'erro': 'Subtipo obrigatorio (vinho, espumantes, uva, suco), ou seja, você precisa especificar como no exemplo --> exportacao?subtipo=vinho'}), 400
    return jsonify(get_subtipo('exportacao', subtipo))
