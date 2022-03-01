# batter dashboard class

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from module.module import count_year, batter_list, daily_hit_prob, batter_yearly_base, get_team_name
from dashboard.base import baselayout
from plotly.subplots import make_subplots
import pandas as pd

def Batter_Base_layout(app):

    app.title = "KBO analysis"
    team_name = []
    year = count_year()
    batter_name = []

    app.layout = html.Div([
        baselayout,
        # 그래프
        dbc.Container([
            dbc.Row(dbc.Col(children=[html.H2("선수를 선택해 주세요")], style={'margin-top':80, 'margin-right':10,'margin-left':10},id="title")),
            dbc.Row(dbc.Col(dbc.Alert("해당 분석은 한국프로야구단 공식 홈페이지인 KBO에서 스크래핑한 데이터를 바탕으로 진행되었습니다.", color="secondary", style={'margin-top':10, 'margin-right':10,'margin-left':10}))),
            dbc.Row([
                dbc.Col(children=[
                        dbc.Card([
                            dbc.CardHeader("최근 선수 스탯"),
                            dbc.CardBody(dcc.Graph(id='graph1')),
                            ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                        dbc.Card([
                            dbc.CardHeader("월별 타율 추세"),
                            dbc.CardBody(dcc.Graph(id='graph3')),
                            ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20})],
                             xs=12, sm=12, md=6, lg=6),
                 dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("연도별 스탯 변화 추이"),
                            dbc.CardBody(dcc.Graph(id='graph2'))
                            ], style={'width':"auto", 'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                             xs=12, sm=12, md=6, lg=6),
                        ]
                ,no_gutters=True,
                justify="around"),
            ],
            id = "graphs",
            style={"width":"auto", 'margin-left': 210, 'color': None, "transition":"all .2s", "z-index": -1},
            fluid=True),
        # 사이드바
        html.Div([
            html.Div([
                dbc.Nav([
                html.P("Main", style={'color':'#7E8083', 'font-size' : '80%'}),
                html.Li(dbc.Row([
                    dbc.Col(html.I(className="fas fa-chart-bar fa-2x", style={'color':'#FFFFFF', 'margin-top': 11, 'font-size':20}), width="auto"),
                    dbc.Col(dbc.NavItem(dbc.NavLink("Batters", href="http://127.0.0.1:5000/batters/", id="batters", style={"color":"#FFFFFF", 'margin-left':-30}))),
                    dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#FFFFFF','margin-top': 8}), href="http://127.0.0.1:5000/batters/")), width=3)                        
                    ])),
                html.Div([
                    dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id='year_select',
                        options=[{'label': i, 'value': i} for i in year],
                        value='year_select',
                        placeholder="year",
                        )),
                    dbc.Col(dcc.Dropdown(
                        id='team_name_select',
                        options=[{'label': i, 'value': i} for i in team_name],
                        value='team_select',
                        placeholder="team",
                        ))],
                        no_gutters=True,
                        align="center",
                        justify="center"
                        ),
                    html.Br(),
                    dcc.Dropdown(
                        id='batter_name_select',
                        options=[{'label': i, 'value': i} for i in batter_name],
                        value='batter_select',
                        placeholder="Choose a batter"
                        )
                    ],
                    style={'width': '100%', 'display': 'inline-block', 'font-size' : '80%', 'margin-bottom': 80, 'margin-top':5}),

                    html.P("Others", style={'color':'#7E8083', 'font-size' : '80%'}),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-project-diagram", style={'color':'#7E8083', 'margin-top': 12}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Teams", href="http://127.0.0.1:5000/teams/", id="teams", style={"color":"#7E8083", 'margin-left':-30}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/teams/")), width=3)                        
                    ])),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-table fa-2x", style={'color':'#7E8083', 'margin-top': 10,'font-size':18}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Pitchers", href="http://127.0.0.1:5000/pitchers/", id="pitchers", style={"color":"#7E8083", 'margin-left':-28}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/pitchers/")), width=3)
                    ])),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-balance-scale fa-2x", style={'color':'#7E8083', 'margin-top': 10,'font-size':17, 'margin-left':-1.5}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Comparer", href="http://127.0.0.1:5000/comparer/", id="comparer", style={"color":"#7E8083", 'margin-left':-30}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/comparer/")), width=3)
                    ]))
                    ],
                vertical="md",
                horizontal='start',
                className="ml-auto"),
            ],
            id="sidebar",
            style={
            "position": "fixed",
            "top": 55,
            "left": "0",
            "bottom": 0,
            "width": "13rem",
            "padding": "2rem 1rem",
            "background-color": "#353A3F",
            "transition":"left .2s"})],
        id="side",
        style={
        "position": "fixed",
        "top": 55,
        "left": "0",
        "bottom": 0,
        "width": "100%",
        "background-color": "rgba(0, 0, 0, 0.5)",
        "transition":"left .2s",
        })
    ])

    @app.callback(
        Output('team_name_select', "options"),
        Input('year_select', "value"))
    def team_name_list(value): 
        team_name = get_team_name(value)
        return [{'label': i, 'value': i} for i in team_name]

    @app.callback(
        Output('batter_name_select', "options"),
        [Input('year_select', "value"), Input('team_name_select', "value")])
    def batter_name_list(value1, value2): 
        batter_name = batter_list(value1, value2)
        return [{'label': i, 'value': i} for i in batter_name]
    
    @app.callback(
            Output('title', 'children'),
            Input('batter_name_select', "value"))    
    def batter_select_name(value):
        if value != 'batter_select' and value != None:
            children=[html.H2(f"{value} 선수의 분석결과 입니다.")]
        else:
            children=[html.H2("선수를 선택해 주세요")]
        return  children

    @app.callback(
        Output('batter_name_select', "value"),
        [Input('year_select', "value"), Input('team_name_select', "value")])
    def test_one(value1, value2):
        if value1 == None or value2 == None:
            return None

    @app.callback(
            Output('graph1', 'figure'),
            Output('graph2', 'figure'),
            [Input('team_name_select', "value"),Input('batter_name_select', 'value')])
    def batter_recent(value1,value2):
        scores = batter_yearly_base(value1,value2)
        df = pd.DataFrame(scores[1:], columns = ['YEAR', 'AVG', 'OBP', 'SLG', 'ISO', 'EOBP'])
        fig1 = go.Figure(go.Scatterpolar(r= list(scores[-1][1:]),
            theta=['평균타율(AVG)','출루율(OBP)','장타율(SGL)','순장타율(ISO)', '순출루율(EOBP)'],
            fill='toself'))
        fig1.update_layout(
            margin=dict(l=30, r=30, t=35, b=35),
            height = 300,template=None,
            polar = dict(
                radialaxis = dict(visible=True,range=[0.0,1.0],showticklabels=False, ticks=''),
                angularaxis = dict(showticklabels=True, ticks='', tickfont_size = 13)))
        fig2 = make_subplots(rows=2, cols=1,shared_xaxes=True,vertical_spacing=0.1,specs=[[{"type": "scatter"}],[{"type": "table"}]])
        fig2.add_trace(go.Scatter(x=df['YEAR'], y=df['AVG'], name='평균타율(AVG)', marker_color='#243858'))
        fig2.add_trace(go.Scatter(x=df['YEAR'], y=df['OBP'], name='출루율(OBP)', marker_color='#749A46'))
        fig2.add_trace(go.Scatter(x=df['YEAR'], y=df['SLG'], name='장타율(SGL)', marker_color='#6BB6DA'))
        fig2.add_trace(go.Scatter(x=df['YEAR'], y=df['ISO'], name='순장타율(ISO)', marker_color='#EC7D7A'))
        fig2.add_trace(go.Scatter(x=df['YEAR'], y=df['EOBP'], name='순출루율(EOBP)', marker_color='#F5CA6F'))
        fig2.add_trace(go.Table(columnorder = [1,2,3,4,5,6], columnwidth = [7.5,10,10,10,10,10],
            header=dict(values=df.columns,height=32,
                fill_color='#6E757C',line_color='#6E757C',align='center',font=dict(color='white')),
            cells=dict(values=[df.YEAR,df.AVG, df.OBP, df.SLG, df.ISO, df.EOBP],fill_color='white',
               line_color='#6E757C',font=dict(color='black'),align='center', height=32),),2,1)
        fig2.update_layout(height=695,margin=dict(l=0, r=0, t=0, b=0),template = 'plotly_white',
            yaxis =dict(anchor="free",side="left",position=0.015),xaxis = dict(tickmode= 'linear',dtick = 1),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
        
        return fig1, fig2

    @app.callback(
            Output('graph3', 'figure'),
            [Input('team_name_select', "value"),Input('batter_name_select', 'value')])
    def batter_monthly(value1,value2):
        df= daily_hit_prob(value1,value2)
        fig = go.Figure(go.Scatter(
            x = df['date'],y = df['value'],mode='markers',
            marker=dict(size=10,color=df['value'].astype('float'),colorscale="viridis",showscale=True)))
        fig.update_layout(template = 'plotly_white',height = 300,margin=dict(l=0, r=0, t=0, b=0))
        return fig

    @app.callback(
        Output("sidebar", "style"), Output("graphs", "style"), Output("side", "style"),
        [Input("sidebtn", "n_clicks")],
        [State("sidebar", "style"), State("graphs", "style"),State("side", "style")])
    def toggle(n, style1, style2, style3):
        if n and style1['left'] == "0" and style2['margin-left'] == 210:
            style1['left'] = "-13rem"
            style2['margin-left'] = 0
            style3['width'] = 0
            return style1, style2, style3
        else: 
            style1['left'] = "0"
            style2['margin-left'] = 210
            style3['width'] = "100%"
            return style1, style2, style3

    return app