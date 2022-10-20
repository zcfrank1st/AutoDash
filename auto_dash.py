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

content = ''
with open('dash.py.tpl', 'rt') as f:
    content = f.read()

code_tpl = Template(content)
code_str = code_tpl.render(**conf)
pprint(code_str)

tree = ast.parse(code_str)
code = compile(tree, '<string>', 'exec')
exec(code)