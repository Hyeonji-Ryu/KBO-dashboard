# 분석 보고서 기본적인 틀 정리

import dash_bootstrap_components as dbc
import dash_html_components as html


baselayout = dbc.Navbar(
    [html.A(
            dbc.Row(dbc.Col(dbc.NavbarBrand("KBO analysis", className="ml-4")),
                align="center",
                no_gutters=False
            ),
            href="http://127.0.0.1:5000/",
            style={'text-decoration' : 'none'}),
            dbc.Button(html.I(className="fas fa-bars"), className="mr-2", id="sidebtn", style={"background-color":"#222529", 'border':0, 'margin-left':50,'transition':'none'}, n_clicks=0)],
    color="#222529",
    dark=True,
    style={'line-height' : '2.0'},
    fixed="top",
)