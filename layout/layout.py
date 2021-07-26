import dash_html_components as html
import dash_core_components as dcc
import uuid

from layout.sidebar.sidebar import sidebar
from flask import request


content = html.Div(id="page-content")

def layout():
    return html.Div([
        dcc.Location(id="url"), 
        sidebar,
        content,
        html.H6(f'{uuid.uuid4()}'),
        #html.H6(f'{vars(request) if request else "empty"}')
    ])