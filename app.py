# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import os
from zipfile import ZipFile
import urllib.parse
from flask import Flask

import pandas as pd
import requests


server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

NAVBAR = dbc.Navbar(
    children=[
        dbc.NavbarBrand(
            html.Img(src="https://gnps-cytoscape.ucsd.edu/static/img/GNPS_logo.png", width="120px"),
            href="https://gnps.ucsd.edu"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("GNPS Classical Networking Group Comparison Dashboard", href="#")),
            ],
        navbar=True)
    ],
    color="light",
    dark=False,
    sticky="top",
)

DASHBOARD = [
    dbc.CardHeader(html.H5("GNPS Classical Networking Group Comparison Dashboard")),
    dbc.CardBody(
        [   
            dcc.Location(id='url', refresh=False),

            html.Div(id='version', children="Version - Release_1"),

            html.Br(),
            dbc.Textarea(className="mb-3", id='gnps_task', placeholder="Enter GNPS Task ID"),
            html.Br(),
            
            html.H2(children='Metadata Selection'),
            dcc.Dropdown(
                id="metadata_columns",
                options=[{"label" : "Default", "value": "Default"}],
                multi=False
            ),
            dcc.Loading(
                id="upset_plot",
                children=[html.Div([html.Div(id="loading-output-4")])],
                type="default",
            )
        ]
    )
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(DASHBOARD)),], style={"marginTop": 30}),
    ],
    className="mt-12",
)

app.layout = html.Div(children=[NAVBAR, BODY])


# This enables parsing the URL to shove a task into the qemistree id
@app.callback(Output('gnps_task', 'value'),
              [Input('url', 'pathname')])
def determine_task(pathname):
    # Otherwise, lets use the url
    if pathname is not None and len(pathname) > 1:
        return pathname[1:]
    else:
        return dash.no_update

@app.callback(Output('metadata_columns', 'options'),
              [Input('gnps_task', 'value')])
def determine_columns(gnps_task):
    # Otherwise, lets use the url
    if gnps_task is not None and len(gnps_task) > 1:
        url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file=metadata_merged/".format(gnps_task)
        df = pd.read_csv(url, sep="\t")
        acceptable_columns = [column for column in df.columns if "ATTRIBUTE_" in column]
        output_options = []
        for column in acceptable_columns:
            output_options.append({"label" : column, "value": column})
        return output_options
    else:
        return [{"label" : "X", "value": "Y"}]


# This function will rerun at any time that the selection is updated for column
@app.callback(
    [Output('upset_plot', 'children')],
    [Input('metadata_columns', 'value'), Input('gnps_task', 'value')],
)
def create_plot(gnps_task, metadata_column):
    url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file=metadata_merged/".format(gnps_task)
    return [url + ":" + metadata_column]

# This function will rerun at any 
# @app.callback(
#     [Output('library-mz-histogram', 'children'), Output('library-instrument-histogram', 'children'), Output('library-table', 'children')],
#     [Input('library-filter', 'value')],
# )
# def filter_library_histogram(search_values):

#     filtered_df = library_df[library_df["library_membership"].isin(search_values)]
#     fig1 = px.histogram(filtered_df, x="Precursor_MZ", color="library_membership")
#     fig1.update_layout(
#         autosize=True,
#         height=600,
#     )

#     fig2 = px.histogram(filtered_df, x="Instrument")
#     fig2.update_layout(
#         autosize=True,
#         height=600,
#     )

#     white_list_columns = ["spectrum_id", "library_membership", "Compound_Name", "Ion_Source", "Instrument", "create_time", "Precursor_MZ"]
#     table_fig = dash_table.DataTable(
#         columns=[
#             {"name": i, "id": i, "deletable": True, "selectable": True} for i in white_list_columns
#         ],
#         data=filtered_df.to_dict('records'),
#         editable=True,
#         filter_action="native",
#         sort_action="native",
#         sort_mode="multi",
#         column_selectable="single",
#         row_selectable="multi",
#         row_deletable=True,
#         selected_columns=[],
#         selected_rows=[],
#         page_action="native",
#         page_current= 0,
#         page_size= 10,
#     )

#     import gc
#     del filtered_df
#     gc.collect()

#     return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2), table_fig]

if __name__ == "__main__":
    app.run_server(debug=True, port=5000, host="0.0.0.0")
