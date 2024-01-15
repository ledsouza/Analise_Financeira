"""
Este script cria um painel do Streamlit para análise financeira mensal.
Ele carrega dados de uma planilha do Google, realiza análises nos dados e visualiza os resultados.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(page_title='Análise Financeira Mensal', layout='wide', page_icon="heavy_dollar_sign")

# Carregamento dos dados
months = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
years = {'2023': '1quM2SQCyXHGd5zPc3y46FYjql_VoOQUqqwRtF9Ws0Xg', '2024': '1M-UIHenSns7o_iSTODK047YOO3Hh-nLS9DLaLvmwU7g'}

default_year = tuple(years.keys()).index(str(datetime.now().year))
year = st.sidebar.selectbox('Ano', tuple(years.keys()), index=default_year)
sheet_id = years[year]

default_month = datetime.now().month - 1
sheet_name = st.sidebar.selectbox('Mês', months, index=default_month)

url = f'https://docs.google.com/spreadsheet/ccc?key={sheet_id}&output=xlsx'
df = pd.read_excel(url, sheet_name=sheet_name, header=2).iloc[:, 10:14]
planejado_real = pd.read_excel(url, sheet_name=sheet_name, header=2).iloc[0:7, 0:3]
planejado_real.set_index(planejado_real.columns[0], inplace=True)
planejado_real.index.name = 'Categorias'

total_categoria = df[['Valor', 'Categoria']].groupby('Categoria')
total_categoria = total_categoria.sum().sort_values('Valor', ascending=False)

total_categoria['Proporcao'] = total_categoria['Valor'] / total_categoria['Valor'].sum() * 100

# Análise da proporção de gastos
valor_disponivel = 3649.92
categorias = set(total_categoria.index)
categoria_lazer = set(['Pessoal']) & categorias
categorias_fixas = categorias - categoria_lazer
custos_fixos = total_categoria.loc[list(categorias_fixas)].sum()
proporcao_custos_fixos = (custos_fixos/valor_disponivel).values[0]*100
custos_lazer = total_categoria.loc[list(categoria_lazer)].sum().values[0]
proporcao_custos_lazer = (custos_lazer/valor_disponivel)*100
guardar = valor_disponivel - (custos_fixos + custos_lazer).values[0]
economizado = ((guardar/valor_disponivel)*100)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.4, 0.4, 2])  # Ajustar larguras das colunas

with col1:
    st.metric('Valor economizado', f'{economizado:.2f}%'.replace('.', ','))

with col2:
    st.metric('Custos fixos', f'{proporcao_custos_fixos:.2f}%'.replace('.', ','))

with col3:
    st.metric('Custos de lazer', f'{proporcao_custos_lazer:.2f}%'.replace('.', ','))

st.markdown("<br>", unsafe_allow_html=True)

# Plot do gráfico de barras das categorias de custos
fig = px.bar(total_categoria.reset_index(), 
             x='Categoria', 
             y='Valor', 
             title='Valor total por categoria', 
             labels={'Categoria': '', 'Valor': 'Valor total (R$)'},
             text_auto=True, 
             color='Categoria', 
             color_discrete_sequence=['#3498DB'])

# Ajuste no display de informações
fig.update_traces(texttemplate='R$ %{y:.0f}', 
                  textposition='outside',
                  hoverinfo='skip', 
                  hovertemplate=None)
fig.update_layout(showlegend=False, yaxis=dict(title='', tickvals=[]))

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown("<div style='margin-top: 35px;'><b>Planejado vs Realizado<br></div><br>", unsafe_allow_html=True)
    
    def highlight_red(row):
        if row['Realizado'] > row['Planejado']:
            return ['', 'color: red']
        elif int(row['Realizado']) == int(row['Planejado']):
            return [''] * len(row)
        else:
            return ['', 'color: green']

    planejado_real.rename(columns={'Real': 'Realizado'}, inplace=True)
    styled_planejado_real = planejado_real.style.apply(highlight_red, axis=1)
    styled_planejado_real = styled_planejado_real.format({'Planejado': 'R$ {:.0f}', 'Realizado': 'R$ {:.0f}'}, decimal=',')
    st.dataframe(styled_planejado_real, use_container_width=True)

# Métricas dos custos médios para subcategorias relevantes
mask = ((df['Descrição'] == 'Uber') | (df['Descrição'] == '99POP')) & ((df['Valor'] > 25) | (df['Valor'] < 14))
df_transporte_trabalho = df[~mask]
media_categoria = df_transporte_trabalho[['Valor', 'Descrição']].groupby('Descrição').mean()
categorias_desejadas = ['Almoço', 'Jantar', 'Café', '99POP', 'Uber']
categorias_presentes = media_categoria.index.isin(categorias_desejadas)
media_categoria = media_categoria[categorias_presentes].T.style.format('R$ {:.2f}', decimal=',')

table1, table2 = st.columns(2)
with table1:
    st.markdown('<b>Tabela de dados completa', unsafe_allow_html=True)
    st.dataframe(df[['Valor', 'Descrição', 'Categoria']].style.format({'Valor': 'R$ {:.2f}'}, decimal=','),
                 use_container_width=True,
                 hide_index=True,
                 height=750)
with table2:
    st.markdown('<b>Custo médio por subcategoria', unsafe_allow_html=True)
    st.dataframe(media_categoria, use_container_width=True)
    st.image('Spending_Plan.png')
