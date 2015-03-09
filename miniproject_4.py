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

filename = 'Data/IPPSlatlon'

x_range = Range1d()
y_range = Range1d()
lat_data = []
lon_data = []
size_data = []
fill_data = []
total_discharges_data =[]
total_cost_data  = []

with open(filename) as fp:
    reader = csv.DictReader(fp)
    fp.seek(0)
    #Go through each line and update appropriate lists with necessary information
    for i,line in enumerate(reader):
        if i == 0:
            continue 
        lat_data.append(float(line['Latitude']))
        lon_data.append(float(line['Longtitude']))
        size_data.append(15)
        fill_data.append('blue')
        total_discharges_data.append(line[' Total Discharges '])
        total_cost_data.append(line[' Average Total Payments '])

map_options = GMapOptions(lat=30.2861, lng=-97.7394, zoom=15)

plot = GMapPlot(
    x_range=x_range, y_range=y_range,
    map_options=map_options,
    title = "Austin"
)
plot.map_options.map_type="hybrid"
print("lat ", lat_data[:10])
print("lon ", lon_data[:10])
print("size ", size_data[:10])

source = ColumnDataSource(
    data=dict(
        lat = lat_data,
        lon = lon_data,
        size = size_data,
        fill = fill_data,
        total_discharges = total_discharges_data,
        total_cost = total_cost_data,
    )
)

# source = ColumnDataSource(
#     data=dict(
#         lat=[30.2861, 30.2855, 30.2869],
#         lon=[-97.7394, -97.7390, -97.7405],
#         fill=['orange', 'blue', 'green']
#     )
# )

#circle = Circle(x="lon", y="lat", size=15, fill_color="fill", line_color="black")


#create all the points based on source data
circle = Circle(x="lon", y="lat", size=15, fill_color="fill", line_color="black")
plot.add_glyph(source, circle)

#set and add interactive tools
pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()
hover = HoverTool()
hover.tooltips = [
    ("index","$index"),
    ("(lat,lon)","$x, $y"),
    ("Average Cost","@total_cost"),
    ("Number of Discharges","@total_discharges")
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