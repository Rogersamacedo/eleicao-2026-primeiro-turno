import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Explorador Eleitoral 2026", layout="wide")
st.title("🔍 Sistema sob Demanda - Eleições Gerais 2026")

# Carregar base tratada unificada
try:
    df = pd.read_csv("dados/eleicoes_gerais_2026.csv")
except FileNotFoundError:
    st.error("Rode o script de criação da base 'eleicoes_gerais_2026.csv' primeiro!")
    st.stop()

# ==========================================
# PAINEL LATERAL DE SELEÇÃO DINÂMICA
# ==========================================
st.sidebar.header("🎯 Parâmetros da Consulta")

# 1. Filtro Principal: Escolha do Cargo
cargo_selecionado = st.sidebar.selectbox(
    "Qual cargo deseja analisar?",
    df["Cargo"].unique()
)

# 2. Filtro Secundário: Região Geográfica
regiao_selecionada = st.sidebar.multiselect(
    "Filtrar por Região (Deixe vazio para todas):",
    options=df["Regiao"].unique(),
    default=[]
)

# Aplicando os filtros encadeados usando Pandas
df_filtrado = df[df["Cargo"] == int(cargo_selecionado) if isinstance(cargo_selecionado, int) else df["Cargo"] == cargo_selecionado]

if regiao_selecionada:
    df_filtrado = df_filtrado[df_filtrado["Regiao"].isin(regiao_selecionada)]

# 3. Ordenação Dinâmica Baseada no Gosto do Usuário
ordem = st.sidebar.radio("Classificação dos Mais Votados:", ["Do maior para o menor", "Do menor para o maior"])
ascendente = True if ordem == "Do menor para o maior" else False

df_filtrado = df_filtrado.sort_values(by="Votos", ascending=ascendente)

# ==========================================
# APRESENTAÇÃO DOS RESULTADOS CONFORME DEMANDA
# ==========================================
st.subheader(f"🏆 Resultados para o cargo de: {cargo_selecionado}")

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para a combinação de filtros selecionada.")
else:
    # Mostra o Top 10 Dinâmico em Gráfico de Barras com correção de tema escuro
    fig = px.bar(
        df_filtrado,
        x="Candidato",
        y="Votos",
        color="Partido",
        title=f"Ranking de Votação Nominal - {cargo_selecionado}",
        labels={"Votos": "Total de Votos Válidos", "Candidato": "Nome na Urna / Legenda"},
        text_auto=",.0f" # Plota os números em cima das barras de forma limpa
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Exibição dos Dados Brutos Filtrados para Cópia ou Análise de Partidos
    col_tabela, col_partido = st.columns([2, 1])
    
    with col_tabela:
        st.markdown("### 📋 Registros Encontrados")
        st.dataframe(df_filtrado, hide_index=True, use_container_width=True)
        
    with col_partido:
        st.markdown("### 📊 Participação por Partido")
        # Soma dinamicamente os votos agrupando por partido na consulta atual do usuário
        participacao_partido = df_filtrado.groupby("Partido")["Votos"].sum().reset_index().sort_values(by="Votos", ascending=False)
        st.dataframe(participacao_partido, hide_index=True, use_container_width=True)

    # Criando o Gráfico Dinâmico com correção de tema escuro
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
    
    # FIX: Força o Plotly a usar fontes claras e remove a opacidade da legenda
    fig_dinamico.update_layout(
        template="plotly_dark",  # Faz o gráfico adotar nativamente o modo escuro
        paper_bgcolor="rgba(0,0,0,0)",  # Mantém o fundo transparente integrado ao Streamlit
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),  # Força todos os textos (eixos e legenda) para branco
        legend=dict(
            bgcolor="rgba(30, 30, 30, 0.8)",  # Adiciona um fundo sólido escuro na legenda
            bordercolor="gray",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_dinamico, use_container_width=True)
