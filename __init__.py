import flask
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap5 import Bootstrap5
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dashboard.teams import Team_Base_layout
from dashboard.batters import Batter_Base_layout 
from dashboard.pitchers import Pitcher_Base_layout
from dashboard.comparer import Comparer_Base_layout

# 어플리케이션 설정
app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = 'LOPES'

Bootstrap5(app)


# dashboard
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/css/bootstrap.min.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']
teams = dash.Dash(__name__, server=app, external_stylesheets= external_stylesheets, url_base_pathname='/teams/',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}])
batters = dash.Dash(__name__, server=app, external_stylesheets= external_stylesheets, url_base_pathname='/batters/',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}])
pitchers = dash.Dash(__name__, server=app ,external_stylesheets= external_stylesheets, url_base_pathname='/pitchers/',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}])
comparer = dash.Dash(__name__, server=app ,external_stylesheets= external_stylesheets, url_base_pathname='/comparer/',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}])

teams = Team_Base_layout(teams)
batters= Batter_Base_layout(batters)
pitchers= Pitcher_Base_layout(pitchers)
comparer = Comparer_Base_layout(comparer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
  