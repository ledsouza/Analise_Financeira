import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = 'Análise Financeira Mensal', layout = 'centered', page_icon = "heavy_dollar_sign")

# Carregamento dos dados
months = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
sheet_name = st.selectbox('Mês', months)
sheet_id = '1quM2SQCyXHGd5zPc3y46FYjql_VoOQUqqwRtF9Ws0Xg'
url = f'https://docs.google.com/spreadsheet/ccc?key={sheet_id}&output=xlsx'
df = pd.read_excel(url, sheet_name=sheet_name, header=2).iloc[:, 10:14]

# Plot do gráfico de barras das categorias de custos
total_categoria = df[['Valor', 'Categoria']].groupby('Categoria')
total_categoria = total_categoria.sum().sort_values('Valor', ascending=False)

fig = px.bar(total_categoria.reset_index(), x='Categoria', y='Valor', title = 'Valor total por categoria', 
             labels={'Categoria': '', 'Valor': 'Valor total (R$)'}, color = 'Categoria', color_discrete_sequence=['#3498DB'])
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Análise da proporção de gastos
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
    st.metric('Valor economizado', f'{economizado:.2f}%'.replace('.', ','))
with col2:
    st.metric('Custos fixos', f'{(custos_fixos/valor_disponivel).values[0]*100:.2f}%'.replace('.', ','))
with col3:
    st.metric('Custos de lazer', f'{(custos_lazer/valor_disponivel)*100:.2f}%'.replace('.', ','))

# Métricas dos custos médios para subcategorias relevantes
mask = ((df['Descrição'] == 'Uber') | (df['Descrição'] == '99POP')) & ((df['Valor'] > 25) | (df['Valor'] < 15))
df_transporte_trabalho = df[~mask]
media_categoria = df_transporte_trabalho[['Valor', 'Descrição']].groupby('Descrição').mean()
categorias_desejadas = ['Almoço', 'Jantar', 'Café', '99POP', 'Uber']
categorias_presentes = media_categoria.index.isin(categorias_desejadas)
media_categoria = media_categoria[categorias_presentes].T.style.format('R${:.2f}', decimal= ',')

table1, table2 = st.columns(2)
with table1:
    'Tabela de dados completa'
    st.dataframe(df[['Valor', 'Descrição', 'Categoria']].style.format({'Valor': 'R${:.2f}'}, decimal = ','), use_container_width = True, hide_index = True)
with table2:
    'Custo médio por subcategoria'
    st.dataframe(media_categoria, use_container_width = True)
    st.image('Spending_Plan.png')