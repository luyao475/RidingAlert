import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'TABLE_AGGRE_SUM',
     bootstrap_servers=['x.x.x.x:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=False,
      )
      
table_sum={}
fatigue_drivers={}

driver_id=['bbf91e6720', 'a7108907c0', 'e6f3cad6dc','7b30c143d8',
                    'd4ec191400','7075c4988c','38e76b9881','e5d37daef0','94085c487e',
                    'dcf0b59678','eb49db316d','199fa05b63','dec2aa8551',
                    'eeace255eb','5e00738ed9','3446442418','a8aee50b5b','b44b941840',
                    '72920f6ebc','8678f1d459']

driving_time=[0]*20
for message in consumer:
    message = message.value
    key = message.split(',')[0]
    value = int(message.split(',')[1])
    table_sum[key]=value
    for i in range (20):
        if key == driver_id[i]:
            driving_time[i]=value
    if value > 6300:
        fatigue_drivers[key]=value
    driver_id_fatigue = fatigue_drivers.keys()[:20]
    driving_time_fatigue = fatigue_drivers.values()[:20]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Taxi Driver Fatigue Detector'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    data = {
        'time': [],
        'driving_time': [],
        'driver_id': [],
        'tracker': [],
        'driving_time_fatigue': [],
        'driver_id_fatigue': []
    }

    # Setting time
    for i in range(8):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i)
        trk = 1
        data['tracker'].append(trk)
        data['time'].append(time)

    # driving time vs driver id
    data['driver_id']=driver_id
    data['driving_time']=driving_time
    
   # fatigue drivers
    data['driver_id_fatigue']= driver_id_fatigue
    data['driving_time_fatigue']= driving_time_fatigue

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=3, cols=1, vertical_spacing=0.2,  row_width=[0.5, 0.5, 0.1])
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['tracker'],
        'name': 'tracker',
       # 'mode': 'lines+markers',
        'type': 'bar'
    }, 1, 1)
    fig.append_trace({
        'x': data['driver_id'],
        'y': data['driving_time'],
        'name': 'driving time vs driver id',
        'type': 'bar',
        'marker_color':'rgb(102,255,178)',
        'width':0.4
       # 'color':'green'
    }, 2, 1)
    fig.append_trace({
        'x': data['driver_id_fatigue'],
        'y': data['driving_time_fatigue'],
        'name': 'fatigue drivers',
        'type': 'bar',
        'marker_color':'rgb(255,102,102)',
        'width':0.4,
       # 'bargap':0.5
    }, 3, 1)

# Update yaxis properties
    fig.update_yaxes(title_text=" ",range=[0, 6300], showgrid=False,showticklabels=False, row=1, col=1)
    fig.update_yaxes(title_text="driving time in seconds", range=[0, 6300], row=2, col=1)
    fig.update_yaxes(title_text="driving time in seconds", range=[0, 6300], row=3, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="time ",row=1, col=1)
    fig.update_xaxes(title_text="driver ID", row=2, col=1)
    fig.update_xaxes(title_text="fatigue drivers", row=3, col=1)

# Update title and height
    fig.update_layout(title_text=" ", height=700)

    return fig

if __name__ == '__main__':
 #   app.run_server(debug=True)
    app.run_server(debug=True, port=8080, host='0.0.0.0')
