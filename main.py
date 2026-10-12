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

    ##formatacao da coluna valor
    columns_fmt = {"Valor":st.column_config.NumberColumn("valor", format="R$ %f")}

    ##exibicao de dados
    st.dataframe(df, hide_index=True, column_config=columns_fmt)