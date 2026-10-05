import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Eleitoral Dinâmico 2026", layout="wide")
st.title("📊 Painel Analítico das Eleições Gerais 2026")

# Carregar base de dados
df = pd.read_csv("dados/eleicao_2026.csv")

# ==========================================
# PAINEL DE CONTROLES (SIDEBAR DINÂMICA)
# ==========================================
st.sidebar.header("🛠️ Filtros e Ordenação Dinâmica")

# 1. Filtro Top N Estados
top_n = st.sidebar.slider("Exibir quantos Estados no Ranking?", min_value=3, max_value=10, value=5)

# 2. Critério de Ordenação dos Gráficos
criterio_votos = st.sidebar.selectbox(
    "Ordenar Estados com base em:",
    ["Votos Flávio Bolsonaro", "Votos Lula", "Eleitores Aptos"]
)

mapa_criterio = {
    "Votos Flávio Bolsonaro": "Votos_Flavio_Bolsonaro",
    "Votos Lula": "Votos_Lula",
    "Eleitores Aptos": "Eleitores_Aptos_Milhoes"
}
coluna_ordenacao = mapa_criterio[criterio_votos]

# 3. Tipo de Ordem
ordem_crescente = st.sidebar.radio("Direção da Ordem:", ["Decrescente (Maiores primeiro)", "Crescente"])
ascendente = True if ordem_crescente == "Crescente" else False

# Processamento de Dados via Pandas baseado nos Filtros da Interface
df_filtrado = df.sort_values(by=coluna_ordenacao, ascending=ascendente).head(top_n)

# ==========================================
# ABAS DO DASHBOARD
# ==========================================
aba1, aba2 = st.tabs(["🏆 Rankings e Filtros Dinâmicos", "🏛️ Macroanálise de Partidos & Governadores"])

with aba1:
    st.subheader(f"🥇 Top {top_n} Estados ordenados por: {criterio_votos}")
    
    # Criando colunas de métricas interativas
    m1, m2 = st.columns(2)
    with m1:
        total_flavio = df_filtrado["Votos_Flavio_Bolsonaro"].sum()
        st.metric(label=f"Total Votos Flávio Bolsonaro (Nesses {top_n} estados)", value=f"{total_flavio:,}")
    with m2:
        total_lula = df_filtrado["Votos_Lula"].sum()
        st.metric(label=f"Total Votos Lula (Nesses {top_n} estados)", value=f"{total_lula:,}")

    # Plotando o gráfico dinâmico conforme ordenação do usuário
    df_melted = df_filtrado.melt(
        id_vars=["Estado"],
        value_vars=["Votos_Flavio_Bolsonaro", "Votos_Lula"],
        var_name="Candidato",
        value_name="Votos"
    )
    
    fig_dinamico = px.bar(
        df_melted,
        x="Estado",
        y="Votos",
        color="Candidato",
        barmode="group",
        title=f"Comparativo de Votação Presidencial Dinâmica (Top {top_n})",
        labels={"Votos": "Total de Votos", "Candidato": "Candidato"},
        color_discrete_sequence=["#1A5276", "#922B21"]
    )
    st.plotly_chart(fig_dinamico, use_container_width=True)

with aba2:
    st.subheader("🏢 Partidos com Maior Participação e Poder nos Governos Estaduais")
    
    col_gov1, col_gov2 = st.columns([1, 2])
    
    with col_gov1:
        st.markdown("**Balanço de Governadores Eleitos no 1º Turno (Base)**")
        # Contagem dinâmica de governadores eleitos por partido usando o valor da nossa base
        df_partidos_gov = df[df["Partido_Governador"] != "2º Turno"]["Partido_Governador"].value_counts().reset_index()
        df_partidos_gov.columns = ["Partido", "Governadores_Eleitos"]
        
        st.dataframe(df_partidos_gov, hide_index=True)
        
    with col_gov2:
        # Gráfico dinâmico dos governadores por legenda
        fig_gov = px.pie(
            df_partidos_gov,
            values="Governadores_Eleitos",
            names="Partido",
            title="Distribuição do comando dos Estados por Partido (1º Turno)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        st.plotly_chart(fig_gov, use_container_width=True)

    # Exibindo os dados brutos filtrados para auditoria rápida do usuário
    st.markdown("### 📋 Tabela de Dados Reais Filtrada (Auditável)")
    st.dataframe(df_filtrado[["Estado", "Eleitores_Aptos_Milhoes", "Votos_Flavio_Bolsonaro", "Votos_Lula", "Governador_Eleito", "Partido_Governador"]], use_container_width=True)
