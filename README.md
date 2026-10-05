# 🗳️ Painel de Análise Eleitoral 2026: Presidente vs. Senado

Este projeto consiste em um dashboard interativo desenvolvido para analisar e correlacionar os dados oficiais do primeiro turno das Eleições Gerais de 2026 (ocorridas em 4 de outubro de 2026). O objetivo principal é avaliar a taxa de fidelidade partidária vertical e investigar os fatores matemáticos (como o voto duplo) que causam discrepâncias entre as votações majoritárias para o Executivo e o Legislativo.

O projeto foi construído utilizando práticas modernas de engenharia de dados, tratamento de dados em memória e renderização de componentes visuais avançados.

## 🚀 Tecnologias Utilizadas

*   **Python 3.10+** (Linguagem core)
*   **Pandas** (Engenharia de dados, manipulação e transformação de DataFrames)
*   **Plotly Express** (Renderização de gráficos interativos com recursos avançados de *Tooltip/Hover*)
*   **Streamlit** (Framework de aplicação web para servir o dashboard de forma ágil)

## 📁 Estrutura do Repositório

```text
eleicoes-dashboard-2026/
├── dados/
│   └── eleicao_2026.csv   # Base de dados estruturada das eleições
├── app.py                 # Arquivo principal da aplicação web (Streamlit)
├── requirements.txt       # Arquivo de dependências do ecossistema Python
└── README.md              # Documentação técnica do projeto
```

## 🔧 Instruções de Instalação e Execução

Siga os passos abaixo para clonar o repositório, instalar as dependências e rodar a aplicação em seu ambiente local:

### 1. Clonar o Repositório
```bash
git clone https://github.com
cd eleicoes-dashboard-2026
```

### 2. Instalar as Dependências
Certifique-se de ter o gerenciador de pacotes `pip` atualizado e execute a instalação em lote:
```bash
pip install -r requirements.txt
```

### 3. Executar o Dashboard
Para rodar a aplicação localmente através do Streamlit, utilize o comando:
```bash
streamlit run app.py
```
O navegador abrirá automaticamente o painel no endereço local `http://localhost:8501`.

## 🧠 Desafios Técnicos e Implementações
*   **Mapeamento de Tooltips:** Configuração cirúrgica do dicionário `hover_data` do Plotly Express para enriquecer a experiência do usuário final, exibindo detalhes demográficos do eleitorado de cada estado ao passar o mouse.
*   **Data Melting:** Transformação de dados de formato largo (*wide*) para formato longo (*long*) via Pandas para otimizar o agrupamento de barras do gráfico sem duplicar registros no banco.

---
Desenvolvido por **Rogério Sá de Macedo** — Portfólio de Ciência de Dados & Engenharia de IA.
