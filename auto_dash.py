import yaml
from jinja2 import Template
import ast

from pprint import pprint

dash_conf = """
title: ''
sub_title: ''
layout:
    row: 1
    column: 1
sources:
    - postgres: &pg
        host: 1 
        port: 1
        user: 1
        passwd: 1
        data_handle: pd.read
graphs:
    - bar: &bar
        x: 'Fruit'
        y: 'Amount'
        color: 'City'
        barmode: 'group'

"""

conf = yaml.safe_load(dash_conf)

content = ''
with open('dash.py.tpl', 'rt') as f:
    content = f.read()

code_tpl = Template(content)
code_str = code_tpl.render(**conf)
pprint(code_str)

tree = ast.parse(code_str)
code = compile(tree, 'dash', 'exec')
exec(code)