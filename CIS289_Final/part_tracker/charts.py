from .repository import Repository
from bokeh.palettes import Sunset, Category10
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, NumeralTickFormatter)
from math import radians
import threading

class BudgetGraph:
    def __init__(self, current_prices):
        self.repo = Repository()
        self.current_prices_data = self.repo.get_lowest_catagory_prices(current_prices)

        
    def graph_pie(self):
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
        
        p = figure(toolbar_location=None, tools="hover", 
                   tooltips="@components: @percentages")
        
        p.wedge(x=1, y=1, radius=1.0,
                start_angle="start", end_angle="end", line_color="white",
                fill_color="colors", source=source)
        
        p.background_fill_color = "black"
        p.border_fill_color = "black"
        p.outline_line_color = "black"
        p.sizing_mode = "scale_both"

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color= None

        script, div = components(p, CDN)

        return {"the_script": script, "the_div": div }
    
    def create_price_charts(self):
        '''
        This function gets all catagories from the db and creates a line chart for 
        each one. 
        :returns: A dictonary of all chart components
        '''
        catagory = self.repo.get_catagories()
        data_dict = dict()
        
        def update_charts(cata):
            data = self.repo.get_prices_by_catagory(cata)
            chart = self.make_line_chart(data)
            data_dict.update({cata.name : chart})
            
        for cata in catagory:
            thread = threading.Thread(target=update_charts, args=(cata,))
            thread.start()
            
        return data_dict

    def make_line_chart(self, data):
        data['float_price'] = (data['price'] * 0.01).round(2)
        data['name'] = [" ".join(x.split()[:5]) for x in data['part__long_name']]
        data_list = []
        dates_prices = data.groupby('part_id').agg({'date': list, 'float_price': list, 'name': list})
        for col in dates_prices:
            data_list.append(list(dates_prices[col]))
        num_lines = len(data_list[0])

        colors = Category10[num_lines + 3][:num_lines] 
        p = figure(width=1200, height=400, x_axis_type='datetime', toolbar_location=None)
        p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
        for item in range(len(colors)):
            p.line(x=data_list[0][item], y=data_list[1][item], line_color=colors[item], 
                        line_width=3, legend_label=data_list[2][item][0])

        p.legend.location = "top_left"
        p.background_fill_color = "black"
        p.border_fill_color = "black"
        p.outline_line_color = "black"
        p.sizing_mode = "scale_both"
        p.xaxis.major_label_text_color = "white"
        p.yaxis.major_label_text_color = "white"

        script, div = components(p, CDN, theme="dark_minimal")

        return script + div
    
if __name__ == "__main__":
    pass
