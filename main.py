import streamlit as st
import pandas as pd

def calc_general_stats(df):

    df_data = df.groupby(by = "Data")[["Valor"]].sum()
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["Diferença Mensal Abs."] = df_data["Valor"] - df_data["lag_1"]
    df_data["Média 6M Diferença Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(6).mean()
    df_data["Média 12M Difereça Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(12).mean()
    df_data["Média 24M Difereça Mensal Abs."] = df_data["Diferença Mensal Abs."].rolling(24).mean()
    df_data["Diferença Mensal Rel."] = df_data["Valor"] / df_data["lag_1"] - 1
    df_data["Evolução 6M  total"] = df_data["Valor"].rolling(6).apply(lambda x: x.iloc[-1] - x.iloc[0]) 
    df_data["Evolução 12M  total"] = df_data["Valor"].rolling(12).apply(lambda x: x.iloc[-1] - x.iloc[0])
    df_data["Evolução 24M  total"] = df_data["Valor"].rolling(24).apply(lambda x: x.iloc[-1] - x.iloc[0])
    df_data["Evolução 6M  Rel."] = df_data["Valor"].rolling(6).apply(lambda x: x.iloc[-1] / x.iloc[0]- 1) 
    df_data["Evolução 12M  Rel."] = df_data["Valor"].rolling(12).apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)
    df_data["Evolução 24M  Rel."] = df_data["Valor"].rolling(24).apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)

    df_data = df_data.drop("lag_1", axis=1)
    return df_data

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

    ##################
    ###DadosBrutos####
    ##################

    exp1 = st.expander("Dados Brutos")
    columns_fmt = {"Valor":st.column_config.NumberColumn("valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    ###################
    ###Instiruições####
    ###################

    exp2 = st.expander("Instituições")
    df_instiuicao = df.pivot_table(index="Data", columns="Instituição", values= "Valor")

    tab_data, tab_history, tb_share = exp2.tabs(["Dados", "Historicos", "Distribuição"])
    
    with tab_data:
        st.dataframe(df_instiuicao)

    with tab_history:
        st.line_chart(df_instiuicao)

    with tb_share:
        
        date = st.selectbox("Filtro Data", options=df_instiuicao.index)

        ###Grafico###
        ## obtem ultima data de dados##
        st.bar_chart(df_instiuicao.loc[date])

    #########################
    ###estatiticas gerais###
    ########################

    exp3 = st.expander("Estátisticas Gerais")

    df_stats = calc_general_stats(df)

    columns_config = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Diferença Mensal Abs.": st.column_config.NumberColumn("Diferença Mensal Abs.", format="R$ %.2f"),
        "Média 6M Diferença Mensal Abs.": st.column_config.NumberColumn("Média 6M Diferença Mensal Abs.", format="R$ %.2f"),
        "Média 12M Difereça Mensal Abs.": st.column_config.NumberColumn("Média 12M Difereça Mensal Abs.", format="R$ %.2f"),
        "Média 24M Difereça Mensal Abs.": st.column_config.NumberColumn("Média 24M Difereça Mensal Abs.", format="R$ %.2f"),
        "Evolução 6M  total": st.column_config.NumberColumn("Evolução 6M  total", format="R$ %.2f"),
        "Evolução 12M  total": st.column_config.NumberColumn("Evolução 12M  total", format="R$ %.2f"),
        "Evolução 24M  total": st.column_config.NumberColumn("Evolução 24M  total", format="R$ %.2f"),
        "Diferença Mensal Rel.": st.column_config.NumberColumn("Diferença Mensal Rel.", format="percent"),
        "Evolução 6M  Rel.": st.column_config.NumberColumn("Evolução 6M  Rel.", format="percent"),
        "Evolução 12M  Rel.": st.column_config.NumberColumn("Evolução 12M  Rel.", format="percent"),
        "Evolução 24M  Rel.": st.column_config.NumberColumn("Evolução 24M  Rel.", format="percent"),
    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Historico de Evolução", "Crescimento Relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config= columns_config)

    with tab_abs:
        abs_cols = [ "Diferença Mensal Abs.",
        "Média 6M Diferença Mensal Abs.",
        "Média 12M Difereça Mensal Abs.",
        "Média 24M Difereça Mensal Abs.",]
        st.line_chart(df_stats[abs_cols])

    with tab_rel:
        rel_cols = [ 
            "Diferença Mensal Rel.",
            "Evolução 6M  Rel.",
            "Evolução 12M  Rel.",
            "Evolução 24M  Rel.",
        ]
        st.line_chart(df_stats[rel_cols])