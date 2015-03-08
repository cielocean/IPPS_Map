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

filename = 'Inpatient_Prospective_Payment_System__IPPS__Provider_Summary_for_the_Top_100_Diagnosis-Related_Groups__DRG__-_FY2011.csv'

x_range = Range1d()
y_range = Range1d()
lat_data = []
lon_data = []
size = []
fill = []
DRG_list = []

class Procedure(object):
    def __init__ (self, location = object['Provider Name'] + " " + object['Provider Street Address'], total_payments = object[' Average Total Payments '], total_discharges = object[' Total Discharges']):
        self.location = location
        self.total_payments = total_payments
        self.total_discharges = total_discharges

    #
    def get_latlon():
        results = Geocoder.geocode(self.location)
        return [results[0].coordinates[0],results[0].coordinates[1]]

    #
    def get_size():
        total_pay = self.total_payments.strip('$')
        size = float(total_pay)/800
        return size

    #translate number of discharges to a greyscale color
    def get_color():
        if float(self.total_discharges) > 100:
            color = 1
        else:
            color = float(discharges)/100
        return str(color)


with open(filename) as fp:
    reader = csv.DictReader(fp)
    for line in reader:
        if line.get('DRG Definition') not in DRG_list:
            DRG_list.append(line.get('DRG Definition'))
    print(DRG_list)
    fp.seek(0)
    #Go through each line and update appropriate lists with necessary information
    for line in reader:
        point  = Procedure(line)
        lat.append(point.get_lat())
        lon.append(point.get_lon())
        size.append(point.get_size())
        fill.append(point.get_color())


map_options = GMapOptions(lat=30.2861, lng=-97.7394, zoom=15)

plot = GMapPlot(
    x_range=x_range, y_range=y_range,
    map_options=map_options,
    title = "Austin"
)
plot.map_options.map_type="hybrid"

source = ColumnDataSource(
    data=dict(
        lat=lat_data
        lon=lon_data
        size=size_data
        fill=fill_data
    )
)

#create all the points based on source data
circle = Circle(x="lon", y="lat", size="size", fill_color="fill", line_color="black")
plot.add_glyph(source, circle)

#set and add interactive tools
pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()
hover = HoverTool()
hover.tooltips = [
    ("index","$index"),
    ("(lat,lon)","$x,$y"),
    ("size","@size"),
    ("Number of Discharges","@fill")
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