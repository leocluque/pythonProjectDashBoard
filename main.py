from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

ALLOWED_TYPES = (
    "search",
)

# criando o grafico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas")

app.layout = html.Div(children=[
    html.H1(children='Faturamento das lojas'),
    html.H2(children='Grafico com o faturamento de todos os produtos separados por loja'),

    html.Div(children='''
    obs: Esse grafico mostra a quantidade de produtos vendidos não o faturamento
    '''),

    html.Div(
        [
            dcc.Input(
                id="search",
                type=_,
                placeholder="input type {}".format(_),
            )
            for _ in ALLOWED_TYPES
        ]
        + [html.Div(id="procura-loja")]
    ),

    dcc.Dropdown(opcoes, value='Todas', id='list_lojas'),

    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])


# @app.callback(
#     Output('grafico_quantidade_vendas', 'figure'),
#     Input('search', 'value')
# )

@app.callback(
    Output('grafico_quantidade_vendas', 'figure'),
    Input('list_lojas', 'value'),
    Input('search', 'value')
)
def update_output(loja, search_words):
    if search_words == "":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == search_words, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

    # if loja == "Todas":
    #     fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    # else:
    #     tabela_filtrada = df.loc[df['ID Loja'] == loja, :]
    #     fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    # return fig


if __name__ == '__main__':
    app.run_server(debug=True)
