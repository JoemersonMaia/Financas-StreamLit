import streamlit as st
import pandas as pd
st.set_page_config(page_title="finanças", page_icon="💰")

st.markdown("""
# Boas vindas!

## Nosso App Financeiro

Espero que vc curta a experiência da nossa solução para organização financeira.

""")

## Widget de upload de dados
file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=["csv"])

## verifica se algum arquivo foi feito upload
if file_upload:

    ##leitura dos dados
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format = "%d/%m/%Y").dt.date
    
    ##formatacao da coluna valor e exibicaod de dados
    exp1 = st.expander("Dados Brutos")
    columns_fmt = {"Valor":st.column_config.NumberColumn("valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    ##Visão Instituição
    exp2 = st.expander("Instituições")
    df_instiuicao = df.pivot_table(index="Data", columns="Instituição", values= "Valor")

    tab_data, tab_history, tb_share = exp2.tabs(["Dados", "Historicos", "Distribuição"])
    
    with tab_data:
        st.dataframe(df_instiuicao)

    with tab_history:
        st.line_chart(df_instiuicao)

    with tb_share:
        
        date = st.selectbox("Filtro Data", options=df_instiuicao.index)
        
        ## obtem ultima data de dados
        st.bar_chart(df_instiuicao.loc[date])
    
