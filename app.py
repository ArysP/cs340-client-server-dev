import logging
import urllib.parse

import dash
import dash_core_components as dcc
import dash_html_components as html
from bson.json_util import dumps
from dash.dependencies import Input, Output
from flask import Flask

from mongo import AnimalShelter

# Create the dash application
server = Flask(__name__)
logger = logging.getLogger(__name__)

app = dash.Dash(
    __name__,
    url_base_pathname="/module-five/",
    server=server,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)

# Declare the application interfaces
app.layout = html.Div(
    # Application has two input boxes, a submit button, a horizontal line and div for output
    [
        dcc.Input(
            id="input_user".format("text"), type="text", placeholder="input type {}".format("text")
        ),
        dcc.Input(
            id="input_passwd".format("password"),
            type="password",
            placeholder="input type {}".format("password"),
        ),
        html.Button("Execute", id="submit_val", n_clicks=0),
        html.Hr(),
        html.Div(id="query_out"),
        html.H1("Arys Pena SNHU CS-340 Module 5 MongoDB Authentication"),
    ]
)


# Define application responses/callback routines
@app.callback(
    Output("query_out", "children"),
    [
        Input("input_user".format("text"), "value"),
        Input("input_passwd".format("password"), "value"),
        Input("submit_val", "n_clicks"),
    ],
    [dash.dependencies.State("input_passwd", "value")],
)
def cb_render(user_value, pass_value, n_clicks, button_value) -> str:
    """
    Take the entered text and if the submit button is clicked then call the mongo database
    with the find_one query and return the result to the output div.

    :param user_value: Username string
    :param pass_value: Password string
    :param n_clicks: If submit button is clicked
    :param button_value: not used.
    :return: Output div populated with database results
    """
    if n_clicks > 0:
        # Data Manipulation / Model use CRUD module to access MongoDB
        username = urllib.parse.quote_plus(user_value)
        password = urllib.parse.quote_plus(pass_value)

        # Instantiate CRUD object with above authentication username and password values
        aac = AnimalShelter()
        logger.info(f"Connected to {aac.database.name} Database for {username}.")

        # MongoDB returns BSON, the pyMongo JSON utility function dumps is used to convert to text
        # Return example query results
        dictionary_data = {"animal_type": "Dog", "name": "Lucy"}
        results = aac.read(dictionary_data)
        json_str = dumps(list(results))
        return json_str


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
