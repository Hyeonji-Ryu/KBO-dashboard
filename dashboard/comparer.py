# pitcher dashboard class

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dashboard.base import baselayout
from plotly.subplots import make_subplots
from module.dbmodule import team_win_table, month_win_prop, count_year, pitcher_names, batter_names, batter_yearly_base, pitcher_yearly_base
import pandas as pd

def Comparer_Base_layout(app):

    app.title = "KBO analysis"
    team_name = ['SK','기아','두산','한화','LG','삼성','키움','롯데', 'NC','KT']
    year = count_year()
    batter_name = []
    pitcher_name = []


    app.layout = html.Div([
        baselayout,
        # 그래프
        dbc.Container([
            dbc.Row(dbc.Col(dbc.Alert("해당 분석은 한국프로야구단 공식 홈페이지인 KBO에서 크롤링한 데이터를 바탕으로 진행되었습니다.", color="secondary", style={'margin-top':80, 'margin-right':10,'margin-left':10}))),
            dbc.Row([
                dbc.Col(children=[
                        dbc.Card([
                            dbc.CardHeader("팀별 분석 비교"),
                            dbc.CardBody(
                                dcc.Checklist(
                                    id='team_name_select',
                                    value = '',
                                    options=[{'label': i, 'value': i} for i in team_name],
                                    inputStyle={'margin-right':'4px','margin-left':'4px'},
                                    labelStyle={'margin-right':'9px','margin-left':'9px'})
                            ),
                            ],color="light", style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                        dbc.CardColumns([
                            dbc.Card([
                                dbc.CardHeader("연도별 승리 추세선"),
                                dbc.CardBody(
                                dcc.Graph(id='team_win_graph', hoverData={'points': [{'year': 'record'}]})
                            ),
                            ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                            dbc.Card([
                                dbc.CardHeader("누적 월별 승률(%)"),
                                dbc.CardBody(
                                dcc.Graph(id='month_winprop_graph', hoverData={'points': [{'year': 'prop'}]})
                            ),
                            ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20})])
                            ],
                             xs=12, sm=12, md=6, lg=6),
                dbc.Col(children=[
                        dbc.Card([
                            dbc.CardHeader("선수별 분석 비교"),
                            dbc.CardBody(
                                dcc.RadioItems(
                                id="player",
                                options=[{'label': '타자(Batter)', 'value': 'batter'},{'label': '투수(Pitcher)', 'value': 'pitcher'}],
                                value='batter', inputStyle={'margin-right':'10px'}, labelStyle={'margin-right':'20px'})
                            )
                            ],color="light", style={'width':"auto", 'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                        dbc.Card([
                            dbc.CardBody(
                            html.Div([
                                    dcc.Dropdown(
                                        id='name_list',
                                        options=[{'label': i, 'value': i} for i in batter_name],
                                        value=[''],
                                        placeholder="Typing player name",
                                        multi=True
                                        ),
                                    dcc.Graph(id='graph2')
                                ],
                                style={'width': '100%', 'display': 'inline-block', 'font-size' : '80%', 'margin-bottom': 80, 'margin-top':5})
                            )
                            ], style={'width':"auto", 'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20})],
                            xs=12, sm=12, md=6, lg=6)],
                        no_gutters=True,
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
                        dbc.Col(html.I(className="fas fa-balance-scale fa-2x", style={'color':'#FFFFFF', 'margin-top': 11,'font-size':17, 'margin-left':-1.5}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Comparer", href="http://127.0.0.1:5000/comparer/", id="comparer", style={"color":"#FFFFFF", 'margin-left':-30}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#FFFFFF','margin-top': 8}), href="http://127.0.0.1:5000/comparer/")), width=3)
                    ])),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.P("Others", style={'color':'#7E8083', 'font-size' : '80%'}),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-project-diagram", style={'color':'#7E8083', 'margin-top': 12}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Teams", href="http://127.0.0.1:5000/teams/", id="teams", style={"color":"#7E8083", 'margin-left':-30}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/teams/")), width=3)                        
                    ])),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-chart-bar fa-2x", style={'color':'#7E8083', 'margin-top': 11, 'font-size':20}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Batters", href="http://127.0.0.1:5000/batters/", id="batters", style={"color":"#7E8083", 'margin-left':-30}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/batters/")), width=3)
                    ])),
                    html.Li(dbc.Row([
                        dbc.Col(html.I(className="fas fa-table fa-2x", style={'color':'#7E8083', 'margin-top': 10,'font-size':18}), width="auto"),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Pitchers", href="http://127.0.0.1:5000/pitchers/", id="pitchers", style={"color":"#7E8083", 'margin-left':-28}))),
                        dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/pitchers/")), width=3)                        
                    ])),
                    ],
                vertical="md",
                horizontal='start',
                className="ml-auto"),
            ],
            id="sidebar",
            style={
            "position": "fixed",
            "top": 55,
            "left": "-13rem",
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
        "width": 0,
        "background-color": "rgba(0, 0, 0, 0.5)",
        "transition":"left .2s",
        })
    ])

    @app.callback(
        Output("sidebar", "style"), Output("graphs", "style"), Output("side", "style"),
        [Input("sidebtn", "n_clicks")],
        [State("sidebar", "style"), State("graphs", "style"),State("side", "style")])
    def toggle(n, style1, style2, style3):
        if n and style1['left'] == "-13rem" and style2['margin-left'] == 0:
            style1['left'] = 0
            style2['margin-left'] = 210
            style3['width'] = "100%"
            return style1, style2, style3
        else: 
            style1['left'] = "-13rem"
            style2['margin-left'] = 0
            style3['width'] = 0
            return style1, style2, style3

    @app.callback(
            Output('team_win_graph', 'figure'),
            Output('month_winprop_graph', 'figure'),
            Input('team_name_select', 'value'))
    def update_output(value):
        fig1 = go.Figure()
        fig2 = go.Figure()
        for i in range(len(value)):
            year, prop, pred = team_win_table(value[i])
            prop1 = month_win_prop(value[i])
            fig1.add_trace(go.Scatter(x=year, y=prop, name=value[i]))
            fig2.add_trace(go.Bar(x=[3,4,5,6,7,8,9,10], y=prop1,name=value[i], text=prop1))
            fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig1.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            template = 'plotly_white',
            height=300,
            xaxis = dict(tickmode = 'linear',dtick = 1),
            legend=dict(orientation="h",yanchor="bottom",xanchor="center",x = 0.5, y=-0.2))
        fig2.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            template = 'plotly_white',
            height=300,
            xaxis = dict(tickmode = 'linear',dtick = 1),
            legend=dict(orientation="h",yanchor="bottom",xanchor="center",x = 0.5, y=-0.2))
        return fig1, fig2

    @app.callback(
        Output('name_list', "options"),
        Output('name_list', "value"),
        Input('player', "value"))
    def batter_name_list(value): 
        if value == 'pitcher':
            pitcher_name = pitcher_names()
            value = ['']
            options = [{'label': i, 'value': i} for i in pitcher_name]
            return options, value
        else:
            batter_name = batter_names()
            value = ['']
            options = [{'label': i, 'value': i} for i in batter_name]
            return options, value

    @app.callback(
        Output('graph2', "figure"),
        Input('name_list', "value"), Input('player', "value"))
    def batter_graph(value, value2):
        if value2 == 'batter':
            fig = make_subplots(rows=2, cols=1,vertical_spacing=0.1,specs=[[{"type": "scatterpolar"}],[{"type": "table"}]])
            df = pd.DataFrame(columns = ['NAME', 'AVG', 'OBP', 'SLG', 'ISO', 'EOBP'])
            if len(value)==0 : value =['']
            for i in range(len(value)):
                scores = batter_yearly_base(value[i])
                df.loc[i] = scores[-1]
                df.replace(2020,value[i],inplace=True)
                fig.add_trace(go.Scatterpolar(r= list(scores[-1][1:]),opacity= 0.7,
                    theta=[' 평균타율(AVG) ',' 출루율(OBP) ',' 장타율(SGL) ',' 순장타율(ISO) ', ' 순출루율(EOBP) '],
                    fill='toself', name=value[i]),1,1)
            fig.add_trace(go.Table(
                header=dict(values=df.columns,height=32, fill_color='#6E757C',line_color='#6E757C',align='center',font=dict(color='white')),
                cells=dict(values=[df.NAME,df.AVG, df.OBP, df.SLG, df.ISO, df.EOBP],fill_color='white', line_color='#6E757C',font=dict(color='black'),align='center', height=32)),2,1)
            fig.update_layout(height=610,margin=dict(l=0, r=0, t=35, b=0),template = None,
                polar = dict(
                    radialaxis = dict(visible=True,showticklabels=False, ticks=''),
                    angularaxis = dict(showticklabels=True, ticks='', tickfont_size = 13)),
                yaxis =dict(anchor="free",side="left",position=0.015),xaxis = dict(tickmode= 'linear',dtick = 1),
                legend=dict(orientation="h",yanchor="bottom",y=1.05,xanchor="center",x=0.5))
        else:
            fig = make_subplots(rows=2, cols=1,vertical_spacing=0.1,specs=[[{"type": "scatterpolar"}],[{"type": "table"}]])
            df = pd.DataFrame(columns = ['NAME','AVG','OBP','RA9','ERA','FIP'])
            if len(value)==0 : value =['']
            for i in range(len(value)):
                scores, temp = pitcher_yearly_base(value[i])
                df.loc[i] = scores[-1]
                df.replace(2020,value[i],inplace=True)
                df.replace(float('inf'),0,inplace=True)
                df= df.fillna(0)
                fig.add_trace(go.Scatterpolar(r= list(scores[-1][1:]),opacity= 0.7,
                    theta=[' 피안타율(AVG) ',' 피출루율(OBP) ',' 평균실점(RA9) ',' 평균자책점(ERA) ',' 수비무관투구(FIP) '],
                    fill='toself', name=value[i]),1,1)
                fig.add_trace(go.Table(
                header=dict(values=df.columns,height=32,
                fill_color='#6E757C',line_color='#6E757C',align='center',font=dict(color='white')),
                cells=dict(values=[df.NAME, df.AVG, df.OBP, df.RA9, df.ERA, df.FIP],fill_color='white',
               line_color='#6E757C',font=dict(color='black'),align='center', height=32)),2,1)
            fig.update_layout(height=610,margin=dict(l=0, r=0, t=35, b=0),template = None,
                polar = dict(
                    radialaxis = dict(visible=True,showticklabels=False, ticks=''),
                    angularaxis = dict(showticklabels=True, ticks='', tickfont_size = 13)),
                yaxis =dict(anchor="free",side="left",position=0.015),xaxis = dict(tickmode= 'linear',dtick = 1),
                legend=dict(orientation="h",yanchor="bottom",y=1.05,xanchor="center",x=0.5))
        return fig

    return app