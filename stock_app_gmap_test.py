from __future__ import print_function

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle
from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource, LinearAxis,
    PanTool, WheelZoomTool, BoxSelectTool,
    BoxSelectionOverlay, GMapOptions,
    NumeralTickFormatter, PrintfTickFormatter, HoverTool)
from bokeh.resources import INLINE
import pandas as pd
import csv
import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Select, TextInput, VBoxForm

x_range = Range1d()
y_range = Range1d()

filename = 'Data/IPPSlatlon'

# def get_data (ticker):
#     with open(filename) as fp:
#         reader = csv.DictReader(fp)
#         fp.seek(0)

#         complist=[]
#         data={}
#         for line in reader:
#             if line['DRG Definition'] == ticker:
#                 complist.append(line)
#         for key in complist[0].iterkeys():
#             data[key] = [data[key] for data in complist]
#         return data
base = {"Provider Id": [], "Provider Name": [], "Provider Street Address": [], "Provider City": [], "Provider State": [], "Provider Zip Code": [], "Hospital Referral Region Description": [], "Total Discharges": [], "Average Covered Charges": [], "Average Total Payments": [], "Average Medicare Payments": [], "Latitude": [], "Longtitude": []}
keys = ["Provider Id","Provider Name","Provider Street Address","Provider City","Provider State","Provider Zip Code","Hospital Referral Region Description","Total Discharges","Average Covered Charges","Average Total Payments","Average Medicare Payments","Latitude","Longtitude"]

with open(filename) as f:
    reader = csv.DictReader(f)
    data = {}
    for line in reader:
        drgDict = data.get(line['DRG Definition'], base.copy())
        for key in keys:
            drgDict[key].append(line[key])
        data[line['DRG Definition']] = drgDict

# with open(filename) as fp:
    # reader = csv.DictReader(fp)
    # fp.seek(0)

    # complist=[]
    # data={}
    # for line in reader:
    #     if line['DRG Definition'] not in data:
    #         data[line['DRG Definition']] = []
    # for key in complist[0].iterkeys():
    #     data[key] = [data[key] for data in complist]
    # return data

    # for key in blank:
    #     data[key] =      
    #     ColumnDataSource(
    #         data=dict(
    #             lat = [float(i) for i in data['Latitude']],
    #             lon = [float(i) for i in data['Longtitude']],
    #             DRG = data['DRG Definition'],
    #             name = data['Provider Name'],
    #             referral = data['Hospital Referral Region Description'],
    #             discharges = data[' Total Discharges '],
    #             covered = data[' Average Covered Charges '],
    #             payments_total = data[' Average Total Payments '],
    #             payments_medical = data['Average Medicare Payments'],
    #             street = data['Provider Street Address'],
    #             city = data['Provider City'],
    #             state = data['Provider State']
    #         )
    #     )

# data = get_data('039 - EXTRACRANIAL PROCEDURES W/O CC/MCC')

class GMapApp(HBox):
    """  Browser-based, interactive plot with ticker controls"""

    extra_generated_classes = [["GMapApp", "GMapApp", "HBox"]]

    plot = Instance(Plot)

    #data source
    source = Instance(ColumnDataSource)

    #inputs
    # ticker = Instance(Select)
    # input_box = Instance(VBoxForm)

    @classmethod
    def create(cls):
        """
        Create all the app objects

        Called once, and is responsible for creating all objects
        """

        obj = cls()

        obj.source = data['039 - EXTRACRANIAL PROCEDURES W/O CC/MCC']

        obj.ticker = Select(
            name='DRG Definition',
            value='039 - EXTRACRANIAL PROCEDURES W/O CC/MCC',
            options=['039 - EXTRACRANIAL PROCEDURES W/O CC/MCC', 
            '057 - DEGENERATIVE NERVOUS SYSTEM DISORDERS W/O MCC',
            '064 - INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION W MCC', 
            '065 - INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION W CC']
        )


        map_options = GMapOptions(lat=30.2861, lng=-97.7394, zoom=15)

        #create a GMap plot
        plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title = "IPPS"
        )

        #Plot all data from source
        circle = Circle(x='lon', y='lat', size=15, fill_color="blue", line_color="black")
        plot.add_glyph(obj.source, circle)

        #set and add interactive tools
        pan = PanTool()
        wheel_zoom = WheelZoomTool()
        box_select = BoxSelectTool()
        hover = HoverTool()
        hover.tooltips = [
            ("index","$index"),
            ("lat,lon","$x,$y"),
            ("cost","@payments_total"),
            ("Number of Discharges","@discharges")
        ]
        plot.add_tools(pan, wheel_zoom, box_select,hover)

        #set Axis
        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        plot.add_layout(xaxis, 'below')
        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        plot.add_layout(yaxis, 'left')

        #add overlay to plot
        overlay = BoxSelectionOverlay(tool=box_select)
        plot.add_layout(overlay)

        obj.plot = plot
        # obj.update_data()

        # obj.inputs = VBoxForm(
        #     children = [
        #         obj.ticker
        #     ]
        # )

        # obj.children.append(obj.inputs)
        # obj.children.append(obj.plot)

    # def setup_events(self):
    #     """
    #     """
    #     super(GMapApp,self).setup_events()
    #     # if self.source:
    #     #     self.source.on_change('selected', self, 'selection_change')
    #     # if self.ticker_select:
    #     #     self.ticker_select.on_change('value',self,'input_change')

    #     # #Ticker event registration
    #     if self.ticker:
    #         self.ticker.on_change('value',self,'input_changes')
    #     #getattr(self,"DRG Definition").on_change('value',self,'input_change')

    # def input_changes(self, obj, attrname, old, new):
    #     """Executes when input ticker input_changes

    #     Will update anything you want, in this case the GMapPlot

    #     Args:
    #         obj: the object that changed
    #         attrname: the attr that changed
    #         old: old value of attr
    #         new: new value of attr

    #     """
    #     self.update_data()
    
    # def update_data(self):
    #     """
    #     """
        #Get current ticker value
        # a = self.ticker.value

        # self.source = data[a]


@bokeh_app.route("/bokeh/sliders/")
@object_page("sin")
def make_sliders():
    app = GMapApp.create()
    return app


if __name__ == "__main__":
    GMapApp.create()