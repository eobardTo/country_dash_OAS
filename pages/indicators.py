from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from data import df, all_cont
import plotly.express as px

layout = dbc.Container([
        dbc.Row ([
        dbc.Col(
                html.Div([
                html.H1("Статистика по отдельным странам"),
                html.H5("Выберите континенты и показатель"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
      )
    ]),

     html.Div([
            html.Div([
                html.Label('Выберите континенты: '),
                dcc.Dropdown(
                    id = 'crossfilter-cont',
                    options = [{'label': i, 'value': i} for i in all_cont],
                    # значение континента, выбранное по умолчанию
                    value = ['Europe'],
                    # возможность множественного выбора
                    multi = True
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
       
            html.Div([
                html.Label('Выберите показатель: '),
                dcc.RadioItems(
                options = [
                    {'label':'Продолжительность жизни', 'value': 'Life expectancy'},
                    {'label':'Население', 'value': 'Population'},
                    {'label':'ВВП', 'value': 'GDP'},
                    {'label':'Школьное образование', 'value': 'Schooling'},
                ],
                id = 'crossfilter-ind',
                value = 'GDP',
                labelStyle={'display': 'inline-block'}
                )
            ],
            style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),

            html.Div([
            html.Label('Выберите интервал: '),
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Year'].min(),
                max = df['Year'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Year'].unique()}
                )],
            style = {'width': '95%', 'padding': '20px 0px 0px 0px'}
            ),
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        
        html.Div(
            dcc.Graph(id = 'bar'),
            style = {'width': '49%', 'display': 'inline-block'}
        ),
       
        html.Div(
            dcc.Graph(id = 'line'),
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),

])

@callback(
    Output('bar', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.bar(
        filtered_data,
        x = 'Year',
        y = indication,
        color = 'Country'
        )
    return figure

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = "Year",
        y = indication,
        color = "Country",
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure