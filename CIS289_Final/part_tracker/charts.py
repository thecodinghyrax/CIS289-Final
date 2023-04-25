from .repository import Repository
from bokeh.palettes import Sunset
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.resources import CDN
from bokeh.plotting import figure, show
from bokeh.models import (AnnularWedge, ColumnDataSource,
                          Legend, LegendItem, Plot, Range1d)
from math import radians
from datetime import datetime as dt

class BudgetGraph:
    def __init__(self):
        self.repo = Repository()
        self.current_prices_data = self.repo.get_lowest_catagory_prices()

        
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
        catagory = self.repo.get_catagories()
        for cata in catagory:
            self.make_line_chart(self.repo.get_prices_by_catagory(cata))
            
        # prices = list(self.repo.get_prices())
        # print(prices[0])
    def make_line_chart(self, data):
        # print(data['part__catagory__name'][0])
        if data['part__catagory__name'][0] == "Motherboard":
            data_list = []
            dates_prices = data.groupby('part_id').agg({'date': list, 'price': list})
            for col in dates_prices:
                data_list.append(list(dates_prices[col]))

            p = figure(title='Price over time', toolbar_location=None, width=600, height=200, x_axis_type='datetime', x_axis_label='Date', y_axis_label='Price')
            
            p.multi_line()
            for item in range(len(data_list[0])):
                p.line(x=data_list[0][item], y=data_list[1][item])
                
            # print(len(dates_prices), "\n")
            # print(dates_prices.index)
            # print(dates_prices.iloc[[0]]['date'])
            # chart_data = { 'date' : [], 'price' : [] }
   
            # mydict= dates_prices.to_dict()
            # print(mydict['date'])
            # print()
            # print(mydict['price'])
            # source = ColumnDataSource(dates_prices)
            # source = ColumnDataSource(dates_prices.iloc[[0]])
            curdoc().theme = "dark_minimal"
            # x = list(dates_prices.iloc[[0]]['date'])
            # y = list(dates_prices.iloc[[0]]['price'])
            # p.line(x=, y[0], source=source)

            # p.line(x='date', y='price2', source=source)
            # filename = f"{data['part__catagory__name'][0]}.png"

            show(p)

    
if __name__ == "__main__":
    pass