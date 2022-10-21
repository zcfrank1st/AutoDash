import yaml
from jinja2 import Template
import ast
import argparse

parser = argparse.ArgumentParser(description="Auto generate static dashboard")
parser.add_argument('-e','--environment', default='dev' ,choices=['dev','prod'] ,help='generate plain code for prod or run server for dev')
parser.add_argument('-f','--file', default='conf.yaml' ,help="config file")
argu = parser.parse_args()

args_dict = vars(argu)

dash_conf = ""
with open(args_dict.get('file'),'rt') as f:
    dash_conf = f.read()

conf = yaml.safe_load(dash_conf)

content = """
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__, external_stylesheets=[dbc.themes.{{theme}}])
load_figure_template('{{figure_theme}}')

header = html.H1(children='{{ info.title }}')
sub_header = html.Div(children='{{ info.sub_title }}')
{% set _extra = ['csv', 'excel', 'plain'] -%}
{%- for source in sources -%}
{%- set sindex = loop.index -%}
    {%- for skey in source.keys() -%}
{%- if skey not in _extra %}
import {{skey}}
engine_{{sindex}} = create_engine('{{source[skey].engine}}')
{% endif %}
df_{{sindex}} = {{ source[skey].data_handle }}
    {% endfor -%}
{%- endfor -%}
{%- for graph in graphs -%}
{%- set gindex = loop.index -%}
    {%- for gkey in graph %}
fig_{{gindex}} = px.{{ gkey }}(df_{{gindex}}, **conf.get('graphs')[{{gindex - 1}}].get('{{ gkey }}'))
graph_{{gindex}} = dcc.Graph(id='fig_{{gindex}}',figure=fig_{{gindex}},style={'flex': 1})
    {% endfor -%}
{%- endfor %}
app.layout = html.Div(children=[
    header,
    sub_header,
{% for n_row in range(layout.row) -%}
    {%- set graphs_list = [] -%}
    {%- for n_col in range(n_row * layout.column, (n_row+1) * layout.column) -%}
        {%- set id = 'graph_'~((n_col+1)|string) -%}
        {%- set _ = graphs_list.append(id) -%}
    {%- endfor %}
    html.Div(children={{ graphs_list | replace("'","") }}, style={'display': 'flex', 'flex-direction': 'row'}),
{% endfor -%}
])

if __name__ == '__main__':
    app.run_server(debug=True)
"""

code_tpl = Template(content)
code_str = code_tpl.render(**conf)


env = args_dict.get('environment')
if env == 'dev':
    tree = ast.parse(code_str)
    code = compile(tree, '<string>', 'exec')
    exec(code)
elif env == 'prod':
    print(code_str)