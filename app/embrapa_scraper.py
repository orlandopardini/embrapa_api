import pandas as pd
import unicodedata

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"

ARQUIVOS = {
    "processamento": {
        "viniferas": "ProcessaViniferas.csv",
        "americanas": "ProcessaAmericanas.csv",
        "mesa": "ProcessaMesa.csv",
        "semclass": "ProcessaSemclass.csv"
    },
    "importacao": {
        "vinhos": "ImpVinhos.csv",
        "espumantes": "ImpEspumantes.csv",
        "frescas": "ImpFrescas.csv",
        "passas": "ImpPassas.csv",
        "suco": "ImpSuco.csv"
    },
    "exportacao": {
        "vinho": "ExpVinho.csv",
        "espumantes": "ExpEspumantes.csv",
        "uva": "ExpUva.csv",
        "suco": "ExpSuco.csv"
    },
    "producao": "Producao.csv",
    "comercializacao": "Comercio.csv"
}

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.lower()).encode('ASCII', 'ignore').decode('utf-8')

def corrigir_texto(texto):
    try:
        return str(texto).encode('latin1').decode('utf-8')
    except:
        return str(texto)

def baixar_csv(nome_arquivo):
    try:
        sep = '\t' if any(palavra in nome_arquivo.lower() for palavra in [
            'americanas', 'mesa', 'semclass', 'vinhos', 'espumantes', 'frescas', 'passas', 'exp'
        ]) else ';'

        url = BASE_URL + nome_arquivo
        df = pd.read_csv(url, sep=sep, encoding='latin1')
        df.columns = [col.strip().replace('\xa0', ' ') for col in df.columns]

        if nome_arquivo in ['Producao.csv', 'Comercio.csv']:
            dados = []
            for _, row in df.iterrows():
                produto = corrigir_texto(row.get('produto') or row.get('Produto'))
                for col in df.columns:
                    if col.isnumeric():
                        dados.append({
                            'Produto': produto,
                            'Ano': int(col),
                            'Quantidade (L)': row[col]
                        })
            return dados

        if "processa" in nome_arquivo.lower():
            dados = []
            for _, row in df.iterrows():
                for col in df.columns:
                    if col.isnumeric():
                        cultivar = corrigir_texto(row.get('cultivar') or row.get('Cultivar') or 'Desconhecido')
                        try:
                            quantidade = float(str(row[col]).replace(',', '.').strip())
                        except:
                            quantidade = 0
                        dados.append({
                            'Cultivar': cultivar,
                            'Ano': int(col),
                            'Quantidade (Kg)': quantidade
                        })
            return dados

        # Importação/exportação com colunas duplicadas por ano (ex: 1970, 1970.1)
        colunas = df.columns.tolist()
        dados = []
        for _, row in df.iterrows():
            i = 2  # começa após Id e País
            while i < len(colunas):
                col1 = colunas[i]
                col2 = colunas[i+1] if i+1 < len(colunas) else None
                if col1.replace('.', '').isdigit():
                    ano = int(float(col1))
                    try:
                        quantidade = float(str(row[col1]).replace(',', '.')) if pd.notna(row[col1]) else 0
                    except:
                        quantidade = 0
                    try:
                        valor = float(str(row[col2]).replace(',', '.')) if col2 and pd.notna(row[col2]) else 0
                    except:
                        valor = 0
                    pais = corrigir_texto(row.get('País') or row.get('Pais') or row.get('PaÃ­s') or 'Desconhecido')
                    dados.append({
                        'País': pais,
                        'Ano': ano,
                        'Quantidade (Kg)': quantidade,
                        'Valor (US$)': valor
                    })
                i += 2
        return dados

    except Exception as e:
        return {"erro": f"Erro ao baixar {nome_arquivo}: {str(e)}"}

def get_producao():
    return baixar_csv(ARQUIVOS['producao'])

def get_comercializacao():
    return baixar_csv(ARQUIVOS['comercializacao'])

def get_subtipo(tipo, subtipo):
    tipo = normalizar(tipo)
    subtipo = normalizar(subtipo)
    try:
        if tipo in ['producao', 'comercializacao']:
            nome_arquivo = ARQUIVOS[tipo]
        else:
            nome_arquivo = ARQUIVOS[tipo][subtipo]
        return baixar_csv(nome_arquivo)
    except KeyError:
        return {
            "erro": f"Tipo ou subtipo invalido: '{tipo}/{subtipo}'",
            "tipos_disponiveis": list(ARQUIVOS.keys()),
            "subtipos_disponiveis": ARQUIVOS.get(tipo, {})
        }
