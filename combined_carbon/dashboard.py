import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import random
import threading
import zmq
import numpy as np
import argparse
import plotly.express as px
import json
import plotly.graph_objects as go

app = dash.Dash(__name__)

##data loading
data = json.load(open('./operation_carbon_kWh_per_day.json'))
operational_p100_v100_candle_p100=data["('p100', 'v100')"]["candle"]["p100"]
operational_p100_v100_candle_v100=data["('p100', 'v100')"]["candle"]["v100"]
operational_p100_v100_cv_p100=data["('p100', 'v100')"]["cv"]["p100"]
operational_p100_v100_cv_v100=data["('p100', 'v100')"]["cv"]["v100"]
operational_p100_v100_nlp_p100=data["('p100', 'v100')"]["nlp"]["p100"]
operational_p100_v100_nlp_v100=data["('p100', 'v100')"]["nlp"]["v100"]
operational_p100_a100_candle_p100=data["('p100', 'a100')"]["candle"]["p100"]
operational_p100_a100_candle_a100=data["('p100', 'a100')"]["candle"]["a100"]
operational_p100_a100_cv_p100=data["('p100', 'a100')"]["cv"]["p100"]
operational_p100_a100_cv_a100=data["('p100', 'a100')"]["cv"]["a100"]
operational_p100_a100_nlp_p100=data["('p100', 'a100')"]["nlp"]["p100"]
operational_p100_a100_nlp_a100=data["('p100', 'a100')"]["nlp"]["a100"]
operational_v100_a100_candle_v100=data["('v100', 'a100')"]["candle"]["v100"]
operational_v100_a100_candle_a100=data["('v100', 'a100')"]["candle"]["a100"]
operational_v100_a100_cv_v100=data["('v100', 'a100')"]["cv"]["v100"]
operational_v100_a100_cv_a100=data["('v100', 'a100')"]["cv"]["a100"]
operational_v100_a100_nlp_v100=data["('v100', 'a100')"]["nlp"]["v100"]
operational_v100_a100_nlp_a100=data["('v100', 'a100')"]["nlp"]["a100"]
data = json.load(open('./embodied_carbon_gCO2.json'))
embodied_p100=data["p100"]
embodied_v100=data["v100"]
embodied_a100=data["a100"]
data = json.load(open('./perf_gain.json'))
perf_p100_v100_candle=data["('p100', 'v100')"]["candle"]
perf_p100_v100_cv=data["('p100', 'v100')"]["cv"]
perf_p100_v100_nlp=data["('p100', 'v100')"]["nlp"]
perf_p100_a100_candle=data["('p100', 'a100')"]["candle"]
perf_p100_a100_cv=data["('p100', 'a100')"]["cv"]
perf_p100_a100_nlp=data["('p100', 'a100')"]["nlp"]
perf_v100_a100_candle=data["('v100', 'a100')"]["candle"]
perf_v100_a100_cv=data["('v100', 'a100')"]["cv"]
perf_v100_a100_nlp=data["('v100', 'a100')"]["nlp"]

carbon_intensity = 400
per_day_candle=[100*((operational_p100_v100_candle_p100*carbon_intensity*i)-(operational_p100_v100_candle_v100*carbon_intensity*i + embodied_v100))/(operational_p100_v100_candle_p100*carbon_intensity*i)  for i in range(1,2000)]

# fig = go.Figure()

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

@app.callback(Output('graph', 'figure'),
                [Input('interval-component', 'n_intervals')])
def update_graph(n):
    per_day_candle=[100*((operational_p100_v100_candle_p100*400*i)-(operational_p100_v100_candle_v100*400*i + embodied_v100))/(operational_p100_v100_candle_p100*400*i)  for i in range(1,2000)]
    fig = go.Figure()
    for i in range(-60, 41):  # fill the background with light green above y=0 and light red below y=0
        if i < 0:
            fig.add_trace(go.Scatter(x=[0, 2000], y=[i, i], fill='tonexty', fillcolor='rgba(255, 182, 193, 0.15)', line_width=0))  # light red
        else:
            fig.add_trace(go.Scatter(x=[0, 2000], y=[i, i], fill='tonexty', fillcolor='rgba(144, 238, 144, 0.15)', line_width=0))  # light green
    fig.add_trace(go.Scatter(x=list(range(1,2000)), y=per_day_candle, line=dict(color='#cc4778', width=4)))  # add the main line
    fig.update_layout(
        title_text="Carbon Intensity",
        xaxis_title="Days",
        yaxis_title="Carbon Emissions Reduction (%)",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        showlegend=False
    )
    fig.update_yaxes(range=[-60, 40])  # set the y-axis limits
    fig.update_xaxes(range=[30, 365*5])
    fig.add_shape(type="line", line=dict(dash='dash'), x0=0, x1=2000, y0=0, y1=0)  # add a dashed line at y=0
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

