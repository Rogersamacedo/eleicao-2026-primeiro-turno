import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuração da página do Streamlit
st.set_page_config(page_title="Análise Eleitoral 2026", layout="wide")
st.title("🗳️ Análise de Fidelidade Partidária: Presidente vs. Senado (PL)")

# 2. Carregar a base de dados que geramos no passo anterior
try:
    df = pd.read_csv("dados/eleicao_2026.csv")
except FileNotFoundError:
    st.error("Arquivo 'dados/eleicao_2026.csv' não encontrado. Certifique-se de rodar o script gerador primeiro!")
    st.stop()

# 3. Engenharia de Dados (Pandas): Preparando os dados para o gráfico de barras comparativas
# Vamos transformar as colunas de votos em formato longo (Melt) para facilitar a plotagem no Plotly
df_melted = df.melt(
    id_vars=["Estado", "Eleitores_Aptos_Milhoes"],
    value_vars=["Votos_Flavio_Bolsonaro", "Votos_Senadores_PL"],
    var_name="Cargo_Partido",
    value_name="Total_Votos"
)

# Ajustando os nomes para exibição na legenda
df_melted["Cargo_Partido"] = df_melted["Cargo_Partido"].map({
    "Votos_Flavio_Bolsonaro": "Flávio Bolsonaro (Presidente)",
    "Votos_Senadores_PL": "Candidatos ao Senado (PL)"
})

# 4. Criando o Gráfico Interativo com Plotly Express
# O parâmetro 'hover_data' customiza as informações que aparecem ao passar o mouse (Tooltip)
fig = px.bar(
    df_melted,
    x="Estado",
    y="Total_Votos",
    color="Cargo_Partido",
    barmode="group",
    title="Comparativo de Votação por Estado (Pool Nacional vs. Votos Legislativos)",
    labels={"Total_Votos": "Total de Votos Válidos", "Cargo_Partido": "Indicador"},
    hover_data={
        "Estado": True,
        "Total_Votos": ":,f",  # Formata o número com separador de milhar
        "Eleitores_Aptos_Milhoes": ":.2f"  # Mostra o total de eleitores do estado com 2 casas decimais
    },
    color_discrete_sequence=["#1A5276", "#229954"]  # Cores profissionais para o dashboard
)

# Ajustando o layout para o Tooltip e design ficar impecável
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial"
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# 5. Renderizar o gráfico interativo na tela do dashboard
st.plotly_chart(fig, use_container_width=True)

# 6. Adicionando a sua análise técnica abaixo do gráfico
st.markdown("""
### 🧠 Análise Técnica dos Dados
Como observado no gráfico interativo ao passar o mouse sobre as barras:
* **Fator Voto Duplo:** O volume total de votos para o Senado do partido frequentemente supera os votos do candidato à presidência em estados com alta fidelidade partidária porque cada cidadão vota em **dois senadores**.
* **Comportamento Regional:** O Tooltip revela o tamanho do colégio eleitoral de cada estado, permitindo correlacionar onde a estratégia de lançar duas candidaturas ao Senado funcionou para inflar a legenda.
""")
