from repository import Repository as repo
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.models import (AnnularWedge, ColumnDataSource,
                          Legend, LegendItem, Plot, Range1d)
from math import radians

def graph_donut(request):
    xdr = Range1d(start=-2, end=2)
    ydr = Range1d(start=-2, end=2)
    
    # Setup plot
    plot = Plot(x_range=xdr, y_range=ydr)
    plot.title.text = "Budget"
    plot.toolbar_location = None
    
    # Data
    current_prices = repo.get_current_prices()
    parts = repo.get_parts()
    price_list = []
    for part in parts:
        lowest_value = 0
        for price in current_prices:
            if part.part_id == price.part_id and price.price > lowest_value:
                lowest_value = price.price
        price_list.append(lowest_value)

    # calculations needed here
    percentages = []
    
    colors = {
        "googling" : "red",
        "daydreaming" : "blue",
         "coding" : "green",
         "fixing bugs" : "yellow",
         "reading the assignment" : "tan"
    }
    
    angles = []
    for count, percent in enumerate(percentages):
        angles.append(radians((percent /100) * 360))
        if count != 0:
            angles[count] += angles[count -1]

    activity_source = ColumnDataSource(dict(
        start = [0] + angles[:-1],
        end   = angles,
        colors = list(colors.values())
    ))
    
    # Create glyph with chart data and add to plot
    glyph = AnnularWedge(x=0, y=0, inner_radius=0.9, outer_radius=1.8,
                         start_angle_units="rad", start_angle="start", end_angle="end",
                         line_color="white", line_width=3, fill_color="colors")
    
    r = plot.add_glyph(activity_source, glyph)
    
    # Configure legend
    legend = Legend(location="center")
    for i, name in enumerate(colors):
        legend.items.append(LegendItem(label=name, renderers=[r], index=i))
    plot.add_layout(legend, "center")

    # Create web components
    script, div = components(plot, CDN)
    title = "Donut Graph"

    return render(request, "graph/index.html", {"the_script": script, "the_div": div, "title" : title})