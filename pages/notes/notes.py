import dash_html_components as html


def layout(*args, **kwargs):
    return html.Div([
        html.P(f"ARGS: {args}"),
        html.P(f"KWARGS: {kwargs}")
    ])