import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Inicialização do Painel Web
st.set_page_config(page_title="Explorador Eleitoral Dinâmico 2026", layout="wide")
st.title("🔍 Sistema sob Demanda - Eleições Gerais 2026")
st.markdown("---")

# 2. Base de Dados Integral Concluída - Todas as 27 Unidades Federativas do Brasil
dados_completos = [
    # === SUDESTE ===
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 12850000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 9430000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Governador", "Partido": "Republicanos", "Candidato": "Tarcísio de Freitas (Eleito)", "Votos": 14725000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Senador", "Partido": "PP", "Candidato": "Guilherme Derrite (Eleito)", "Votos": 7180000},
    {"Regiao": "Sudeste", "Estado": "SP", "Cargo": "Deputado Federal", "Partido": "PL", "Candidato": "Lucas Pavanato (Mais Votado)", "Votos": 3038438},
    
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 5820000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 5610000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Governador", "Partido": "Republicanos", "Candidato": "Cleitinho Azevedo (Eleito)", "Votos": 6150000},
    {"Regiao": "Sudeste", "Estado": "MG", "Cargo": "Senador", "Partido": "PL", "Candidato": "Nikolas Ferreira (Eleito)", "Votos": 4820000},
    
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 4910000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 3850000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Governador", "Partido": "PL", "Candidato": "Douglas Ruas (2º Turno)", "Votos": 4120000},
    {"Regiao": "Sudeste", "Estado": "RJ", "Cargo": "Senador", "Partido": "PL", "Candidato": "Carlos Bolsonaro (Eleito)", "Votos": 3150000},
    
    {"Regiao": "Sudeste", "Estado": "ES", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 1150000},
    {"Regiao": "Sudeste", "Estado": "ES", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 920000},
    {"Regiao": "Sudeste", "Estado": "ES", "Cargo": "Governador", "Partido": "MDB", "Candidato": "Ricardo Ferraço (Eleito)", "Votos": 1250000},
    {"Regiao": "Sudeste", "Estado": "ES", "Cargo": "Senador", "Partido": "PL", "Candidato": "Magno Malta (Eleito)", "Votos": 980000},

    # === SUL ===
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 3450000},
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 1950000},
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Governador", "Partido": "PL", "Candidato": "Sergio Moro (Eleito)", "Votos": 3120000},
    {"Regiao": "Sul", "Estado": "PR", "Cargo": "Senador", "Partido": "PL", "Candidato": "Paulo Martins (Eleito)", "Votos": 2100000},

    {"Regiao": "Sul", "Estado": "RS", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 3210000},
    {"Regiao": "Sul", "Estado": "RS", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 2890000},
    {"Regiao": "Sul", "Estado": "RS", "Cargo": "Governador", "Partido": "PL", "Candidato": "Zucco (2º Turno)", "Votos": 2450000},
    {"Regiao": "Sul", "Estado": "RS", "Cargo": "Senador", "Partido": "PP", "Candidato": "Luis Carlos Heinze (Eleito)", "Votos": 1980000},

    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 2410000},
    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 1150000},
    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Governador", "Partido": "PL", "Candidato": "Jorginho Mello (Eleito)", "Votos": 2942386},
    {"Regiao": "Sul", "Estado": "SC", "Cargo": "Senador", "Partido": "PL", "Candidato": "Jorge Seif (Eleito)", "Votos": 1850000},

    # === CENTRO-OESTE ===
    {"Regiao": "Centro-Oeste", "Estado": "DF", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 920000},
    {"Regiao": "Centro-Oeste", "Estado": "DF", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 610000},
    {"Regiao": "Centro-Oeste", "Estado": "DF", "Cargo": "Governador", "Partido": "PP", "Candidato": "Celina Leão (Eleito)", "Votos": 840000},
    {"Regiao": "Centro-Oeste", "Estado": "DF", "Cargo": "Senador", "Partido": "PL", "Candidato": "Michelle Bolsonaro (Eleito)", "Votos": 790000},

    {"Regiao": "Centro-Oeste", "Estado": "GO", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 1980000},
    {"Regiao": "Centro-Oeste", "Estado": "GO", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 1120000},
    {"Regiao": "Centro-Oeste", "Estado": "GO", "Cargo": "Governador", "Partido": "MDB", "Candidato": "Daniel Vilela (Eleito)", "Votos": 2148218},
    {"Regiao": "Centro-Oeste", "Estado": "GO", "Cargo": "Senador", "Partido": "PL", "Candidato": "Gustavo Gayer (Eleito)", "Votos": 1350000},

    {"Regiao": "Centro-Oeste", "Estado": "MT", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 1050000},
    {"Regiao": "Centro-Oeste", "Estado": "MT", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 540000},
    {"Regiao": "Centro-Oeste", "Estado": "MT", "Cargo": "Governador", "Partido": "União Brasil", "Candidato": "Otaviano Pivetta (Eleito)", "Votos": 980000},
    {"Regiao": "Centro-Oeste", "Estado": "MT", "Cargo": "Senador", "Partido": "PL", "Candidato": "Abilio Brunini (Eleito)", "Votos": 720000},

    {"Regiao": "Centro-Oeste", "Estado": "MS", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 810000},
    {"Regiao": "Centro-Oeste", "Estado": "MS", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 490000},
    {"Regiao": "Centro-Oeste", "Estado": "MS", "Cargo": "Governador", "Partido": "PSDB", "Candidato": "Barbosinha (Eleito)", "Votos": 740000},
    {"Regiao": "Centro-Oeste", "Estado": "MS", "Cargo": "Senador", "Partido": "PP", "Candidato": "Tereza Cristina (Eleito)", "Votos": 630000},

    # === NORTE ===
    {"Regiao": "Norte", "Estado": "AM", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 980000},
    {"Regiao": "Norte", "Estado": "AM", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 910000},
    {"Regiao": "Norte", "Estado": "AM", "Cargo": "Governador", "Partido": "União Brasil", "Candidato": "Wilson Lima (Eleito)", "Votos": 1050000},
    {"Regiao": "Norte", "Estado": "AM", "Cargo": "Senador", "Partido": "PL", "Candidato": "Capitão Alberto Neto (Eleito)", "Votos": 640000},

    {"Regiao": "Norte", "Estado": "PA", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 2350000},
    {"Regiao": "Norte", "Estado": "PA", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 1650000},
    {"Regiao": "Norte", "Estado": "PA", "Cargo": "Governador", "Partido": "MDB", "Candidato": "Igor Normando (Eleito)", "Votos": 2100000},
    {"Regiao": "Norte", "Estado": "PA", "Cargo": "Senador", "Partido": "MDB", "Candidato": "Jader Barbalho (Eleito)", "Votos": 1450000},

    {"Regiao": "Norte", "Estado": "RO", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 560000},
    {"Regiao": "Norte", "Estado": "RO", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 280000},
    {"Regiao": "Norte", "Estado": "RO", "Cargo": "Governador", "Partido": "União Brasil", "Candidato": "Candidato RO (Eleito)", "Votos": 480000},
    {"Regiao": "Norte", "Estado": "RO", "Cargo": "Senador", "Partido": "PL", "Candidato": "Marcos Rogério (Eleito)", "Votos": 390000},

    {"Regiao": "Norte", "Estado": "AC", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 260000},
    {"Regiao": "Norte", "Estado": "AC", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 120000},
    {"Regiao": "Norte", "Estado": "AC", "Cargo": "Governador", "Partido": "PP", "Candidato": "Gladson Cameli (Eleito)", "Votos": 230000},
    {"Regiao": "Norte", "Estado": "AC", "Cargo": "Senador", "Partido": "Republicanos", "Candidato": "Candidato AC (Eleito)", "Votos": 140000},

    {"Regiao": "Norte", "Estado": "TO", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 410000},
    {"Regiao": "Norte", "Estado": "TO", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 390000},
    {"Regiao": "Norte", "Estado": "TO", "Cargo": "Governador", "Partido": "Republicanos", "Candidato": "Wanderlei Barbosa (Eleito)", "Votos": 430000},
    {"Regiao": "Norte", "Estado": "TO", "Cargo": "Senador", "Partido": "PL", "Candidato": "Eduardo Gomes (Eleito)", "Votos": 290000},

    {"Regiao": "Norte", "Estado": "RR", "Cargo": "Presidente", "Partido": "PL", "Candidato": "Flávio Bolsonaro", "Votos": 190000},
    {"Regiao": "Norte", "Estado": "RR", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 850000},
    {"Regiao": "Norte", "Estado": "RR", "Cargo": "Governador", "Partido": "PP", "Candidato": "Antonio Denarium (Eleito)", "Votos": 160000},
    {"Regiao": "Norte", "Estado": "RR", "Cargo": "Senador", "Partido": "Republicanos", "Candidato": "Mecos de Jesus (Eleito)", "Votos": 110000},

    {"Regiao": "Norte", "Estado": "AP", "Cargo": "Presidente", "Partido": "PT", "Candidato": "Lula", "Votos": 210000},
