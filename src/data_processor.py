# =============================================
# Script: data_processor.py
# Projeto: CryptoPrice-Dashboard
# Descrição: Processa e analisa os dados brutos de criptomoedas
# Autor: Nathan Thomaz
# Data de Criação: 27/04/2025
# Versão: 1.0
# =============================================

import pandas as pd
import os
from glob import glob

# =============================================
# Funções
# =============================================

# =============================================
# load_latest_data
# =============================================
def load_latest_data(raw_data_path="data/raw/"):
    """
    Carrega o arquivo CSV mais recente da pasta de dados brutos.
    
    Args:
        raw_data_path (str): Caminho da pasta onde estão os arquivos brutos.
    
    Returns:
        pd.DataFrame: Dados carregados em um DataFrame.
    """
    # Procura todos os CSVs na pasta de dados brutos
    list_of_files = glob(os.path.join(raw_data_path, "*.csv"))
    
    if not list_of_files:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado em 'data/raw/'.")

    # Pega o arquivo mais recente (pelo nome, que tem data/hora)
    latest_file = max(list_of_files, key=os.path.getctime)

    # Lê o CSV para um DataFrame
    df = pd.read_csv(latest_file)
    return df

# =============================================
# analyze_data
# =============================================
def analyze_data(df):
    """
    Realiza análises nos dados de criptomoedas.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados brutos.
    
    Returns:
        dict: Resultados da análise (melhor, pior moeda e média de variação).
    """
    # Encontrar a moeda com maior valorização
    best_coin = df.loc[df['price_change_percentage_24h'].idxmax()]

    # Encontrar a moeda com maior desvalorização
    worst_coin = df.loc[df['price_change_percentage_24h'].idxmin()]

    # Calcular a média de variação das moedas
    avg_change = df['price_change_percentage_24h'].mean()

    result = {
        "best_coin": best_coin['name'],
        "best_change": best_coin['price_change_percentage_24h'],
        "worst_coin": worst_coin['name'],
        "worst_change": worst_coin['price_change_percentage_24h'],
        "average_change": avg_change
    }

    return result

# =============================================
# save_analysis
# =============================================
def save_analysis(result, processed_data_path="data/processed/"):
    """
    Salva o resultado da análise em um arquivo CSV.
    
    Args:
        result (dict): Resultados da análise.
        processed_data_path (str): Caminho para salvar os dados tratados.
    """
    os.makedirs(processed_data_path, exist_ok=True)

    df_result = pd.DataFrame([result])
    filename = os.path.join(processed_data_path, "crypto_analysis.csv")
    df_result.to_csv(filename, index=False)

# =============================================
# Execução principal
# =============================================

if __name__ == "__main__":
    # Fluxo principal do script
    df = load_latest_data()
    analysis_result = analyze_data(df)
    save_analysis(analysis_result)
