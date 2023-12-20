# Análise Financeira

Criar uma dashboard de análise financeira mensal

| :books: Vitrine.Dev |     |
| -------------  | --- |
| :sparkles: Nome        | **Análise Financeira**
| :label: Tecnologias | Python, streamlit, pandas, pyplot
| :rocket: URL         | ledsouza-dashboard-financeiro.streamlit.app

<!-- Inserir imagem com a #vitrinedev ao final do link -->
![](https://vitrinedev.s3.amazonaws.com/Analise_Financeira.png#vitrinedev)

## Detalhes do projeto

Este código Python utiliza as bibliotecas pandas, plotly.express, e streamlit para realizar uma análise financeira mensal. A análise é baseada em dados de gastos mensais armazenados em uma planilha do Google Sheets. O código extrai os dados da planilha, realiza cálculos estatísticos e gera visualizações interativas para apresentar as informações financeiras de maneira clara.

1. **Configuração da Página:**
   - `st.set_page_config`: Configuração do título, layout e ícone da página do Streamlit para "Análise Financeira Mensal", centrado e com o ícone do dólar.

2. **Carregamento dos Dados:**
   - Definição dos meses em uma tupla chamada `months`.
   - Utilização de `st.selectbox` para permitir a escolha de um mês.
   - Construção do URL da planilha do Google Sheets com base no ID da planilha e mês selecionado.
   - Leitura dos dados da planilha usando Pandas, pulando as duas primeiras linhas e selecionando apenas as colunas de 10 a 13.

3. **Análise de Gastos:**
   - Agrupamento do DataFrame pelos valores das colunas 'Valor' e 'Categoria', somando os valores.
   - Classificação desses valores por categoria em ordem decrescente.

4. **Análise de Proporção de Gastos:**
   - Definição de um valor disponível para gastos mensais.
   - Cálculo dos custos fixos e de lazer.
   - Cálculo da proporção desses custos em relação ao valor disponível.
   - Cálculo do valor economizado em relação ao valor disponível.

5. **Apresentação das Métricas:**
   - Uso do `st.metric` para apresentar três métricas: Valor Economizado, Proporção de Custos Fixos e Proporção de Custos de Lazer.

6. **Gráfico de Barras:**
   - Utilização do Plotly Express para criar um gráfico de barras mostrando o valor total por categoria.
   - Ocultação da legenda e utilização das cores da sequência '#3498DB'.
   - Apresentação do gráfico usando `st.plotly_chart`.

7. **Métricas dos Custos Médios:**
   - Filtragem do DataFrame para excluir linhas que contenham as palavras 'Uber' ou '99POP' e que tenham valores entre 15 e 25.
   - Cálculo da média dos custos para subcategorias relevantes.
   - Apresentação das médias formatadas em uma tabela.

8. **Tabelas e Imagem:**
   - Uso de duas colunas do Streamlit para apresentar duas tabelas: a tabela completa de dados e a tabela de custo médio por subcategoria.
   - Adição de uma imagem chamada 'Spending_Plan.png' à segunda coluna.
