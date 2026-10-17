# 💰 App Financeiro — Análise e Planejamento Patrimonial

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-dados-150458?logo=pandas&logoColor=white)
![API](https://img.shields.io/badge/API-Banco%20Central%20do%20Brasil-00529B)

Aplicação web desenvolvida em **Python** e **Streamlit** que transforma um simples arquivo CSV com saldos por instituição financeira em um painel de acompanhamento patrimonial: histórico, distribuição, estatísticas de evolução e planejamento de metas com base na taxa Selic.

---

## Sumário

- [Apresentação](#apresentação)
- [Demonstração](#demonstração)
- [Funcionalidades](#funcionalidades)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Como a aplicação funciona](#como-a-aplicação-funciona)
- [Análises e cálculos financeiros](#análises-e-cálculos-financeiros)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e execução local](#instalação-e-execução-local)
- [Formato dos dados](#formato-dos-dados)
- [Integração com a API do Banco Central](#integração-com-a-api-do-banco-central)
- [Limitações e considerações](#limitações-e-considerações)
- [Possíveis melhorias futuras](#possíveis-melhorias-futuras)
- [Aprendizados técnicos](#aprendizados-técnicos)

---

## Apresentação

Quem acompanha o próprio patrimônio costuma ter o dinheiro espalhado em várias instituições (bancos, corretoras, carteiras digitais) e registra os saldos em planilhas. Responder perguntas simples, como *"quanto meu patrimônio cresceu nos últimos 12 meses?"* ou *"estou no ritmo da minha meta?"*, exige cálculos manuais repetitivos.

Este projeto automatiza esse processo. O usuário faz o upload de um CSV com o histórico de saldos e a aplicação:

1. organiza os valores por instituição e por data;
2. calcula variações e médias móveis do patrimônio total;
3. permite definir uma meta de 12 meses e compará-la com a evolução real, usando a Selic como referência de rendimento.

Todo o código está em um único script Python, com interface interativa criada diretamente com os componentes do Streamlit.

---

## Demonstração

| Item | Link |
|------|------|
| Aplicação publicada | [finance-jjo.streamlit.app](https://finance-jjo.streamlit.app/) |

### Capturas de tela

**1. Tela inicial e upload do CSV**

![Tela inicial com o campo de upload](docs/img/01-tela-inicial.png)

**2. Seções liberadas após o upload**

![Seções Dados Brutos, Instituições, Estatísticas Gerais e Metas](docs/img/02-secoes.png)

**3. Dados brutos e análise por instituição**

![Dados brutos e tabela por instituição](docs/img/03-dados-instituicoes.png)

**4. Estatísticas gerais e configuração de metas**

![Crescimento relativo e configuração de metas](docs/img/04-estatisticas-metas.png)

> As capturas usam os dados fictícios do arquivo de modelo do repositório.

---

## Funcionalidades

### Importação e visualização dos dados
- Upload de arquivo `.csv` pelo componente `st.file_uploader`.
- Tabela com os **dados brutos** importados, com a coluna de valor formatada em reais.

### Análise por instituição
- Tabela dinâmica (pivot) com as datas nas linhas e as instituições nas colunas.
- **Gráfico de linhas** com o histórico de cada instituição.
- **Gráfico de barras** com a distribuição dos valores entre as instituições em uma data escolhida pelo usuário.

### Estatísticas gerais do patrimônio
- Patrimônio total por data (soma de todas as instituições).
- Diferença mensal absoluta e relativa.
- Médias móveis da diferença mensal absoluta (6, 12 e 24 períodos).
- Evolução total e relativa em janelas de 6, 12 e 24 períodos.
- Gráficos de linhas para a evolução absoluta e para o crescimento relativo.

### Planejamento de metas
- Entrada de data de início da meta, salário líquido, salário bruto e custos fixos.
- Patrimônio na data de início, obtido do próprio histórico importado.
- Selic sugerida automaticamente a partir da API do Banco Central (editável pelo usuário).
- Estimativa de potencial de arrecadação mensal e anual.
- Meta estipulada (valor inicial sugerido igual ao potencial anual, editável) e patrimônio estimado após a meta.
- Tabela de acompanhamento dos 12 meses seguintes, com meta mensal, valor atingido e percentuais de atingimento.
- Gráfico comparando o atingimento real com o atingimento esperado.

---

## Tecnologias utilizadas

### Linguagem e bibliotecas

| Tecnologia | Uso no projeto |
|------------|----------------|
| **Python** | Linguagem principal |
| **Streamlit** | Interface web: upload, expanders, abas, colunas, containers, tabelas e gráficos |
| **Pandas** | Leitura do CSV, `groupby`, `pivot_table`, `rolling`, `shift`, `merge` e formatação de datas |
| **Requests** | Chamada HTTP à API do Banco Central |

O módulo `datetime`, da biblioteca padrão do Python, é importado no código.

### Serviços externos

| Serviço | Uso no projeto |
|---------|----------------|
| **API de dados abertos do Banco Central do Brasil (SGS)** | Série histórica da taxa Selic (série 432) |

---

## Como a aplicação funciona

1. **Boas-vindas e upload** — a página exibe uma mensagem de boas-vindas e o campo de upload. Enquanto nenhum arquivo é enviado, nada mais é exibido.
2. **Leitura dos dados** — o CSV é lido com Pandas e a coluna `Data` é convertida usando o formato `dd/mm/aaaa`.
3. **Seção "Dados Brutos"** — tabela com o conteúdo importado.
4. **Seção "Instituições"** — três abas: *Dados* (tabela dinâmica), *Historicos* (gráfico de linhas) e *Distribuição* (gráfico de barras para a data selecionada).
5. **Seção "Estátisticas Gerais"** — três abas: *Dados* (tabela completa de métricas), *Historico de Evolução* (valores absolutos) e *Crescimento Relativo* (percentuais).
6. **Seção "Metas"** — três abas: *Configuração* (entradas e estimativas), *Dados* (tabela de acompanhamento mensal) e *Graficos* (atingimento real × esperado).

Os dados são processados em memória durante a sessão. O código não grava os arquivos enviados.

---

## Análises e cálculos financeiros

### Patrimônio total por data
Os valores de todas as instituições na mesma data são **somados** (`groupby("Data").sum()`).

### Variações mensais

| Métrica | Cálculo |
|---------|---------|
| Diferença Mensal Abs. | Valor atual − valor do período anterior |
| Diferença Mensal Rel. | Valor atual ÷ valor do período anterior − 1 |
| Média 6M / 12M / 24M da Diferença Mensal Abs. | Média móvel da diferença mensal absoluta em 6, 12 e 24 linhas |

### Evolução em janelas

| Métrica | Cálculo |
|---------|---------|
| Evolução 6M / 12M / 24M total | Último valor da janela − primeiro valor da janela |
| Evolução 6M / 12M / 24M Rel. | Último valor da janela ÷ primeiro valor da janela − 1 |

> As janelas são contadas em **linhas (períodos)** e não em calendário. O código foi pensado para dados mensais, então 6, 12 e 24 períodos equivalem a 6, 12 e 24 meses apenas se o CSV tiver um registro por mês. Uma janela de N períodos compara o primeiro e o último ponto, ou seja, cobre N − 1 intervalos.

### Planejamento de metas

1. **Patrimônio inicial**: valor total na última data do histórico menor ou igual à data de início escolhida.
2. **Selic**: último valor da série do Banco Central até a data de início da meta (pode ser alterado manualmente). O valor é tratado como taxa anual em %.
3. **Selic mensal equivalente**: `(1 + selic_ano) ^ (1/12) − 1`.
4. **Rendimento estimado**: patrimônio inicial × Selic anual (ano) e patrimônio inicial × Selic mensal equivalente (mês).
5. **Potencial de arrecadação mensal**: `salário líquido − custos fixos + rendimento mensal`.
6. **Potencial de arrecadação anual**: `2 × (salário líquido − custos fixos) + rendimento anual`, conforme implementado no código. Veja a observação em [Limitações](#limitações-e-considerações).
7. **Patrimônio estimado pós-meta**: `meta estipulada + patrimônio inicial`.

### Tabela de acompanhamento (12 meses)

| Coluna | Significado |
|--------|-------------|
| Meta Mensal | `patrimônio inicial + (meta ÷ 12, arredondada) × mês` |
| Valor (exibido como "Valor Antigindo") | Patrimônio real do mesmo ano-mês, se existir no CSV |
| Atigimento (%) | Valor real ÷ meta mensal |
| Atigimento Ano | Valor real ÷ patrimônio estimado pós-meta |
| Atigimento Esperado | Meta mensal ÷ patrimônio estimado pós-meta |

Os nomes das colunas aparecem com a grafia usada no código.

> As estimativas são cálculos simples a partir dos valores informados. **Não são garantia de rentabilidade** nem recomendação de investimento.

---

## Estrutura do projeto

```text
.
├── .vscode/
├── .gitignore
├── main.py                                            # aplicação Streamlit
├── requirements.txt                                   # dependências do projeto
├── Template Controle Financeiro - Saldo Mensal.csv    # arquivo de modelo para testar
└── README.md
```

O `main.py` contém:

| Elemento | Função |
|----------|--------|
| `get_selic()` | Consulta a série da Selic na API do Banco Central |
| `calc_general_stats(df)` | Calcula as estatísticas gerais do patrimônio |
| `main_metas()` | Monta a interface e os cálculos de planejamento de metas |

---

## Pré-requisitos

- Python 3
- `pip` ou Conda
- Bibliotecas: `streamlit`, `pandas`, `requests` (listadas no `requirements.txt`)
- Uma versão recente do Streamlit (o código usa `st.container(border=True)` e `format="percent"` em `NumberColumn`)
- Conexão com a internet para a consulta à Selic
- Um arquivo CSV no [formato esperado](#formato-dos-dados)

---

## Instalação e execução local

```bash
# 1. Clonar o repositório
git clone https://github.com/JoemersonMaia/Financas-StreamLit.git
cd Financas-StreamLit
```

**Opção A — virtualenv**

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Opção B — Conda**

```bash
conda create -n app-financeiro python=3
conda activate app-financeiro
pip install -r requirements.txt
```

**Executar**

```bash
streamlit run main.py
```

O Streamlit abrirá a aplicação no navegador (normalmente em `http://localhost:8501`).

---

## Formato dos dados

O CSV precisa ter **exatamente** estas colunas (com os mesmos nomes, incluindo o acento em `Instituição`):

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Data` | Data no formato `dd/mm/aaaa` | Data do registro |
| `Instituição` | Texto | Nome da instituição financeira |
| `Valor` | Numérico | Saldo na data, em reais |

**Exemplo fictício** (apenas para ilustração):

```csv
Data,Instituição,Valor
01/01/2024,Banco Exemplo,10000.00
01/01/2024,Corretora Exemplo,25000.00
01/02/2024,Banco Exemplo,10500.00
01/02/2024,Corretora Exemplo,25800.00
01/03/2024,Banco Exemplo,10800.00
01/03/2024,Corretora Exemplo,26500.00
```

O repositório inclui o arquivo `Template Controle Financeiro - Saldo Mensal.csv`, que pode ser usado como modelo para testar a aplicação.

Recomendações:
- Use um registro por instituição em cada data.
- Use o ponto como separador decimal e o formato de data indicado acima.
- Para as médias e evoluções de 6, 12 e 24 períodos aparecerem, o histórico precisa ter pelo menos essa quantidade de datas.

---

## Integração com a API do Banco Central

A função `get_selic()` consulta a API de dados abertos do Banco Central (Sistema Gerenciador de Séries Temporais) para obter a **série 432 da Selic**:

```text
https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados
```

- **Finalidade:** sugerir automaticamente a taxa Selic vigente na data de início da meta, usada para estimar o rendimento do patrimônio.
- **Período consultado:** de `01/01/2020` a `31/12/2025` (fixo no código).
- **Requisitos:** acesso à internet. A requisição tem timeout de 30 segundos e levanta erro em caso de resposta HTTP inválida.
- **Uso do valor:** o usuário pode substituir a taxa sugerida por outra na própria interface.

---

## Limitações e considerações

- **Período da Selic fixo:** a consulta cobre apenas de 01/01/2020 a 31/12/2025. Datas de início de meta fora desse intervalo podem não funcionar como esperado (antes de 2020 não há valor disponível; depois de 2025 será usado o último valor do período consultado).
- **Fator da arrecadação anual:** o código calcula o potencial anual como `2 × (salário líquido − custos fixos) + rendimento anual`, enquanto o texto de ajuda exibido na interface descreve `12 × (...)`. Essa divergência deve ser revisada antes de se interpretar o resultado.
- **Salário bruto:** o campo é solicitado na interface, mas não é utilizado em nenhum cálculo atual.
- **Rendimento simplificado:** a estimativa aplica a Selic diretamente sobre o patrimônio total, sem considerar impostos, taxas, inflação ou o perfil real dos investimentos.
- **Múltiplos registros na mesma data/instituição:** a tabela dinâmica usa a média por padrão, enquanto as estatísticas gerais usam a soma. Evite duplicidades no CSV.
- **Janelas em períodos:** as métricas de 6, 12 e 24 períodos assumem dados mensais regulares.
- **Sem validação de entrada:** o código não valida colunas ausentes ou formatos incorretos do CSV.
- **Sem cache:** a consulta à Selic é refeita sempre que a página é reexecutada com um arquivo carregado.
- **Sem persistência, autenticação ou armazenamento:** nada disso está implementado. Os dados existem apenas durante a sessão.
- **Dependência externa:** a seção de metas depende da disponibilidade da API do Banco Central.
- **Uso informativo:** as projeções não representam garantia de rentabilidade.

---

## Possíveis melhorias futuras

> Nenhum dos itens abaixo está implementado.

- Validar o CSV e exibir mensagens claras para colunas ou datas inválidas.
- Tornar o período da consulta à Selic dinâmico (até a data atual).
- Usar cache nas chamadas à API (`st.cache_data`).
- Corrigir/alinhar o cálculo e o texto de ajuda da arrecadação anual e usar o salário bruto, se fizer sentido.
- Incluir impostos e inflação nas estimativas.
- Adicionar testes automatizados.
- Permitir exportar tabelas e gráficos.

---

## Aprendizados técnicos

Conceitos aplicados no código:

- **Tratamento de dados com Pandas:** conversão de datas, `groupby`, `pivot_table`, `shift`, `rolling` com funções personalizadas, `merge` e criação de colunas derivadas.
- **Análise financeira básica:** variações absolutas e relativas, médias móveis, taxa anual convertida em taxa mensal equivalente e acompanhamento de metas.
- **Visualização de dados:** gráficos de linhas e de barras com Streamlit.
- **Interfaces interativas:** `file_uploader`, `expander`, `tabs`, `columns`, `container`, `selectbox`, `date_input`, `number_input` e `column_config` para formatação de valores.
- **Integração com API REST:** consumo de dados públicos em JSON com Requests, tratamento de erros HTTP e conversão para DataFrame.
