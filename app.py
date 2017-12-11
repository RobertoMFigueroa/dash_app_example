
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# 
# The dashboard will have two graphs: 
# 
#     The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
#     The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# In[4]:


import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[6]:


eurostat = pd.read_csv("nama_10_gdp_1_Data.csv")

indicators = eurostat['NA_ITEM'].unique()

countries = eurostat['GEO'].unique()

eurostat1 = eurostat[eurostat['UNIT'] == 'Current prices, million euro']


# Final dashboard

# In[7]:


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown( 
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in indicators],
                value='Imports of goods'
            )
        ],
        style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in countries]
            )
        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic-b'),
    
    html.Div([

        html.Div([
            dcc.Dropdown( 
                id='xaxis',
                options=[{'label': i, 'value': i} for i in indicators],
                value='Imports of goods'
            )
        ],
        style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis',
                options=[{'label': i, 'value': i} for i in indicators],
                value='Exports of goods'
            )
        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic-a'),
    
    
    dcc.Slider( 
        id='slider',
        min=eurostat['TIME'].min(),
        max=eurostat['TIME'].max(),
        value=eurostat['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eurostat['TIME'].unique()}
    )

])

@app.callback(
    dash.dependencies.Output('indicator-graphic-b', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
    
    eurostat_year2 = eurostat1[eurostat1['GEO'] == yaxis_column_name]
        
    return {
        'data': [go.Scatter(
            x=eurostat_year2['TIME'].unique(),
            y=eurostat_year2[eurostat_year2['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            line={'color': 'green'},
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic-a', 'figure'),
    [dash.dependencies.Input('xaxis', 'value'),
     dash.dependencies.Input('yaxis', 'value'),
     dash.dependencies.Input('slider', 'value')])

def update_graph(xaxis_name, yaxis_name, year_value):
    
    eurostat_year = eurostat[eurostat['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=eurostat_year[eurostat_year['NA_ITEM'] == xaxis_name]['Value'],
            y=eurostat_year[eurostat_year['NA_ITEM'] == yaxis_name]['Value'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }




if __name__ == '__main__':
    app.run_server()



# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell
