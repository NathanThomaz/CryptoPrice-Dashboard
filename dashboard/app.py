# =============================================
# Script: app.py
# Projeto: CryptoPrice-Dashboard
# Descrição: Dashboard interativo para visualizar análises detalhadas de criptomoedas
# Autor: Nathan Thomaz
# Data de Atualização: 27/04/2025
# Versão: 1.0
# =============================================

import streamlit as st  # type: ignore
import pandas as pd
import os
import glob
import subprocess
import sys
import time

# =============================================
# Funções de Atualização
# =============================================

def atualizar_dados():
    data_fetcher_path = os.path.abspath(os.path.join("src", "data_fetcher.py"))
    data_processor_path = os.path.abspath(os.path.join("src", "data_processor.py"))
    root_path = os.path.abspath(".")
    placeholder = st.empty()

    try:
        fetcher_result = subprocess.run(
            [sys.executable, data_fetcher_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=root_path
        )

        if fetcher_result.returncode != 0:
            placeholder.error(f"❌ Erro ao coletar dados:\n\n{fetcher_result.stderr}")
            time.sleep(3)
            placeholder.empty()
            return

        subprocess.run(
            [sys.executable, data_processor_path],
            check=True,
            cwd=root_path
        )

        placeholder.success("✅ Dados atualizados com sucesso!")
        fade_out(placeholder)

    except subprocess.CalledProcessError as e:
        placeholder.error(f"❌ Erro ao executar subprocesso: {e}")
        time.sleep(3)
        placeholder.empty()
    except Exception as e:
        placeholder.error(f"❌ Erro inesperado: {e}")
        time.sleep(3)
        placeholder.empty()

def fade_out(placeholder):
    """
    Faz a mensagem de sucesso desaparecer suavemente apenas apagando a opacidade,
    sem alterar tamanho, sem remover espaço, sem encolher.
    """
    placeholder.markdown(
        """
        <style>
        .fade-message {
            font-size: 20px;
            color: #22c55e;  /* verde bonito */
            animation: fadeOut 3s ease forwards;
            padding: 0.5rem;
            margin: 0.5rem 0;
            background-color: rgba(34, 197, 94, 0.1);
            border-radius: 8px;
            text-align: center;
        }
        @keyframes fadeOut {
            0% {opacity: 1;}
            100% {opacity: 0;}
        }
        </style>

        <div class="fade-message">
            ✅ Dados atualizados com sucesso!
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(4)  # Espera o fade-out terminar
    placeholder.empty()  # Remove o placeholder após o fade-out
    time.sleep(1)  # Espera um pouco antes de remover o placeholder
# =============================================
# Funções Auxiliares
# =============================================

def load_analysis(processed_data_path="data/processed/crypto_analysis.csv"):
    if not os.path.exists(processed_data_path):
        st.error("Arquivo de análise não encontrado. Execute a atualização primeiro.")
        return None
    return pd.read_csv(processed_data_path)

def load_raw_data():
    raw_files = glob.glob('data/raw/*.csv')
    if raw_files:
        latest_raw_file = max(raw_files, key=os.path.getctime)
        df_raw = pd.read_csv(latest_raw_file)

        df_raw.rename(columns={
            "id": "Nome Técnico",
            "symbol": "Símbolo",
            "name": "Nome da Moeda",
            "current_price": "Preço Atual (US$)",
            "price_change_percentage_24h": "Variação 24h (%)",
            "market_cap": "Valor de Mercado (US$)",
            "market_cap_rank": "Ranking de Mercado",
            "total_volume": "Volume Total (US$)",
            "circulating_supply": "Quantidade Circulante",
            "ath": "Preço Máximo Histórico",
            "atl": "Preço Mínimo Histórico",
            "last_updated": "Última Atualização"
        }, inplace=True)

        df_raw["Preço Atual (US$)"] = df_raw["Preço Atual (US$)"].round(2)
        df_raw["Variação 24h (%)"] = df_raw["Variação 24h (%)"].round(2)
        df_raw["Valor de Mercado (US$)"] = df_raw["Valor de Mercado (US$)"].round(0)
        df_raw["Volume Total (US$)"] = df_raw["Volume Total (US$)"].round(0)
        df_raw["Quantidade Circulante"] = df_raw["Quantidade Circulante"].apply(lambda x: f"{x:,.0f}")
        df_raw["Preço Máximo Histórico"] = df_raw["Preço Máximo Histórico"].round(2)
        df_raw["Preço Mínimo Histórico"] = df_raw["Preço Mínimo Histórico"].round(2)
        df_raw['Última Atualização'] = pd.to_datetime(df_raw['Última Atualização']).dt.strftime('%Y-%m-%d %H:%M')

        return df_raw
    else:
        return None

# =============================================
# Funções de Páginas
# =============================================

def mostrar_visao_geral(df):
    st.header("📊 Resumo da Análise")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Moeda que Mais Subiu", value=df['best_coin'][0], delta=f"{df['best_change'][0]:.2f}%")

    with col2:
        st.metric(label="Moeda que Mais Caiu", value=df['worst_coin'][0], delta=f"{df['worst_change'][0]:.2f}%")

    with col3:
        st.metric(label="Média de Variação", value=f"{df['average_change'][0]:.2f}%")

def mostrar_graficos(df_raw):
    st.header("📈 Análises Gráficas")

    if df_raw is not None:
        metric_option = st.selectbox(
            "Selecione a métrica para visualizar:",
            ["Variação 24h (%)", "Valor de Mercado (US$)", "Volume Total (US$)"]
        )

        if metric_option == "Variação 24h (%)":
            df_chart = df_raw.set_index('Nome da Moeda')["Variação 24h (%)"]
        elif metric_option == "Valor de Mercado (US$)":
            df_chart = df_raw.set_index('Nome da Moeda')["Valor de Mercado (US$)"]
        elif metric_option == "Volume Total (US$)":
            df_chart = df_raw.set_index('Nome da Moeda')["Volume Total (US$)"]

        st.bar_chart(df_chart)
    else:
        st.warning("Nenhum dado bruto encontrado para gerar o gráfico.")

def mostrar_tabela(df_raw):
    st.header("🔍 Dados Completos das 10 Principais Moedas")

    if df_raw is not None:
        df_raw.index = range(1, len(df_raw) + 1)
        st.dataframe(df_raw)
    else:
        st.warning("Nenhum dado bruto encontrado para exibir.")

# =============================================
# Aplicativo Principal
# =============================================

def main():
    st.set_page_config(page_title="Crypto Dashboard", layout="wide")

    # Título Principal
    st.title("🚀 CryptoPrice Dashboard")
    st.subheader("Monitoramento detalhado de crescimento e variação de criptomoedas.")

    # ========================================
    # Sidebar
    # ========================================
    st.sidebar.title("📋 Menu de Navegação")

    # Estado da página usando st.session_state
    if "pagina" not in st.session_state:
        st.session_state.pagina = "🏠 Visão Geral"

    # Botões para mudar de página
    if st.sidebar.button("🏠 Visão Geral"):
        st.session_state.pagina = "🏠 Visão Geral"
    if st.sidebar.button("📈 Gráficos"):
        st.session_state.pagina = "📈 Gráficos"
    if st.sidebar.button("📑 Tabela Detalhada"):
        st.session_state.pagina = "📑 Tabela Detalhada"

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Atualizar Dados"):
        atualizar_dados()

    # Carregar os dados
    df = load_analysis()
    df_raw = load_raw_data()

    # Exibir conteúdo conforme a página
    if df is not None:
        if st.session_state.pagina == "🏠 Visão Geral":
            mostrar_visao_geral(df)
        elif st.session_state.pagina == "📈 Gráficos":
            mostrar_graficos(df_raw)
        elif st.session_state.pagina == "📑 Tabela Detalhada":
            mostrar_tabela(df_raw)
    else:
        st.warning("Nenhum dado carregado. Clique em 'Atualizar Dados'.")

# =============================================
# Execução
# =============================================

if __name__ == "__main__":
    main()
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
