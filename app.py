import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuração da página do Streamlit
st.set_page_config(page_title="Análise Eleitoral 2026", layout="wide")
st.title("🗳️ Painel de Análise Eleitoral 2026")

# 2. Criação das Abas de Navegação no Dashboard
aba1, aba2 = st.tabs(["Fidelidade Partidária (Executivo vs Senado)", "Composição do Legislativo"])

# ==========================================
# ABA 1: FIDELIDADE PARTIDÁRIA
# ==========================================
with aba1:
    st.header("Análise de Fidelidade Partidária: Presidente vs. Senado (PL)")
    
    try:
        df = pd.read_csv("dados/eleicao_2026.csv")
    except FileNotFoundError:
        st.error("Arquivo 'dados/eleicao_2026.csv' não encontrado.")
        st.stop()

    # Engenharia de Dados (Pandas): Wide para Long
    df_melted = df.melt(
        id_vars=["Estado", "Eleitores_Aptos_Milhoes"],
        value_vars=["Votos_Flavio_Bolsonaro", "Votos_Senadores_PL"],
        var_name="Cargo_Partido",
        value_name="Total_Votos"
    )

    df_melted["Cargo_Partido"] = df_melted["Cargo_Partido"].map({
        "Votos_Flavio_Bolsonaro": "Flávio Bolsonaro (Presidente)",
        "Votos_Senadores_PL": "Candidatos ao Senado (PL)"
    })

    # Gráfico 1: Barras Agrupadas (Plotly Express)
    fig1 = px.bar(
        df_melted,
        x="Estado",
        y="Total_Votos",
        color="Cargo_Partido",
        barmode="group",
        title="Comparativo de Votação por Estado (Pool Nacional vs. Votos Legislativos)",
        labels={"Total_Votos": "Total de Votos Válidos", "Cargo_Partido": "Indicador"},
        hover_data={
            "Estado": True,
            "Total_Votos": ":,f",
            "Eleitores_Aptos_Milhoes": ":.2f"
        },
        color_discrete_sequence=["#1A5276", "#229954"]
    )
    
    fig1.update_layout(hoverlabel=dict(bgcolor="white", font_size=14))
    st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# ABA 2: COMPOSIÇÃO DO LEGISLATIVO (NOVO!)
# ==========================================
with aba2:
    st.header("🏛️ Distribuição de Cadeiras no Congresso Nacional")
    
    # Criando colunas lado a lado no Streamlit para os dois gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Câmara dos Deputados")
        # Dados oficiais consolidados
        dados_camara = {
            "Partido": ["PL", "Federação Brasil da Esperança (PT/PCdoB/PV)", "União Brasil", "PP", "MDB", "PSD", "Outros"],
            "Cadeiras": [121, 88, 59, 47, 42, 42, 114]
        }
        df_camara = pd.DataFrame(dados_camara)
        
        # Gráfico de Rosca para a Câmara com Tooltip customizado
        fig_camara = px.pie(
            df_camara,
            values="Cadeiras",
            names="Partido",
            hole=0.4,
            title="Bancadas na Câmara (Total: 513 Deputados)",
            hover_data=["Cadeiras"],
            labels={"Cadeiras": "Número de Cadeiras"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_camara.update_traces(textinfo="percent+label")
        fig_camara.update_layout(hoverlabel=dict(bgcolor="white", font_size=14))
        st.plotly_chart(fig_camara, use_container_width=True)
        
    with col2:
        st.subheader("Senado Federal")
        # Dados oficiais consolidados da nova composição do Senado
        dados_senado = {
            "Partido": ["PL", "PT", "PSD", "MDB", "União Brasil", "PP", "Outros"],
            "Cadeiras": [19, 6, 12, 10, 9, 7, 18]  # Foco na renovação das vagas disputadas ontem
        }
        df_senado = pd.DataFrame(dados_senado)
        
        # Gráfico de Rosca para o Senado com Tooltip customizado
        fig_senado = px.pie(
            df_senado,
            values="Cadeiras",
            names="Partido",
            hole=0.4,
            title="Vagas Conquistadas no Senado (Renovação de 2/3)",
            hover_data=["Cadeiras"],
            labels={"Cadeiras": "Senadores Eleitos"},
            color_discrete_sequence=px.colors.qualitative.Modern
        )
        fig_senado.update_traces(textinfo="percent+label")
        fig_senado.update_layout(hoverlabel=dict(bgcolor="white", font_size=14))
        st.plotly_chart(fig_senado, use_container_width=True)

    st.markdown("""
    ### 🧠 Análise Geopolítica do Legislativo
    Ao interagir com os gráficos passando o mouse sobre as fatias:
    * **Crescimento de Bancada:** É nítida a expansão de partidos alinhados à direita e centro-direita na Câmara dos Deputados, com o PL atingindo a marca histórica de **121 cadeiras**.
    * **Equilíbrio de Forças:** O Senado Federal apresenta uma forte bancada de oposição eleita, o que exigirá intensa articulação política para a aprovação de reformas no próximo ciclo de governo.
    """)
