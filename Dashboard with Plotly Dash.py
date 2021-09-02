#Here you can find the code used to delevop the Dashboard with Plotly Dash

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options= [
                                            {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                            {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                            {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                            {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                            {'label':'All','value':'All'}
                                        ],
                                        placeholder='Select a Launch Site here'
                                    )
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0, 
                                    max = 10000, 
                                    step = 1000, 
                                    value = [min(spacex_df['Payload Mass (kg)']), max(spacex_df['Payload Mass (kg)'])],
                                    marks={
                                        0: '0',
                                        3000: '3000',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    }
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', component_property='figure'),
    [Input('site-dropdown', component_property='value')])

def pie_chart(value):
    if format(value) == 'All':
        fig = px.pie(spacex_df, values='class', names='Launch Site')
    else:
        df = spacex_df[spacex_df['Launch Site']==format(value)]
        fig = px.pie(df, names='class')

    return  fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', component_property='figure'),
    [Input('site-dropdown', component_property='value'),
    Input("payload-slider", component_property="value")])

def scatter_chart(value, values):
    if format(value) == 'All':
        df = spacex_df[ (spacex_df['Payload Mass (kg)'] >= min(values)) & (spacex_df['Payload Mass (kg)'] <= max(values))]
        fig2 = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
    else:
        df = spacex_df[(spacex_df['Launch Site']==format(value)) & (spacex_df['Payload Mass (kg)'] >= min(values)) & (spacex_df['Payload Mass (kg)'] <= max(values))]
        fig2 = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
    return  fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
