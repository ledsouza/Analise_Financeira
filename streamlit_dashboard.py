import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st

st.set_page_config(page_title = 'Análise Financeira Mensal', layout = 'centered')

months = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
sheet_name = st.selectbox('Mês', months)
sheet_id = '1quM2SQCyXHGd5zPc3y46FYjql_VoOQUqqwRtF9Ws0Xg'
url = f'https://docs.google.com/spreadsheet/ccc?key={sheet_id}&output=xlsx'
df = pd.read_excel(url, sheet_name=sheet_name, header=2).iloc[:, 10:14]

total_categoria = df[['Valor', 'Categoria']].groupby('Categoria')
total_categoria = total_categoria.sum().sort_values('Valor', ascending=False)
ax = sns.barplot(data = total_categoria, x = 'Categoria', y = 'Valor')
ax.figure.set_size_inches(12,6)
ax.set_title('Valor total por categoria', loc='left', fontsize=18)
ax.set_xlabel('Categoria', fontsize=14)
ax.set_ylabel('Valor total (R$)', fontsize=14)
st.pyplot(ax.get_figure())

valor_disponivel = 3649.92
categorias = set(total_categoria.index)
categoria_lazer = set(['Pessoal']) & categorias
categorias_fixas = categorias - categoria_lazer
custos_fixos = total_categoria.loc[list(categorias_fixas)].sum()
custos_lazer = total_categoria.loc[list(categoria_lazer)].sum().values[0]
guardar = valor_disponivel - (custos_fixos + custos_lazer)
economizado = ((guardar/valor_disponivel)*100).values[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Valor economizado (%)', round(economizado, 2))
with col2:
    st.metric('Custos fixos (%)', round((custos_fixos/valor_disponivel).values[0]*100, 2))
with col3:
    st.metric('Custos de lazer (%)', round((custos_lazer/valor_disponivel)*100, 2))