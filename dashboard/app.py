# =============================================
# Script: app.py
# Projeto: CryptoPrice-Dashboard
# Descrição: Dashboard interativo para visualizar análises detalhadas de criptomoedas
# Autor: Nathan Thomaz
# Data de Atualização: 28/04/2025
# Versão: 2.0
# =============================================

from datetime import datetime
import streamlit as st  # type: ignore
import pandas as pd
import altair as alt  # type: ignore
import os
import glob
import subprocess
import sys
import time
import io

# =============================================
# Funções de Atualização
# =============================================

def atualizar_dados():
    data_fetcher_path = os.path.abspath(os.path.join("src", "data_fetcher.py"))
    data_processor_path = os.path.abspath(os.path.join("src", "data_processor.py"))
    root_path = os.path.abspath(".")

    try:
        with st.spinner("🔄 Atualizando dados..."):
            # Executa o fetcher
            fetcher_result = subprocess.run(
                [sys.executable, data_fetcher_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=root_path
            )

            if fetcher_result.returncode != 0:
                st.error(f"❌ Erro ao coletar dados:\n\n{fetcher_result.stderr}")
                return

            # Executa o processor
            subprocess.run(
                [sys.executable, data_processor_path],
                check=True,
                cwd=root_path
            )

        # Mensagem de sucesso
        mensagem_suave("✅ Dados atualizados com sucesso!")

    except subprocess.CalledProcessError as e:
        st.error(f"❌ Erro ao executar subprocesso: {e}")
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")

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

def mensagem_suave(mensagem):
    """
    Exibe uma mensagem que desaparece suavemente.
    """
    placeholder = st.empty()
    placeholder.success(mensagem)

    time.sleep(2)

    placeholder.markdown(
        """
        <style>
        .fade-message {
            animation: fadeOut 2s forwards;
        }
        @keyframes fadeOut {
            from {opacity: 1;}
            to {opacity: 0;}
        }
        </style>
        <div class="fade-message">
            ✅ Dados atualizados com sucesso!
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(2.5)
    placeholder.empty()

def load_analysis(processed_data_path="data/processed/crypto_analysis.csv"):
    if not os.path.exists(processed_data_path):
        st.error("Arquivo de análise não encontrado. Execute a atualização primeiro.")
        return None
    return pd.read_csv(processed_data_path)

def load_raw_data():
    """
    Carrega o arquivo de dados brutos mais recente para gráficos e tabelas detalhadas,
    e cria uma versão formatada para exibição.
    """
    raw_files = glob.glob('data/raw/*.csv')
    if raw_files:
        latest_raw_file = max(raw_files, key=os.path.getctime)
        df_raw = pd.read_csv(latest_raw_file)

        # Renomear colunas
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

        # Corrigir data
        df_raw['Última Atualização'] = pd.to_datetime(df_raw['Última Atualização']).dt.strftime('%Y-%m-%d %H:%M:%S')

        # Criar versão formatada
        df_formatado = df_raw.copy()

        # Formatando valores monetários
        colunas_moeda = [
            "Preço Atual (US$)", "Valor de Mercado (US$)", "Volume Total (US$)",
            "Preço Máximo Histórico", "Preço Mínimo Histórico"
        ]
        colunas_quantidade = ["Quantidade Circulante"]

        for col in colunas_moeda:
            df_formatado[col] = df_formatado[col].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        for col in colunas_quantidade:
            df_formatado[col] = df_formatado[col].apply(lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))

        df_formatado["Variação 24h (%)"] = df_formatado["Variação 24h (%)"].apply(lambda x: f"{x:.2f}%")

        return df_raw, df_formatado
    else:
        return None, None

# =============================================
# Funções de Páginas
# =============================================

def pegar_ultima_data():
    """
    Busca a data da última atualização dos dados processados.
    """
    caminho = "data/processed/crypto_analysis.csv"
    if os.path.exists(caminho):
        timestamp = os.path.getmtime(caminho)
        ultima_data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        return ultima_data
    return None

def mostrar_visao_geral(df):

    # Buscar dados do dataframe
    moeda_subiu = df['best_coin'][0]
    var_subiu = df['best_change'][0]

    moeda_caiu = df['worst_coin'][0]
    var_caiu = df['worst_change'][0]

    media_geral = df['average_change'][0]

    # Layout com três colunas de cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style='padding: 1rem; border-radius: 12px; background-color: #1c1c1c; text-align: center;'>
                <h3>📈 Moeda que Mais Subiu</h3>
                <h1 style='color: #22c55e;'>{moeda_subiu}</h1>
                <p style='color: #22c55e; font-size: 1.5rem;'>⬆️ {var_subiu:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='padding: 1rem; border-radius: 12px; background-color: #1c1c1c; text-align: center;'>
                <h3>📉 Moeda que Mais Caiu</h3>
                <h1 style='color: #ef4444;'>{moeda_caiu}</h1>
                <p style='color: #ef4444; font-size: 1.5rem;'>⬇️ {var_caiu:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style='padding: 1rem; border-radius: 12px; background-color: #1c1c1c; text-align: center;'>
                <h3>📊 Média de Variação</h3>
                <h1 style='color: #60a5fa;'>{media_geral:.2f}%</h1>
                <h4></h4>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Pequena mensagem motivacional com base na media geral
    if media_geral >= 0.5:
        st.success("🚀 O mercado está em alta! Fique atento às oportunidades.")
    elif media_geral <= -0.5:
        st.error("📉 Atenção! O mercado está retraindo hoje.")
    else:
        st.info("📈 Mercado está relativamente estável no momento.")

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================
    # Top 3 moedas que mais subiram
    # =============================
    st.subheader("🏆 Top 3 Criptomoedas em Alta")

    top3 = df[['top1_coin', 'top1_change', 'top2_coin', 'top2_change', 'top3_coin', 'top3_change']]

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(label=top3['top1_coin'][0], value=f"{top3['top1_change'][0]:.2f}%", delta_color="normal")

    with col5:
        st.metric(label=top3['top2_coin'][0], value=f"{top3['top2_change'][0]:.2f}%", delta_color="normal")

    with col6:
        st.metric(label=top3['top3_coin'][0], value=f"{top3['top3_change'][0]:.2f}%", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================
    # Gráfico de quantas moedas subiram e caíram
    # =============================
    st.subheader("📊 Resumo de Performance das Moedas")

    # Exemplo de df para gráfico
    grafico_df = pd.DataFrame({
        'Status': ['Subiram', 'Caíram'],
        'Quantidade': [df['coins_up'][0], df['coins_down'][0]]
    })

    grafico = alt.Chart(grafico_df).mark_bar(size=40).encode(
        x=alt.X('Status:N', title='Status'),
        y=alt.Y('Quantidade:Q', title='Quantidade de Moedas'),
        color=alt.Color('Status:N', scale=alt.Scale(domain=['Subiram', 'Caíram'], range=['#22c55e', '#ef4444'])),
        tooltip=['Status:N', 'Quantidade:Q']
    ).properties(
        width=500,
        height=300
    )

    st.altair_chart(grafico, use_container_width=True)

    # =============================
    # Última atualização humanizada
    # =============================
    ultima_atualizacao = df['ultima_atualizacao'][0]
    ultima_atualizacao_dt = datetime.strptime(ultima_atualizacao, '%Y-%m-%d %H:%M:%S')
    tempo_passado = datetime.now() - ultima_atualizacao_dt
    minutos_passados = int(tempo_passado.total_seconds() // 60)

    st.caption(f"⏳ Atualizado há {minutos_passados} minutos.")

def mostrar_graficos(df_raw):
    st.header("📊 Análises Gráficas")

    if df_raw is not None:
        moedas_disponiveis = sorted(df_raw["Nome da Moeda"].unique())

        # 🔍 Opção para mostrar apenas favoritas
        mostrar_so_favoritas = st.checkbox("🔍 Mostrar apenas favoritas", value=False)

        if mostrar_so_favoritas and "favoritas" in st.session_state and st.session_state.favoritas:
            moedas_disponiveis = [moeda for moeda in moedas_disponiveis if moeda in st.session_state.favoritas]

        opcoes_moedas = st.multiselect(
            "Escolha as criptomoedas para visualizar:",
            options=moedas_disponiveis,
            default=moedas_disponiveis,
            placeholder="Selecione moedas..."
        )

        metricas_disponiveis = ["Variação 24h (%)", "Preço Atual (US$)", "Quantidade Circulante"]
        metrica_escolhida = st.selectbox(
            "Selecione a métrica para o gráfico:",
            metricas_disponiveis
        )

        ordenacao = st.radio(
            "Ordenação dos dados:",
            ("Misto", "Crescente", "Decrescente"),
            horizontal=True,
            label_visibility="collapsed"
        )

        df_filtrado = df_raw[df_raw["Nome da Moeda"].isin(opcoes_moedas)][["Nome da Moeda", metrica_escolhida]].copy()

        if metrica_escolhida in ["Preço Atual (US$)", "Variação 24h (%)", "Quantidade Circulante"]:
            df_filtrado[metrica_escolhida] = (
                df_filtrado[metrica_escolhida]
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .astype(float)
            )

        if ordenacao == "Crescente":
            df_filtrado = df_filtrado.sort_values(by=metrica_escolhida, ascending=True)
        elif ordenacao == "Decrescente":
            df_filtrado = df_filtrado.sort_values(by=metrica_escolhida, ascending=False)

        st.markdown("---")

        st.caption({
            "Variação 24h (%)": "ℹ️ Percentual de valorização ou desvalorização nas últimas 24 horas.",
            "Preço Atual (US$)": "ℹ️ Valor atual da criptomoeda em dólares americanos.",
            "Quantidade Circulante": "ℹ️ Número total de unidades disponíveis no mercado."
        }[metrica_escolhida])

        chart = alt.Chart(df_filtrado).mark_bar(size=40).encode(
            x=alt.X('Nome da Moeda:N', sort=None, title='Criptomoeda'),
            y=alt.Y(f'{metrica_escolhida}:Q', title=metrica_escolhida),
            color=alt.condition(
                alt.datum[metrica_escolhida] >= 0,
                alt.value("#4CAF50"),
                alt.value("#FF5252")
            ),
            tooltip=[alt.Tooltip('Nome da Moeda:N'), alt.Tooltip(f'{metrica_escolhida}:Q', format=",.2f")]
        ).properties(
            width=800,
            height=500
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("Nenhum dado disponível para gerar o gráfico.")

def mostrar_tabela(df_raw, df_raw_formatado):
    st.header("🔍 Tabela Detalhada das Criptomoedas")

    if df_raw is not None and df_raw_formatado is not None:
        tipo_exibicao = st.radio(
            "Tipo de Exibição:",
            ("Formatado (padrão)", "Dados Brutos"),
            horizontal=True
        )

        df_exibido = df_raw_formatado if tipo_exibicao == "Formatado (padrão)" else df_raw

        moedas_disponiveis = sorted(df_exibido["Nome da Moeda"].unique())

        mostrar_so_favoritas = st.checkbox("🔍 Mostrar apenas favoritas", value=False)

        if mostrar_so_favoritas and "favoritas" in st.session_state and st.session_state.favoritas:
            moedas_disponiveis = [moeda for moeda in moedas_disponiveis if moeda in st.session_state.favoritas]

        opcoes_moedas = st.multiselect(
            "Filtrar criptomoedas:",
            options=moedas_disponiveis,
            default=moedas_disponiveis,
            placeholder="Selecione as moedas..."
        )

        df_filtrado = df_exibido[df_exibido["Nome da Moeda"].isin(opcoes_moedas)].copy()
        df_filtrado.index = df_filtrado.index + 1

        st.dataframe(df_filtrado, use_container_width=True)

        formato_exportacao = st.radio(
            "Escolha o formato para exportar:",
            ("CSV", "Excel (.xlsx)"),
            horizontal=True
        )

        data_atual = datetime.now().strftime("%Y-%m-%d")
        nome_base = f"CryptoPrice_Tabela_{data_atual}"

        if formato_exportacao == "CSV":
            buffer = io.BytesIO()
            df_filtrado.to_csv(buffer, index=False, encoding='utf-8-sig')
            buffer.seek(0)
            st.download_button(
                label="⬇️ Baixar Tabela (CSV)",
                data=buffer,
                file_name=f"{nome_base}.csv",
                mime='text/csv'
            )

        elif formato_exportacao == "Excel (.xlsx)":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_filtrado.to_excel(writer, sheet_name='Criptomoedas', index=False)
            buffer.seek(0)
            st.download_button(
                label="⬇️ Baixar Tabela (Excel)",
                data=buffer,
                file_name=f"{nome_base}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    else:
        st.warning("Nenhum dado para mostrar.")

def mostrar_favoritas(df_raw):
    st.header("⭐ Gerenciar Moedas Favoritas")

    if "favoritas" not in st.session_state:
        st.session_state.favoritas = []

    if df_raw is not None:
        moedas_disponiveis = sorted(df_raw["Nome da Moeda"].unique())

        for moeda in moedas_disponiveis:
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.write(moeda)
            with col2:
                if moeda in st.session_state.favoritas:
                    if st.button("⭐", key=f"desfav_{moeda}"):
                        st.session_state.favoritas.remove(moeda)
                else:
                    if st.button("☆", key=f"fav_{moeda}"):
                        st.session_state.favoritas.append(moeda)

        if st.session_state.favoritas:
            st.success(f"Favoritas: {', '.join(st.session_state.favoritas)}")
        else:
            st.info("Nenhuma moeda favoritada ainda.")
    else:
        st.warning("Nenhum dado disponível para favoritar.")

# =============================================
# Aplicativo Principal
# =============================================

def main():
    st.set_page_config(page_title="Crypto Dashboard", layout="wide")

    # Título Principal
    st.title("🚀 CryptoPrice Dashboard")
    st.subheader("Monitoramento detalhado de crescimento e variação de criptomoedas.")

    # Sidebar
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
    if st.sidebar.button("⭐ Moedas Favoritas"):
        st.session_state.pagina = "⭐ Moedas Favoritas"

    # Separador
    st.sidebar.markdown("---")

    # Botão de Atualizar Dados
    if st.sidebar.button("🔄 Atualizar Dados"):
        atualizar_dados()

    # 🕒 Mostrar última atualização no sidebar
    ultima_atualizacao = pegar_ultima_data()
    if ultima_atualizacao:
        st.sidebar.markdown(
            f"""
            <div style="padding-left: 5px; font-size: 0.85em;">
                🕒 <b>Última Atualização:</b><br>
                <span style="padding-left: 10px;">{ultima_atualizacao}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Carregar os dados
    df = load_analysis()
    df_raw, df_raw_formatado = load_raw_data()

    # Exibir o conteúdo da página
    if df is not None:
        if st.session_state.pagina == "🏠 Visão Geral":
            mostrar_visao_geral(df)
        elif st.session_state.pagina == "📈 Gráficos":
            mostrar_graficos(df_raw)
        elif st.session_state.pagina == "📑 Tabela Detalhada":
            mostrar_tabela(df_raw, df_raw_formatado) 
        elif st.session_state.pagina == "⭐ Moedas Favoritas":
            mostrar_favoritas(df_raw)
    else:
        st.warning("Nenhum dado carregado. Clique em 'Atualizar Dados'.")

# =============================================
# Execução
# =============================================

if __name__ == "__main__":
    main()
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
