# %%
import requests
import streamlit as st
import pandas as pd
import datetime

def get_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"

    params = {
        "formato": "json",
        "dataInicial": "01/01/2020",
        "dataFinal": "31/12/2025"
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    df = pd.DataFrame(resp.json())

    df["data"] = pd.to_datetime(df["data"], dayfirst=True).dt.date
    df["valor"] = pd.to_numeric(df["valor"])

    return df

## funcao estatiticas do dado brutos ##
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

def main_metas():
            ##colunas##
            col1, col2 = st.columns(2)

            ##Inico Meta e Salario liquido
            data_inicio_meta = col1.date_input("Inico da Meta", max_value=df_stats.index.max())
            data_filtrada = df_stats.index[df_stats.index <= data_inicio_meta][-1]
            salario_liq = col2.number_input("Sálario Liquido", min_value=0., format = "%.2f")

            ##Salario Bruto e Custos Fixos
            salario_bruto =col1.number_input("Sálario Bruto", min_value=0., format = "%.2f")
            custo_fixo = col2.number_input("Custo Fixos", min_value=0., format = "%.2f")

            ##patrimcio inicio meta
            valor_inicio = df_stats.loc[data_filtrada]["Valor"]
            col1.markdown(f"**Patrimonio no ínicio da Meta**: R$ {valor_inicio : .2f}")


            selic_gov_df = get_selic()

            filter_selic_date = selic_gov_df["data"] <= data_inicio_meta

            selic_default = selic_gov_df.loc[filter_selic_date, "valor"].iloc[-1]

            selic = st.number_input(
                "Selic",
                min_value=0.0,
                value=float(selic_default),
                format="%.2f"
            )

            selic_ano = selic / 100
            selic_mes = (selic_ano + 1) ** (1/12) - 1

            redimento_ano = valor_inicio * selic_ano
            redimento_mes = valor_inicio * selic_mes
                                                                                                                                                                                        
            ##coluna pontecial, mas resete de coluna
            col1_pot, col2_pot = st.columns(2)

            ##conta arrrencadacao mensal e anual
            mensal = salario_liq - custo_fixo + redimento_mes
            anual = 2 * (salario_liq -custo_fixo) + redimento_ano

            ## contanier + Input do valor
            with col1_pot.container(border=True):
                st.markdown(f"""**Pontencial Arrecadação Mês**:\n\n R$ {mensal : .2f}""",
                            help = f"{salario_liq : .2f} + (-{custo_fixo : .2f}) + {redimento_mes :.2f}")

            with col2_pot.container(border=True):
                st.markdown(f"""**Pontencial Arrecadação Ano**:\n\n R$ {anual : .2f}""",
                            help = f"12 * ({salario_liq : .2f} + (-{custo_fixo : .2f})) + {redimento_ano :.2f}")

            ## contanier meta e patrimonio juntos
            with st.container(border=True):
                col1_meta, col2_meta = st.columns(2)
                with col1_meta:
                    meta_estipulada = st.number_input("Meta Estipulada", min_value=-99999999999999999999999999990., format="%.2f", value=anual)

                with col2_meta:
                    patrimonio_final = meta_estipulada + valor_inicio
                    st.markdown(f"Patrimônio Estimado pós meta:\n\n R$ {patrimonio_final : .2f}")
            return data_inicio_meta, valor_inicio, meta_estipulada, patrimonio_final
 


## alteracao do nick name da pagina ##
st.set_page_config(page_title="finanças", page_icon="💰")

## texto ##
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

    ##grafico em linha ##
    with tab_history:
        st.line_chart(df_instiuicao)

    with tb_share:

        ## filtro por data ##
        date = st.selectbox("Filtro Data", options=df_instiuicao.index)

        ###Grafico###
        ## obtem ultima data de dados##
        st.bar_chart(df_instiuicao.loc[date])

    #########################
    ###estatiticas gerais###
    ########################

    exp3 = st.expander("Estátisticas Gerais")

    df_stats = calc_general_stats(df)

    ## Calma, nao se assusta, Formatacao dos valores das estatiticas
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

    ##abas, dentro do expander##
    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Historico de Evolução", "Crescimento Relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config= columns_config)

    ##grafico em linha##
    with tab_abs:
        abs_cols = [ "Diferença Mensal Abs.",
        "Média 6M Diferença Mensal Abs.",
        "Média 12M Difereça Mensal Abs.",
        "Média 24M Difereça Mensal Abs.",]
        st.line_chart(df_stats[abs_cols])

    ## grafico em linha ##
    with tab_rel:
        rel_cols = [ 
            "Diferença Mensal Rel.",
            "Evolução 6M  Rel.",
            "Evolução 12M  Rel.",
            "Evolução 24M  Rel.",
        ]
        st.line_chart(df_stats[rel_cols])

    ############
    ###Metas####
    ############

    with st.expander("Metas"):
        tab_main, tab_date_meta, tab_graph = st.tabs(tabs=["Configuração", "Dados", "Graficos"])

        with tab_main:
            data_inicio_meta, valor_inicio, meta_estipulada, patrimonio_final = main_metas()

        with tab_date_meta:
            meses = pd.DataFrame({
                                "Data Referencia":[(data_inicio_meta + pd.DateOffset(months=i)) for i in range(1,13)],
                                "Meta Mensal" : [valor_inicio+ round(meta_estipulada/12, 2) * i for i in range(1, 13)],
                                })
            
            meses["Data Referencia"] = meses["Data Referencia"].dt.strftime("%Y-%m")
            df_patrimonio = df_stats.reset_index()[["Data", "Valor"]]
            df_patrimonio["Data Referencia"] = pd.to_datetime(df_patrimonio["Data"]).dt.strftime("%Y-%m")
            meses = meses.merge(df_patrimonio, how = "left", on= "Data Referencia")

            meses = meses[["Data Referencia", "Meta Mensal", "Valor",]]
            meses["Atigimento (%)"]= meses["Valor"] / meses["Meta Mensal"]
            meses["Atigimento Ano"] = meses["Valor"] / patrimonio_final
            meses = meses.set_index("Data Referencia")
            meses["Atigimento Esperado"] = meses["Meta Mensal"] / patrimonio_final
        

            columns_config_meses = {
                    "Meta Mensal": st.column_config.NumberColumn("Meta Mensal", format="R$ %.2f"),
                    "Valor": st.column_config.NumberColumn("Valor Antigindo", format="R$ %.2f"),
                    "Atigimento (%)": st.column_config.NumberColumn("Atigimento (%)", format="percent"),
                    "Atigimento Ano": st.column_config.NumberColumn("Atigimento Ano", format="percent"),
                    "Atigimento Esperado": st.column_config.NumberColumn("Atigimento Esperado", format="percent"),
                }

            st.dataframe(meses, column_config=columns_config_meses)

        with tab_graph:
            st.line_chart(meses[["Atigimento Ano", "Atigimento Esperado"]])