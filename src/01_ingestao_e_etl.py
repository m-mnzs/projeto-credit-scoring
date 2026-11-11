import os 
import sqlite3
import pandas as pd 

def executar_ingestao():
    print("Iniciando a ingestão e ETL do dataset Give Me Some Credit.")

    # Pega o diretório exato onde o script está salvo
    dir_script = os.path.dirname(os.path.abspath(__file__))

    # Caminhos dos arquivos
    caminho_csv = os.path.join(dir_script, "..", "data", "cs-training.csv")
    caminho_db = os.path.join(dir_script, "..", "data", "credit_scoring.db")

    # Verifica se o arquivo CSV existe na pasta data/
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(
            f"Arquivo não encontrando em: {caminho_csv}. "
            "Por favor, verifique se o arquivo 'cs-training.csv' está na pasta data/." 
        )

    # 1. Leitura do dataset bruto
    print(f"Lendo o arquivo {caminho_csv}.")
    df = pd.read_csv(caminho_csv)

    # O Kaggle costuma exportar uma coluna de índice sem nome (ex: 'Unnamed: 0')
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Padronização básica de nomes de colunas para minúsculas (boa prática de engenharia)
    df.columns = [col.strip() for col in df.columns]

    print(f"Dataset carregado com sucesso! Dimensões: {df.shape[0]} linhas e {df.shape[1]} colunas.")

    # 2. Persistência em Banco SQLite para consultas rápidas
    print(f"Salvando os dados no banco SQLite ({caminho_db}).")
    conexao = sqlite3.connect(caminho_db)

    # Salva a tabela principal de treino
    df.to_sql("credito_treino", conexao, if_exists="replace", index=False)

    conexao.close()
    print("Ingestão concluída com sucesso! Banco de dados pronto para a EDA.")

if __name__ == "__main__":
    executar_ingestao()