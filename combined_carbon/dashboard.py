import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.title = "Carbon Footprint Saving Dashboard for Hardware Upgrade"

app.layout = html.Div([
    html.H1("Carbon Footprint Saving Dashboard for Hardware Upgrade", 
            style={
                'textAlign': 'center', 
                'color': '#507d50',
                'fontFamily': 'Arial, sans-serif',
                'marginTop': '20px',
                'marginBottom': '5px',
                'fontSize': '30px',
                'fontWeight': 'bold',
                'textShadow': '1px 1px #000'
            }),  
    html.Div([
        dcc.Graph(id='graph'),
        html.Div([
            html.Label('Carbon Intensity (gCO2/kWh): ', style={'fontSize': 20}),
            dcc.Input(id='carbon-intensity-input', type='number', value=400, style={'height': '30px', 'width': '60px', 'marginBottom': '20px'}),  # Add marginBottom here
            html.Br(),
            html.Label('Power Consumption of Old Hardware (W): ', style={'fontSize': 20, 'marginTop': '20px'}),
            dcc.Input(id='old-power-input', type='number', value=200, style={'height': '30px', 'width': '60px', 'marginBottom': '20px'}),
            html.Br(),
            html.Label('Power Consumption of New Hardware (W): ', style={'fontSize': 20, 'marginTop': '20px'}),
            dcc.Input(id='new-power-input', type='number', value=160, style={'height': '30px', 'width': '60px', 'marginBottom': '20px'}),
            html.Br(),
            html.Label('Embodied Carbon of New Hardware (gCO2): ', style={'fontSize': 20, 'marginTop': '20px'}),
            dcc.Input(id='embodied-carbon-input', type='number', value=24684, style={'height': '30px', 'width': '60px', 'marginBottom': '20px'}),
            html.Br(),
            html.Label('Daily Usage Ratio: ', style={'fontSize': 20, 'marginTop': '20px'}),
            dcc.Input(id='usage-input', type='number', value=0.4, style={'height': '30px', 'width': '60px', 'marginBottom': '20px'}),
            html.Br(),
            html.Button('Update', id='update-button', n_clicks=0, style={
                'backgroundColor': 'navy',
                'border': '2px solid black',
                'color': 'white',
                'padding': '32px 32px',
                'textAlign': 'center',
                'textDecoration': 'none',
                'display': 'inline-block',
                'fontSize': '22px',
                'margin': '60px 130px',
                'cursor': 'pointer',
                'borderRadius': '50%'
            })
        ], style={'marginLeft': '0px', 'marginTop': '100px'}),
    ], style={'display': 'flex'})
])

@app.callback(
    Output('graph', 'figure'),
    [Input('update-button', 'n_clicks')],
    [State('carbon-intensity-input', 'value'),
     State('old-power-input', 'value'),
     State('new-power-input', 'value'),
     State('embodied-carbon-input', 'value'),
     State('usage-input', 'value')]
)
def update_graph(n_clicks, carbon_intensity, old_power_Watt, new_power_Watt, embodied_carbon_new, daily_usage_ratio):
    operation_carbon_old_per_day = old_power_Watt * 24 / 1000 * daily_usage_ratio
    operation_carbon_new_per_day = new_power_Watt * 24 / 1000 * daily_usage_ratio
    per_day_carbon_save = [100*((operation_carbon_old_per_day*carbon_intensity*i)-(operation_carbon_new_per_day*carbon_intensity*i + embodied_carbon_new))/(operation_carbon_old_per_day*carbon_intensity*i)  for i in range(1,2000)]
    fig = go.Figure()
    for i in range(-150, 151):  # fill the background with light green above y=0 and light red below y=0
        if i < 0:
            fig.add_trace(go.Scatter(x=[-21, 2000], y=[i, i], fill='tonexty', fillcolor='rgba(255, 182, 193, 0.15)', line_width=0))  # light red
        else:
            fig.add_trace(go.Scatter(x=[-21, 2000], y=[i, i], fill='tonexty', fillcolor='rgba(144, 238, 144, 0.15)', line_width=0))  # light green
    fig.add_trace(go.Scatter(x=list(range(1,2000)), y=per_day_carbon_save, line=dict(color='#cc4778', width=4)))  # add the main line
    fig.update_layout(
        autosize=False,
        width=1200,
        height=800,
        title_text=f"Carbon Intensity: {carbon_intensity} gCO2/kWh",
        xaxis_title="Time of Operation (Years) After Upgrade",
        yaxis_title="Carbon Footprint Saving (%) with Upgrade",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        showlegend=False,
        xaxis = dict(
            tickmode = 'array',
            tickvals = [-10,365,365*2,365*3,365*4, 365*5],
            ticktext = ['0', '1', '2', '3', '4','5'],
            gridcolor='lightgray',
        ),
        yaxis=dict(gridcolor='lightgray')
    )
    fig.update_yaxes(range=[-60, 60])  # set the y-axis limits
    fig.update_xaxes(range=[-10, 365*5])
    fig.add_shape(type="line", line=dict(dash='dash'), x0=0, x1=2000, y0=0, y1=0)  # add a dashed line at y=0
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8080)

