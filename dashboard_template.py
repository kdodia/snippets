# -*- coding: utf-8 -*-
"""Dashboard Template."""
from __future__ import absolute_import, division, print_function

# Imports
# -------

import argparse

# You might need these, you might not. Just a reminder.
# import pandas as pd
# import numpy as np

from time import sleep

import requests
from requests.exceptions import ConnectionError

# Most common Bokeh elements
from bokeh.plotting import *
# from bokeh.objects import ColumnDataSource, DataRange1d, HoverTool
# from bokeh.widgets import TableColumn, HandsonTable, HBox, VBox, TextInput, Paragraph, Slider

from bokeh.document import Document
from bokeh.session import Session

# Personal styling
from seabornify import seabornify


# Constants
# ---------

COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
BK_SERVER_PORT = 5006
DOC_NAME = "dashboard"


# Utility Functions
# -----------------

def parse_args():

    parser = argparse.ArgumentParser(
         description='Construct and display a new dashboard.')

    parser.add_argument("-p", "--port", type=int, default=BK_SERVER_PORT,
                        help="Match port of bokeh-server instance" +
                             "   (Default: %(default)s)")
    parser.add_argument("-d", "--doc", dest="doc_name", type=str, default=DOC_NAME,
                        help="Document name for this session" +
                             "   (Default: '%(default)s')")
    parser.add_argument("-s", "--show", action="store_true",
                        help="Auto-raise dashboard in a browser window")

    return parser.parse_args()


class Dashboard(object):
    """
    A collection of plots and widgets served by bokeh-server.
    """

    def __init__(self,
            port = BK_SERVER_PORT,
            doc_name = DOC_NAME,
            colors = COLORS,
            show = False,
        ):
        """
        Initialize Bokeh session and document.
        """

        self.document = Document()

        self.port = port
        self.show = show
        self.doc_name = doc_name

        name="http://localhost:{}/".format(port)
        root_url="http://localhost:{}/".format(port)

        # Initialize Session
        self.session = Session(load_from_config=False,
                               name=name,
                               root_url=root_url)

        try:
            self.session.use_doc(doc_name)
        except requests.ConnectionError as e:
            print("\nPlease start bokeh-sever on the command line to launch this dashboard.")
            exit(1)
        self.session.load_document(self.document)

        # Configuration
        self.colors = itertools.cycle(COLORS)


        # Initialize data sources, construct and store dashboard
        self.init_sources()
        self.document.add(self.construct())


# Sources
# -------

    def init_sources(self):
        """Initialize DataSource objects backing the dashboard elements."""

        columns = ['some', 'column', 'headers']
        self.columns = columns

        self.data_source = ColumnDataSource(data=dict(zip(columns, []*len(columns))))

# Construction
# ------------

    def construct(self):

        slider = self.slider()
        plot = self.plot()
        handson_table = self.handson_table()

        layout = VBox(children=[
            slider,
            plot,
            handson_table
            ])
        return layout

# Widgets
# -------

    def slider(self):
        slider = Slider(value=10, start=10, end=100, step=10, orientation="horizontal", title="Slider")
        slider.on_change('value', self.on_slider_change)

        return HBox(children=[slider], width=500)

    def on_slider_change(self, obj, attr, old, new):

    def handson_table(self):
        # Hands On Table Widget
        columns = [
            TableColumn(field="a", header="A"),
            TableColumn(field="b", header="B"),
            TableColumn(field="c", header="C"),
        ]

        return HandsonTable(source=self.data_source, columns=columns, width=800)

# Plots
# -----

    def plot(self):
        plot = curplot()
        hover = plot.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("type", " @type"),
        ])

        seabornify(plot)
        return plot

# Update Routine
# --------------

    def update(self):
        self.session.store_objects(self.data_source)

# Run
# ---

    def run(self, poll_interval=1):

        self.session.store_document(self.document)

        link = self.session.object_link(self.document.context)
        if self.show:
            import webbrowser
            webbrowser.open(link)
        else:
            print("Please visit %s to see the plots (press ctrl-C to exit)" % link)

        try:
            while True:
                self.session.load_document(self.document)
                sleep(poll_interval)
        except KeyboardInterrupt:
            print()
        except ConnectionError:
            print("Connection to bokeh-server was terminated.")

if __name__ == "__main__":

    args = parse_args()

    dashboard = Dashboard(**vars(args))
    dashboard.run()
