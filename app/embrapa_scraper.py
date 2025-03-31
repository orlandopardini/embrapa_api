import pandas as pd

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"

# Subtipos obrigatórios para cada tipo
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
    }
}

# Rotas que funcionam normalmente sem subtipo
def get_producao():
    return baixar_csv("Producao.csv")

def get_comercializacao():
    return baixar_csv("Comercio.csv")

# Centraliza leitura
def baixar_csv(nome_arquivo):
    try:
        url = BASE_URL + nome_arquivo
        df = pd.read_csv(url, sep=';', encoding='latin1')
        return df.to_dict(orient='records')
    except Exception as e:
        return {"erro": f"Erro ao baixar {nome_arquivo}: {str(e)}"}

# Acessa tipo/subtipo obrigatório
def get_subtipo(tipo, subtipo):
    try:
        nome_arquivo = ARQUIVOS[tipo][subtipo]
        return baixar_csv(nome_arquivo)
    except KeyError:
        return {
            "erro": f"Tipo ou subtipo invalido: '{tipo}/{subtipo}'",
            "tipos_disponiveis": list(ARQUIVOS.keys()),
            "subtipos_disponiveis": ARQUIVOS.get(tipo, {})
        }
