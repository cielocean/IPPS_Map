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
#from pygeocoder import Geocoder
import csv
import pandas as pd

filename = 'Data/IPPSlatlon'

x_range = Range1d()
y_range = Range1d()


"""Importing data file as class 'pandas.core.frame.DataFrame'"""
csvdata = pd.read_csv(
    filename
    )

"""Adding data files as lists in dictionary"""
header=[]
data ={}

for line in csvdata:
    header.append(line)
print (header)
for key in header:
    data[key] = []

for key in data.iterkeys():
    for i in csvdata.get(key):
        data[key].append(i)


map_options = GMapOptions(lat=data['Latitude'][0], lng=data['Longtitude'][0], zoom=15)

plot = GMapPlot(
    x_range=x_range, y_range=y_range,
    map_options=map_options,
    title = "IPPS"
)
plot.map_options.map_type="hybrid"

source = ColumnDataSource(
    data=dict(
        lat = data['Latitude'],
        lon = data['Longtitude'],
        DRG = data['DRG Definition'],
        name = data['Provider Name'],
        referral = data['Hospital Referral Region Description'],
        discharges = data[' Total Discharges '],
        covered = data[' Average Covered Charges '],
        payments_total = data[' Average Total Payments '],
        payments_medical = data['Average Medicare Payments'],
        street = data['Provider Street Address'],
        city = data['Provider City'],
        state = data['Provider State']
    )
)

#create all the points based on source data
circle = Circle(x='lon', y='lat', size=15, fill_color="blue", line_color="black")
plot.add_glyph(source, circle)

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

doc = Document()
doc.add(plot)

if __name__ == "__main__":
    filename = "maps.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Google Maps Example"))
    print("Wrote %s" % filename)
    view(filename)