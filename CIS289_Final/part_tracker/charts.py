from .repository import Repository
from bokeh.palettes import Sunset
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.models import (AnnularWedge, ColumnDataSource,
                          Legend, LegendItem, Plot, Range1d)
from math import radians

class BudgetGraph:
    def __init__(self):
        self.repo = Repository()
        self.current_prices_data = self.repo.get_lowest_catagory_prices()

        
    def graph_donut(self):
        data = {
            'components' : list(self.current_prices_data['part__catagory__name'].values()),
            'percentages' : list(self.current_prices_data['percentage'].values())
            }
        
        angles = []
        for count, percent in enumerate(data['percentages']):
            angles.append(radians((percent / 100) * 360))
            if count != 0:
                angles[count] += angles[count -1]
        data['start'] = [0] + angles[:-1]
        data['end'] = angles
        data['colors'] = Sunset[len(data['components'])]
        
        source = ColumnDataSource(data=data)
        
        p = figure(title="Max Budget Breakdown", toolbar_location=None, 
                   tools="hover", tooltips="@components: @percentages")
        
        
        p.wedge(x=1, y=1, radius=0.4,
                start_angle="start", end_angle="end", line_color="white",
                fill_color="colors", legend_field="components", source=source)
                

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color= None

        script, div = components(p, CDN)

        return {"the_script": script, "the_div": div }
    
    def graph_donut2(self):
        xdr = Range1d(start=-2, end=2)
        ydr = Range1d(start=-2, end=2)
        
        # Setup plot
        plot = Plot(x_range=xdr, y_range=ydr)
        plot.title.text = "Percent of time spent on this assignment"
        plot.toolbar_location = None
        
        # Data
        percentages = [60, 5, 10, 29, 1]
        
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

        return {"the_script": script, "the_div": div, "title" : title}
    
    
if __name__ == "__main__":
    pass