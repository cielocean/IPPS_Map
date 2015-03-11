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
import csv
import pandas as pd

filename = 'Data/IPPSlatlon'
"""Importing data file as class 'pandas.core.frame.DataFrame'"""
csvdata = pd.read_csv(filename)
"""Adding data files as lists (one list for each header) in dictionary"""
data ={}
for key in csvdata:
    data[key] = []
    for i in csvdata.get(key):
        data[key].append(i)

class GMap(object):

    """
    This class will create a new GMap object
    Inputs:
        map_title
        data
        x_range
        y_range
    """
    def __init__(self,map_title,data,x_range,y_range):
        self.data = data
        self.x_range = x_range
        self.y_range = y_range
        self.map_options = GMapOptions(lat=self.data['Latitude'][0], lng=self.data['Longtitude'][0], zoom=13)
        self.plot = GMapPlot(
            x_range=self.x_range, y_range=self.y_range,
            map_options = self.map_options,
            title = map_title
        )
        pass

    def set_tools(self):
        """
            Method will set tools for the plot
        """

        """Set and add interactive tools"""
        self.pan = PanTool()
        self.wheel_zoom = WheelZoomTool()
        self.box_select = BoxSelectTool()
        self.hover = HoverTool()
        """Specify What is Displayed"""
        self.hover.tooltips = [
            ("Procedure",'@DRG'),
            ("Zip Code"," @state @zip"),
            ("Average Total Payments","@payments_total"),
            ("Number of Discharges","@discharges")
        ]

        self.plot.add_tools(self.pan, self.wheel_zoom, self.box_select, self.hover)

    def set_plot_options(self,x_location,y_location):
        """
        Method takes in where you want to put the axes
        """
        #set x and y axis
        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        self.plot.add_layout(xaxis, x_location)
        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        self.plot.add_layout(yaxis, y_location)
            
    def make_plot(self):
        """
        Creates the Plot
        """
        self.set_tools()
        self.set_plot_options('below','left')
        source = ColumnDataSource(
            data=dict(
                lat = self.data['Latitude'],
                lon = self.data['Longtitude'],
                DRG = [x.lower() for x in self.data['DRG Definition'] ],
                name = self.data['Provider Name'],
                referral = self.data['Hospital Referral Region Description'],
                discharges = self.data['Total Discharges'],
                covered = self.data['Average Covered Charges'],
                payments_total = self.data['Average Total Payments'],
                payments_medical = self.data['Average Medicare Payments'],
                street = self.data['Provider Street Address'],
                city = self.data['Provider City'],
                state = self.data['Provider State'],
                zip = self.data['Provider Zip Code']
            )
        )

        #create all the points based on source data
        circle = Circle(x='lon', y='lat', size=10, fill_color="red", line_color="white", line_width = 2)
        self.plot.add_glyph(source, circle)

        #create overlay
        overlay = BoxSelectionOverlay(tool=self.box_select)
        self.plot.add_layout(overlay)

    def create_GMap(self):
        """
        Builds the actual Google Map 
        """
        self.make_plot()
        self.doc = Document()
        self.doc.add(self.plot)
        

if __name__ == "__main__":
    IPPS_GMap = GMap("IPPS Map",data,Range1d(),Range1d())
    IPPS_GMap.create_GMap()
    doc = IPPS_GMap.doc
    filename = "maps.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "IPPS Map"))
    print("Wrote %s" % filename)
    view(filename)


