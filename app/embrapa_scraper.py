import pandas as pd                # Biblioteca para manipulação de dados em forma de tabela (DataFrames)
import unicodedata                # Biblioteca para tratar textos e remover acentos

# URL base de onde os arquivos CSV da Embrapa são baixados
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"

# Dicionário que mapeia cada tipo de dado para os nomes dos arquivos correspondentes
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

# Função que remove acentos e normaliza o texto (usado para evitar erros em buscas por tipo/subtipo)
def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.lower()).encode('ASCII', 'ignore').decode('utf-8')

# Função que tenta corrigir a acentuação de textos codificados em latin1
def corrigir_texto(texto):
    try:
        return str(texto).encode('latin1').decode('utf-8')
    except:
        return str(texto)

# Função principal que baixa e trata os dados conforme o tipo de arquivo
def baixar_csv(nome_arquivo):
    try:
        # Determina se o separador é tab (\t) ou ponto e vírgula (;), com base no nome do arquivo
        sep = '\t' if any(palavra in nome_arquivo.lower() for palavra in [
            'americanas', 'mesa', 'semclass', 'vinhos', 'espumantes', 'frescas', 'passas', 'exp'
        ]) else ';'

        # Baixa o CSV e carrega no Pandas
        url = BASE_URL + nome_arquivo
        df = pd.read_csv(url, sep=sep, encoding='latin1')
        df.columns = [col.strip().replace('\xa0', ' ') for col in df.columns]

        # Caso seja um arquivo de Produção ou Comercialização
        if nome_arquivo in ['Producao.csv', 'Comercio.csv']:
            dados = []
            for _, row in df.iterrows():
                produto = corrigir_texto(row.get('produto') or row.get('Produto'))
                for col in df.columns:
                    if col.isnumeric():  # cada coluna de ano
                        dados.append({
                            'Produto': produto,
                            'Ano': int(col),
                            'Quantidade (L)': row[col]
                        })
            return dados

        # Caso seja um arquivo de Processamento
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

        # Caso seja importação ou exportação com colunas duplicadas (ex: 1970, 1970.1)
        colunas = df.columns.tolist()
        dados = []
        for _, row in df.iterrows():
            i = 2  # Começa da terceira coluna (Id, País são as duas primeiras)
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
                i += 2  # pula para o próximo par (ex: 1971, 1971.1)
        return dados

    except Exception as e:
        # Se der erro ao baixar ou tratar, retorna mensagem com erro
        return {"erro": f"Erro ao baixar {nome_arquivo}: {str(e)}"}

# Funções de acesso direto, retornam dados já tratados
def get_producao():
    return baixar_csv(ARQUIVOS['producao'])

def get_comercializacao():
    return baixar_csv(ARQUIVOS['comercializacao'])

# Função que retorna os dados de um subtipo qualquer (como 'vinhos' de importação, por exemplo)
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
