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

filename = 'Data/test'

x_range = Range1d()
y_range = Range1d()

def get_data (ticker):
    with open(filename) as fp:
        reader = csv.DictReader(fp)
        fp.seek(0)

        complist=[]
        data={}
        for line in reader:
            print (line)
            if line['DRG Definition'] == ticker:
                complist.append(line)
        for key in complist[0].iterkeys():
            data[key] = [data[key] for data in complist]
        return data

data = get_data('039 - EXTRACRANIAL PROCEDURES W/O CC/MCC')
print(data)
map_options = GMapOptions(lat=float(data['Latitude'][0]), lng=float(data['Longtitude'][0]), zoom=15)

plot = GMapPlot(
    x_range=x_range, y_range=y_range,
    map_options=map_options,
    title = "IPPS"
)
plot.map_options.map_type="hybrid"

source = ColumnDataSource(
    data=dict(
        lat = [float(i) for i in data['Latitude']],
        lon = [float(i) for i in data['Longtitude']],
        DRG = data['DRG Definition'],
        name = data['Provider Name'],
        referral = data['Hospital Referral Region Description'],
        discharges = data[' Total Discharges '],
        covered = data[' Average Covered Charges '],
        payments_total = data[' Average Total Payments '],
        payments_medical = data['Average Medicare Payments'],
        street = data['Provider Street Address'],
        city = data['Provider City'],
        state = data['Provider State'],
        zip = data['Provider Zip Code']
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
    ("Zip Code"," @state @zip"),
    ("Average Total Payments","@payments_total"),
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