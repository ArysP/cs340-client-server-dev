import base64
import logging

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask import Flask

from mongo import AnimalShelter

# Create the dash application
server = Flask(__name__)
logger = logging.getLogger(__name__)

app = dash.Dash(
    __name__,
    url_base_pathname="/animal-shelter/",
    server=server,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)


# username and password and CRUD Python module name
username = "accuser"
password = "aacuserpass"
aac = AnimalShelter(username, password)
logger.info(f"Connected to {aac.database.name} Database")  # for {username}.")

# Add in Grazioso Salvare’s logo
image_filename = "data/GraziosoSalvareLogo.png"  # replace with your own image
encoded_image_logo = base64.b64encode(open(image_filename, "rb").read())

image_filename = "data/australian_shepherd.jpg"  # replace with your own image
encoded_image_dog = base64.b64encode(open(image_filename, "rb").read())


query = aac.read_all()
df = pd.DataFrame.from_records(query)

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
        html.Div(id="hidden_div", style={"display": "none"}),
        # Use row and col to control vertical alignment of logo / brand
        html.Div(
            [
                dbc.Col(
                    [
                        html.A(
                            [
                                html.Img(
                                    src="data:image/png;base64,{}".format(
                                        encoded_image_logo.decode()
                                    ),
                                    style={"height": "2" "00px"},
                                )
                            ],
                            href="https://www.snhu.edu",
                        ),
                        html.Img(
                            src="data:image/png;base64,{}".format(encoded_image_dog.decode()),
                            style={"height": "2" "00px"},
                            className="align-right",
                        ),
                        html.H4(
                            children="Created by Arys Pena",
                            style={"textAlign": "right", "color": "white"},
                        ),
                        html.B(
                            html.Center(
                                [
                                    html.H1(
                                        "Grazioso Salvare Animal Shelter Web Application Dashboard"
                                    ),
                                    html.H3("Web Application Dashboard"),
                                ]
                            ),
                            style={"color": "white"},
                        ),
                    ],
                    className="col-6",
                ),
            ],
            style={
                "height": "auto",
                "width": "auto",
                "backgroundColor": "#0067b9",
                # "align-items": "center",
            },
        ),
        html.Hr(),
        dcc.RadioItems(
            id="radio_items_id",
            options=[
                {"label": "Water Rescue", "value": "WR"},
                {"label": "Mountain Rescue", "value": "MR"},
                {"label": "Disaster Rescue", "value": "DR"},
                {"label": "Reset", "value": "R"},
            ],
            value="R",
            labelStyle={"display": "inline-block"},
        ),
        dash_table.DataTable(
            id="datatable_id",
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            # data=df.to_dict("records"),
            editable=False,
            filter_action="native",
            # FIXME: Set up the features for your interactive data table to make it user-friendly for your client
        ),
        html.Br(),
        html.Hr(),
        html.Div(id="map_id", className="col s12 m6",),
    ]
)


#############################################
# Interaction Between Components / Controller
#############################################
# This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output("datatable_id", "style_data_conditional"), [Input("datatable_id", "selected_columns")]
)
def update_styles(selected_columns):
    return [{"if": {"column_id": i}, "background_color": "#D2F3FF"} for i in selected_columns]


@app.callback(Output("datatable_id", "data"), [Input("radio_items_id", "value")])
def update_datatable(value):
    if value == "R":
        df = pd.DataFrame.from_records(aac.read_all()).to_dict("records")
        print("Reset button pressed")
        return df
    if value == "WR":
        df = pd.DataFrame.from_records(aac.filter_water_rescue())
        print(f"Filtered to Water Rescue {df.head(5)}")
        return df.to_dict("records")
    if value == "MR":
        df = pd.DataFrame.from_records(aac.filter_mountain_wilderness())
        print(f"Filtered to Mountain Rescue {df.head(5)}")
        return df.to_dict("records")
    if value == "DR":
        df = pd.DataFrame.from_records(aac.filter_disaster_rescue_tracking())
        print(f"Filtered to Diasater Rescue {df.head(5)}")
        return df.to_dict("records")


@app.callback(
    Output("map_id", "children"),
    [Input("radio_items_id", "value"), Input("datatable_id", "derived_viewport_data")],
)
def update_map(value, view_data):
    if value == "R":
        dff = pd.DataFrame.from_dict(view_data)
        return []
    dff = pd.DataFrame.from_dict(view_data)
    return [
        dl.Map(
            style={"width": "1000px", "height": "500px"},
            center=[30.75, -97.48],
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),
                # Marker with tool tip and popup
                dl.Marker(
                    position=[30.75, -97.48],
                    children=[
                        dl.Tooltip(dff.iloc[0, 4]),
                        dl.Popup([html.H1("Animal Name"), html.P(dff.iloc[1, 9])]),
                    ],
                ),
            ],
        )
    ]


# Define application responses/callback routines
# @app.callback(
#     Output("query_out", "children"),
#     [
#         Input("input_user".format("text"), "value"),
#         Input("input_passwd".format("password"), "value"),
#         Input("submit_val", "n_clicks"),
#     ],
#     [dash.dependencies.State("input_passwd", "value")],
# )
# def cb_render(user_value, pass_value, n_clicks, button_value) -> str:
#     """
#     Take the entered text and if the submit button is clicked then call the mongo database
#     with the find_one query and return the result to the output div.
#
#     :param user_value: Username string
#     :param pass_value: Password string
#     :param n_clicks: If submit button is clicked
#     :param button_value: not used.
#     :return: Output div populated with database results
#     """
#     if n_clicks > 0:
#         # Data Manipulation / Model use CRUD module to access MongoDB
#         username = urllib.parse.quote_plus(user_value)
#         password = urllib.parse.quote_plus(pass_value)
#
#         # Instantiate CRUD object with above authentication username and password values
#         aac = AnimalShelter()
#         logger.info(f"Connected to {aac.database.name} Database for {username}.")
#
#         # MongoDB returns BSON, the pyMongo JSON utility function dumps is used to convert to text
#         # Return example query results
#         dictionary_data = {"animal_type": "Dog", "name": "Lucy"}
#         results = aac.read(dictionary_data)
#         json_str = dumps(list(results))
#         return json_str


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
