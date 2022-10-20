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