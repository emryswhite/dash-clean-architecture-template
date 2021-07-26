import enum
from layout.layout import layout
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from utils.constants import home_page_location, gdp_page_location, iris_page_location

from pages.home import home
from pages.gdp import gdp
from pages.iris import iris
from pages.notes import notes


import re
from urllib.parse import urlsplit
from typing import Callable, Dict, List, Tuple

class Route:
    """
    Attempts to be a very basic implementation of Django's url routing capability.

    Doesn't have the 

    One path defines one controller.

    Relies on us writing good regular expressions.

    If anything complex goes into the URls we will need to escape carefully.
    """
    def __init__(self, pattern: str, controller: Callable, name: str):
        try:
            self.regex = re.compile(pattern)
        except re.error as error:
            raise ValueError(f'Pattern {pattern} is not a valid regex: {error}')

        self.controller = controller
        self.name = name

    def match_path(self, candidate_url: str) -> Tuple[Callable, List, Dict]:
        """
        Test if the candidate is valid, extract any args and kwargs and return
        them with the controller.
        """
        match = self.regex.fullmatch(candidate_url)
        if match:
            keyword_positions = self.regex.groupindex
            positional_args = [
                g for i, g in enumerate(match.groups(), 1) 
                if i not in keyword_positions.values()
            ]
            return self.controller, positional_args, match.groupdict()


def path(pattern: str, controller: Callable, name: str=""):
    return Route(pattern, controller, name or f'{controller}: {pattern}')


def error(path):
     return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {path} was not recognised..."),
        ]
    )

urls = [
    path("/", home.layout, name='Home page'),
    path("/gdp", gdp.layout ,name='gpd-view'),
    path("/iris", iris.layout, name='iris-viewer'),
    path("/notes/(\w+)/(?P<gretta>\d+)", notes.layout, name='notes-viewer'),
]


def get_layout(path: str) -> Tuple[Callable, List, Dict]:
    components = urlsplit(path)
    matches = []
    for url in urls:
        match = url.match_path(components.path)
        if match:
            matches.append(match)
    if len(matches) > 1:
        raise ValueError(
            f'URLs are improperly configured - multiple matches found for {path}:'
            f'{matches}'
        )
    if not matches:
        return error(components.path)
    controller, _args, _kwargs = matches[0]
    return controller(*_args, **_kwargs)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return get_layout(pathname)