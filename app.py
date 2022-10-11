# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import main as calcs
import plotly.express as px
import pandas as pd

df = calcs.genMarginals(children=3, married=True, studentLoan=False)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

server = app.server

header = html.H4(
    "UK marginal tax rate calculator", className="bg-primary text-white p-2 mb-2 text-center"
)

married_dropdown = html.Div(
    [
        dbc.Label("Marital status"),
        dcc.Dropdown(
            ["Married", "Not married (incl. divorced or widowed)"],
            "Not married (incl. divorced or widowed)",
            id="married_drop",
            clearable=False,
        ),
    ],
    className="mb-4",
)

loan_dropdown = html.Div(
    [
        dbc.Label("Student loan"),
        dcc.Dropdown(
            ["No"],
            "No",
            id="student_loan",
            clearable=False,
        ),
    ],
    className="mb-4",
)

children_dropdown = html.Div(
    [
        dbc.Label("Number of children"),
        dcc.Dropdown(
            {i: i for i in range(10)}, 0,
            id='number_children',
            clearable=False,
        ),
    ],
    className="mb-4",
)

line_graph = dcc.Graph(id='marginal-graph',
                       # className="m-4"
                       )

controls = dbc.Card(
    [married_dropdown,
     loan_dropdown,
     children_dropdown],
    body=True,
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls,
                        # When running this app locally, un-comment this line:
                        # ThemeChangerAIO(aio_id="theme")
                    ],
                    width=4,
                ),
                dbc.Col(line_graph, width=8),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)


# app.layout = html.Div([
#     # html.H1(
#     #     children='UK marginal tax rate calculator', style={
#     #         'textAlign': 'left'},
#     #     id='title'
#     # ),
#
#     # html.H2(children='It\'s much higher than you might think', style={
#     #     'textAlign': 'left'
#     # }),
#
#     html.Div([
#
#         html.Div([
#             html.Br(),
#             dbc.Label("Marital status"),
#             # html.Label('Marital status'),
#             dcc.Dropdown(['Married', 'Not married (incl. divorced or widowed)'], 'Married',
#                          id='married_drop')
#         ],
#             # style={'width': '30%', 'display': 'inline-block'}
#         ),
#
#         html.Div([
#             html.Br(),
#             html.Label('Student loan?'),
#             dcc.Dropdown(['Yes', 'No'], 'Yes',
#                          id='student_loan')
#         ], style={'width': '30%', 'float': 'center', 'display': 'inline-block'}),
#
#         html.Div([
#             html.Br(),
#             html.Label('Number of children'),
#             dcc.Dropdown({i: i for i in range(10)}, 0,
#                          id='number_children')
#         ], style={'width': '30%', 'display': 'inline-block'})
#
#     ]),
#
#     dcc.Graph(id='marginal-graph'
#               )
#
# ], style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output(component_id='marginal-graph', component_property='figure'),
    Input(component_id='number_children', component_property='value'),
    Input(component_id='married_drop', component_property='value'),
    Input(component_id='student_loan', component_property='value'),
)
def update_graph(number_children, married_drop, student_loan):
    if married_drop == 'Married':
        married = True
    else:
        married = False

    if student_loan == 'Yes':
        loan = True
    else:
        loan = False

    dff = calcs.genMarginals(int(number_children), married, loan)
    fig = px.line(dff,
                  x="Gross Income",
                  y="Marginal Tax Rate",
                  template="plotly"
                  )
    fig.layout.yaxis.tickformat = ',.0%'

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
