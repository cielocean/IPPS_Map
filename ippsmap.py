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
x_range = Range1d()
y_range = Range1d()


# """Importing data file as class 'pandas.core.frame.DataFrame'"""
# csvdata = pd.read_csv(filename)

# """Adding data files as lists (one list for each header) in dictionary"""
# data ={}
# for key in csvdata:
#     data[key] = []
#     for i in csvdata.get(key):
#         data[key].append(i)

class GMap(object):

    def __init__(self):
        """Importing data file as class 'pandas.core.frame.DataFrame'"""
        csvdata = pd.read_csv(filename)

        """Adding data files as lists (one list for each header) in dictionary"""
        data ={}
        for key in csvdata:
            data[key] = []
            for i in csvdata.get(key):
                data[key].append(i)
        self.data = data

        map_options = GMapOptions(lat=self.data['Latitude'][0], lng=self.data['Longtitude'][0], zoom=15)
        
        self.plot = GMapPlot(
            x_range=x_range, y_range=y_range,
            map_options=map_options,
            title = "IPPS"
        )

        self.source = ColumnDataSource(
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

    # def import_data(self):
    #     """Importing data file as class 'pandas.core.frame.DataFrame'"""
    #     csvdata = pd.read_csv(filename)

    #     """Adding data files as lists (one list for each header) in dictionary"""
    #     data ={}
    #     for key in csvdata:
    #         data[key] = []
    #         for i in csvdata.get(key):
    #             data[key].append(i)
    #     self.data = data
    #     return self.data

    def set_tools(self):
        """set and add interactive tools"""
        self.pan = PanTool()
        self.wheel_zoom = WheelZoomTool()
        self.box_select = BoxSelectTool()
        self.hover = HoverTool()

        """Specify What is Displayed"""
        self.hover.tooltips = [
            ("Procedure","@DRG"),
            ("Zip Code"," @state @zip"),
            ("Average Total Payments","@payments_total"),
            ("Number of Discharges","@discharges")
        ]

        self.plot.add_tools(self.pan, self.wheel_zoom, self.box_select,self.hover)

    def set_axis(self):
        # map_options = GMapOptions(lat=self.data['Latitude'][0], lng=self.data['Longtitude'][0], zoom=15)

        self.plot.map_options.map_type="hybrid"

        xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
        self.plot.add_layout(xaxis, 'below')
        yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
        self.plot.add_layout(yaxis, 'left')
            
    def make_plot(self):
        self.set_tools()
        self.set_axis()

        # self.plot = GMapPlot(
        #     x_range=x_range, y_range=y_range,
        #     map_options=map_options,
        #     title = "IPPS"
        # )

        #create all the points based on source data
        circle = Circle(x='lon', y='lat', size=15, fill_color="blue", line_color="black")
        self.plot.add_glyph(self.source, circle)


    def create_GMap(self):
        """
        Builds the actual map
        """
        # import_data()
        self.make_plot()

        overlay = BoxSelectionOverlay(tool=self.box_select)
        self.plot.add_layout(overlay)
        self.doc = Document()
        self.doc.add(self.plot)
        
        if __name__ == "__main__":
            filename = "maps.html"
            with open(filename, "w") as f:
                f.write(file_html(self.doc, INLINE, "Google Maps Example"))
            print("Wrote %s" % filename)
            view(filename)

# map_options = GMapOptions(lat=data['Latitude'][0], lng=data['Longtitude'][0], zoom=15)
# plot = GMapPlot(
#     x_range=x_range, y_range=y_range,
#     map_options=map_options,
#     title = "IPPS"
# )

# plot.map_options.map_type="hybrid"

# source = ColumnDataSource(
#     data=dict(
#         lat = data['Latitude'],
#         lon = data['Longtitude'],
#         DRG = [x.lower() for x in data['DRG Definition'] ],
#         name = data['Provider Name'],
#         referral = data['Hospital Referral Region Description'],
#         discharges = data['Total Discharges'],
#         covered = data['Average Covered Charges'],
#         payments_total = data['Average Total Payments'],
#         payments_medical = data['Average Medicare Payments'],
#         street = data['Provider Street Address'],
#         city = data['Provider City'],
#         state = data['Provider State'],
#         zip = data['Provider Zip Code']
#     )
# )
# #create all the points based on source data
# circle = Circle(x='lon', y='lat', size=15, fill_color="blue", line_color="black")
# plot.add_glyph(source, circle)

# """set and add interactive tools"""
# pan = PanTool()
# wheel_zoom = WheelZoomTool()
# box_select = BoxSelectTool()
# hover = HoverTool()

# hover.tooltips = [
#     ("Procedure",'@DRG'),
#     ("Zip Code"," @state @zip"),
#     ("Average Total Payments","@payments_total"),
#     ("Number of Discharges","@discharges")

# ]

# plot.add_tools(pan, wheel_zoom, box_select,hover)

#set Axis
# xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
# plot.add_layout(xaxis, 'below')
# yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
# plot.add_layout(yaxis, 'left')

# #add overlay to plot
# overlay = BoxSelectionOverlay(tool=box_select)
# plot.add_layout(overlay)
# doc = Document()
# doc.add(plot)

# if __name__ == "__main__":
#     filename = "maps.html"
#     with open(filename, "w") as f:
#         f.write(file_html(doc, INLINE, "Google Maps Example"))
#     print("Wrote %s" % filename)
#     view(filename)
IPPS_GMap = GMap()
IPPS_GMap.create_GMap()