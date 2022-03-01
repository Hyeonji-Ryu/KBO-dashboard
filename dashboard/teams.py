# team dashboard class

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from module.module import team_win_table, month_win_prob, home_visit_prob, team_win_prob
from dashboard.base import baselayout
from plotly.subplots import make_subplots

def Team_Base_layout(app):

    app.title = "KBO analysis"
    team_name = ['SK','KIA','두산','한화','LG','삼성','키움','롯데','NC','KT','SSG']

    app.layout = html.Div([
        baselayout,
        # 그래프
        dbc.Container([
            dbc.Row(dbc.Col(children=[html.H2("팀을 선택해 주세요")], style={'margin-top':80, 'margin-right':10,'margin-left':10},id="title")),
            dbc.Row(dbc.Col(dbc.Alert("해당 분석은 한국프로야구단 공식 홈페이지인 KBO에서 스크래핑한 데이터를 바탕으로 진행되었습니다.", color="secondary", style={'margin-top':10, 'margin-right':10,'margin-left':10}))),
            dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Keyword"),
                            dbc.CardBody(children=[html.H5("None")],id="card1")],
                            style={'margin-top':10, 'margin-right':10,'margin-left':10}, color="primary", inverse=True),
                            xs=12, sm=6, md=6, lg=3),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Keyword"),
                            dbc.CardBody(children=[html.H5("None")],id="card2")],
                            style={'margin-top':10, 'margin-right':10,'margin-left':10}, color="secondary", inverse=True),
                            xs=12, sm=6, md=6, lg=3),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Keyword"),
                            dbc.CardBody(children=[html.H5("None")],id="card3")],
                            style={'margin-top':10, 'margin-right':10,'margin-left':10}, color="info", inverse=True),
                            xs=12, sm=6, md=6, lg=3),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Keyword"),
                            dbc.CardBody(children=[html.H5("None")],id="card4")],
                            style={'margin-top':10, 'margin-right':10,'margin-left':10}, color="dark", inverse=True),
                            xs=12, sm=6, md=6, lg=3)],
                        no_gutters=True,
                        justify="center"),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("연도별 승리 추세선"),
                        dbc.CardBody(dcc.Graph(id='team_win_graph', hoverData={'points': [{'year': 'record'}]}))
                        ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10}),
                         xs=12, sm=12, md=6, lg=6),
                 dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("누적 월별 승률(%)"),
                        dbc.CardBody(dcc.Graph(id='month_winprop_graph', hoverData={'points': [{'year': 'prop'}]}))
                        ], style={'width':"auto",'margin-top':20, 'margin-right':10,'margin-left':10}),
                         xs=12, sm=12, md=6, lg=6),
                ]
                ,no_gutters=True,
                justify="around"),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("홈원정팀 누적 승패 횟수"),
                        dbc.CardBody(dcc.Graph(id='pie_graph'))
                        ], style={'width':"auto",'margin-top':20, 'margin-left':10,'margin-right':10,'margin-bottom':20}),
                         xs=12, sm=12, md=6, lg=6),
                 dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("구단별 누적 1:1 승률"),
                        dbc.CardBody(dcc.Graph(id='map_graph', hoverData={'points': [{'year': 'prop'}]}))
                        ], style={'width':"auto",'margin-top':20, 'margin-right':10,'margin-left':10,'margin-bottom':20}),
                         xs=12, sm=12, md=6, lg=6),
                ]
                ,no_gutters=True,
                justify="around"),
            ],
            id = "graphs",
            style={"width":"auto", 'margin-left': 210, "transition":"all .2s"},
            fluid=True),
        # 사이드바
        html.Div([
            html.Div([
                dbc.Nav([
                html.P("Main", style={'color':'#7E8083', 'font-size' : '80%'}),
                html.Li(dbc.Row([
                    dbc.Col(html.I(className="fas fa-project-diagram", style={'color':'#FFFFFF', 'margin-top': 12}), width="auto"),
                dbc.Col(dbc.NavItem(dbc.NavLink("Teams", href="http://127.0.0.1:5000/teams/", id="teams", style={"color":"#FFFFFF", 'margin-left':-30}))),
                dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#FFFFFF','margin-top': 8}), href="http://127.0.0.1:5000/teams/")), width=3)                        
                ])),
                html.Div([
                dcc.Dropdown(
                    id='team_name_select',
                    options=[{'label': i, 'value': i} for i in team_name],
                    value='team_select',
                    placeholder="Choose a team",
                    )
                ],style={'width': '100%', 'display': 'inline-block', 'font-size' : '80%', 'margin-bottom': 80, 'margin-top':5}),

                html.P("Others", style={'color':'#7E8083', 'font-size' : '80%'}),
                html.Li(dbc.Row([dbc.Col(html.I(className="fas fa-chart-bar fa-2x", style={'color':'#7E8083', 'margin-top': 11, 'font-size':20}), width="auto"),
                    dbc.Col(dbc.NavItem(dbc.NavLink("Batters", href="http://127.0.0.1:5000/batters/", id="batters", style={"color":"#7E8083", 'margin-left':-30}))),
                    dbc.Col(dbc.NavItem(dbc.NavLink(html.I(className="fas fa-chevron-right fa-xs", style={'color':'#7E8083','margin-top': 8}), href="http://127.0.0.1:5000/batters/")), width=3)
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
            Output('title', 'children'),
            Input('team_name_select', 'value'))    
    def team_select_name(value):
        if value != 'team_select' and value != None:
            children=[html.H2(f"{value}팀의 분석결과 입니다.")]
        else:
            children=[html.H2("팀을 선택해 주세요")]
        return  children

    @app.callback(
            Output('team_win_graph', 'figure'),
            Output('card1','children'),
            Input('team_name_select', 'value'))
    def update_output_div(value):
        year, prop, pred = team_win_table(value)
        fig = go.Figure(go.Scatter(x=year, y=pred, name='기대 승률', line = dict(color='#b3b9c4', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=year, y=prop, name='실제 승률', marker_color='rgb(63, 63, 191)'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            template = 'plotly_white',
            height=300,
            xaxis = dict(tickmode = 'linear',dtick = 1),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        if value != 'team_select' and value != None and prop[-2] > prop[-1]:
            children = [html.H5('최근년도 하락세')]
        elif value != 'team_select' and value != None and prop[-2] < prop[-1]:
            children = [html.H5('최근년도 상승세')]
        elif value != 'team_select' and value != None and prop[-2] == prop[-1]:
            children = [html.H5('최근년도 추세변동없음')]
        else: children=[html.H5("None")]
        return fig, children
    
    @app.callback(
            Output('month_winprop_graph', 'figure'),
            Output('card2','children'),
            Input('team_name_select', 'value'))
    def update_output(value):
        month, prop = month_win_prob(value)
        fig = go.Figure(go.Bar(x=month, y=prop, marker_color='#6E757C', text=prop))
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            template = 'plotly_white',
            height=300,
            yaxis_range=[0.0,1.0],
            xaxis = dict(tickmode = 'linear',dtick = 1),
            showlegend=False)
        if value != 'team_select' and value != None and max(prop)-min(prop) < 0.1:
            children = [html.H5('균일한 승률')]
        elif value != 'team_select' and value != None and prop.index(max(prop)) in [0,1,2,3]:
            children = [html.H5('전반전 강자')]
        elif value != 'team_select' and value != None and prop.index(max(prop)) in [4,5,6,7,8]:
            children = [html.H5('후반전 강자')]
        else: children=[html.H5("None")]
        return fig, children

    @app.callback(
            Output('pie_graph', 'figure'),
            Output('card3','children'),
            Input('team_name_select', 'value'))
    def update_pie(value):
        home_df, visit_df, num = home_visit_prob(value)
        label = ['lose', 'draw','win']
        night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)']
        specs = [[{'type':'domain'}, {'type':'domain'}]]
        if value != 'team_select' and value != None:
            temp=['HOME', 'AWAY']
        else: temp=[]
        fig = make_subplots(rows=1, cols=2, specs = specs, subplot_titles=temp)
        fig.add_trace(go.Pie(labels=label, values=home_df['score'], hole=.3, marker_colors=night_colors),1,1)
        fig.add_trace(go.Pie(labels=label, values=visit_df['score'], hole=.3,marker_colors=night_colors),1,2)
        fig.update_traces(textinfo='percent+label', textfont_size=[15, 10, 15], textposition=["inside","outside","inside"])
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
            legend=dict(orientation="h",yanchor="bottom",xanchor="center",x = 0.5, y=-0.3))
        if value != 'team_select' and value != None and  (num >= 0.03):
            children = [html.H5('홈경기 우세')]
        elif value != 'team_select' and value != None and (-0.03 < num < 0.03):
            children = [html.H5('장소 상관 없음')]
        elif value != 'team_select' and value != None and (num <= -0.03):
            children = [html.H5('원정경기 우세')]
        else: children=[html.H5("None")]
        return fig, children

    @app.callback(
            Output('map_graph', 'figure'),
            Output('card4','children'),
            Input('team_name_select', 'value'))
    def update_output(value):
        df=team_win_prob(value)
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="team",color = "prop",size="prop", 
                    color_continuous_scale=px.colors.sequential.Cividis,size_max=20, zoom=5, height=300)
        fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        if value != 'team_select' and value != None and min(df['prop']) != 0:
            name = list(df[df.prop==min(df['prop'])]['team'])[0]
            children = [html.H5(f'{name}팀에 약세')]
        else: children=[html.H5("None")]
        return fig, children

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