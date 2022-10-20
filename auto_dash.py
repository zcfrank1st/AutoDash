import yaml
from jinja2 import Template
import ast

from pprint import pprint

dash_conf = """
info:
    title: 'Test'
    sub_title: 'test'
layout:
    row: 2
    column: 1
sources:
    - postgres:
        host: 1 
        port: 1
        user: 1
        passwd: 1
        data_handle: 'pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],"Amount": [4, 1, 2, 2, 4, 5],"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})'
    - postgres:
        host: 1 
        port: 1
        user: 1
        passwd: 1
        data_handle: 'pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],"Amount": [4, 1, 2, 2, 4, 5],"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})'
graphs:
    - bar:
        x: 'Fruit'
        y: 'Amount'
        color: 'City'
        barmode: 'group'
    - bar:
        x: 'Fruit'
        y: 'Amount'
        color: 'City'
        barmode: 'group'

"""

conf = yaml.safe_load(dash_conf)

content = """
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

header = html.H1(children='{{ info.title }}', style={'flex': 1})
sub_header = html.Div(children='{{ info.sub_title }}', style={'flex': 1})


{% for source in sources %}
{% set sindex = loop.index %}
    {% for skey in source.keys() %}
df_{{sindex}} = {{ source[skey].data_handle }}
    {% endfor %}
{% endfor%}

{% for graph in graphs %}
{% set gindex = loop.index %}
    {% for gkey in graph %}
fig_{{gindex}} = px.{{ gkey }}(df_{{gindex}}, **conf.get('graphs')[{{gindex - 1}}].get('{{ gkey }}'))
graph_{{gindex}} = dcc.Graph(id='fig_{{gindex}}',figure=fig_{{gindex}})
    {% endfor %}
{% endfor %}

app.layout = html.Div(children=[
    header,
    sub_header,

{% for n_row in range(layout.row) %}
    {% set graphs_list = [] %}
    {% for n_col in range(n_row * layout.column, (n_row+1) * layout.column) %}
        {% set id = 'graph_'~((n_col+1)|string) %}
        {% set _ = graphs_list.append(id) %}
    {% endfor %}
    html.Div(children={{ graphs_list | replace("'","") }}, style={'display': 'flex', 'flex-direction': 'row'}),
{% endfor %}

], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True)
"""

code_tpl = Template(content)
code_str = code_tpl.render(**conf)
pprint(code_str)

tree = ast.parse(code_str)
code = compile(tree, '<string>', 'exec')
exec(code)