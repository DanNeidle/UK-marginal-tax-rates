# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import main as calcs
import plotly.express as px
import pandas as pd

df = calcs.genMarginals(children=3, married=True, studentLoan=False)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        children='UK marginal tax rate for married earner, family of 3 kids', style={
            'textAlign': 'center'},
        id='title'
    ),

    html.H2(children='It\'s insane.', style={
        'textAlign': 'center'
    }),

    html.Div([

        html.Div([
            html.Br(),
            html.Label('Marital status'),
            dcc.Dropdown(['Married', 'Not married (incl. divorced or widowed)'], 'Married',
                         id='married_drop')
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Br(),
            html.Label('Student loan?'),
            dcc.Dropdown(['Yes', 'No'], 'Yes',
                         id='student_loan')
        ], style={'width': '30%', 'float': 'center', 'display': 'inline-block'}),

        html.Div([
            html.Br(),
            html.Label('Number of children'),
            dcc.Dropdown({i: i for i in range(10)}, 0,
                         id='number_children')
        ], style={'width': '30%', 'display': 'inline-block'})

    ]),

    dcc.Graph(id='marginal-graph'
              )

], style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output(component_id='marginal-graph', component_property='figure'),
    # Output(component_id='title', component_property='value'),
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
    fig = px.line(dff, x="Gross Income", y="Marginal Tax Rate")
    fig.layout.yaxis.tickformat = ',.0%'

    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


