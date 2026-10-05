import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuração de Inicialização do Painel
st.set_page_config(page_title="Explorador Eleitoral Dinâmico 2026", layout="wide")
st.title("🔍 Sistema sob Demanda - Eleições Gerais 2026")

# 2. Engenharia de Dados: Criação e Carga da Base Geral Consolidada na Memória
dados_completos = [
    # --- SUDESTE ---
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 12850000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 9430000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Governador", "Partido": "Republicanos", "Candidato": "Tarcísio de Freitas (Eleito)", "Votos": 14725000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Senador", "Partido": "PP", "Candidato": "Guilherme Derrite (Eleito)", "Votos": 7180000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Senador", "Partido": "PL", "Candidato": "André do Prado (Eleito)", "Votos": 6870000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Deputado Federal", "Partido": "PL", "Candidato": "Lucas Pavanato (Mais Votado)", "Votos": 3038438},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Deputado Federal", "Partido": "PSOL", "Candidato": "Erika Hilton", "Votos": 1596472},
    
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 5820000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 5610000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Governador", "Partido": "Republicanos", "Candidato": "Cleitinho Azevedo (Eleito)", "Votos": 6150000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Deputado Estadual", "Partido": "PL", "Candidato": "Bruno Engler (Mais Votado)", "Votos": 600000},

    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 4910000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 3850000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Governador", "Partido": "PL", "Candidato": "Douglas Ruas (2º Turno)", "Votos": 4120000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Governador", "Partido": "PSD", "Candidato": "Eduardo Paes (2º Turno)", "Votos": 3580000},

    # --- SUL ---
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 3450000},
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 1950000},
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Governador", "Partido": "PL", "Candidato": "Sergio Moro (Eleito)", "Votos": 3120000},

    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 2410000},
    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 1150000},
    {"Regiao": "Sul", "SC", "Cargo": "Governador", "Partido": "PL", "Candidato": "Jorginho Mello (Eleito)", "Votos": 2942386},

    # --- NORDESTE ---
    {"Regiao": "Nordeste", "Estado": "BA", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 4850000},
    {"Regiao": "Nordeste", "Estado": "BA", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 2150000},
    {"Regiao": "Nordeste", "Estado": "BA", "Cargo": "Governador", "Partido": "PT", "Candidato": "Jerônimo Rodrigues (Eleito)", "Votos": 4100000},

    {"Regiao": "Nordeste", "Estado": "PE", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 2950000},
    {"Regiao": "Nordeste", "Estado": "PE", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 1910000},
    {"Regiao": "Nordeste", "Estado": "PE", "Cargo": "Governador", "Partido": "PSDB", "Candidato": "Raquel Lyra (Eleito)", "Votos": 2530000}
]

df = pd.DataFrame(dados_completos)

# ==========================================
# CONTROLES INTERATIVOS (SIDEBAR)
# ==========================================
st.sidebar.header("🎯 Parâmetros da Consulta")

# Seletor dinâmico de cargos baseado nos dados existentes
cargo_selecionado = st.sidebar.selectbox("Escolha o Cargo para Filtrar:", df["Cargo"].unique())

# Filtro multi-seleção por região geográfica
regioes_disponiveis = df["Regiao"].unique()
regiao_selecionada = st.sidebar.multiselect("Filtrar por Região (Vazio = Todas):", options=regioes_disponiveis, default=[])

# Controle de Ordenação de Dados
ordem_votos = st.sidebar.radio("Classificação dos Resultados:", ["Do maior para o menor", "Do menor para o maior"])
ascendente = True if ordem_votos == "Do menor para o maior" else False

# Slider dinâmico para limitar o Top N do gráfico na tela
max_linhas = len(df[df["Cargo"] == cargo_selecionado])
top_n = st.sidebar.slider("Quantidade máxima de registros na tela:", min_value=2, max_value=max_linhas, value=min(5, max_linhas))

# ==========================================
# FILTRAGEM ATIVA VIA PANDAS
# ==========================================
df_filtrado = df[df["Cargo"] == cargo_selecionado]

if regiao_selecionada:
    df_filtrado = df_filtrado[df_filtrado["Regiao"].isin(regiao_selecionada)]

# Aplica ordenação e o limite do Slider
df_filtrado = df_filtrado.sort_values(by="Votos", ascending=ascendente).head(top_n)

# ==========================================
# RENDERIZAÇÃO DOS GRÁFICOS INTERATIVOS
# ==========================================
st.subheader(f"🏆 Resultados em Tempo Real: {cargo_selecionado}")

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    # Gráfico de Barras Dinâmico com correção estrita de cor de texto para dark/light mode
    fig = px.bar(
        df_filtrado,
        x="Candidato",
        y="Votos",
        color="Partido",
        title=f"Ranking de Votos - {cargo_selecionado} (Exibindo {len(df_filtrado)} registros)",
        labels={"Votos": "Votos Válidos", "Candidato": "Candidato / Legenda"},
        text_auto=",.0f"
    )
    
    # Customização das propriedades de Hover/Tooltip e Layout adaptativo
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", font_color="black")
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Exibição simultânea das tabelas estruturadas abaixo do gráfico
    col_esquerda, col_direita = st.columns(2)
    
    with col_esquerda:
        st.markdown("### 📋 Tabela de Dados Filtrados")
        st.dataframe(df_filtrado[["Estado", "Partido", "Candidato", "Votos"]], hide_index=True, use_container_width=True)
        
    with col_direita:
        st.markdown("### 🏢 Concentração de Votos por Partido")
        soma_partidos = df_filtrado.groupby("Partido")["Votos"].sum().reset_index().sort_values(by="Votos", ascending=False)
        st.dataframe(soma_partidos, hide_index=True, use_container_width=True)
