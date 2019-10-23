import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from smart_open import open
import csv

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

with open ('s3://nyctaxi-trip-data/output_result.csv') as result_data:
        read_result=csv.reader(result_data,delimiter=',')
with open ('s3://nyctaxi-trip-data/fatigue_result.csv') as fatigue_data:
        read_fatigue=csv.reader(fatigue_data,delimiter=',')

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
    data['driver_id']=['bbf91e6720', 'a7108907c0', 'e6f3cad6dc','7b30c143d8',
                    'd4ec191400','7075c4988c','38e76b9881','e5d37daef0','94085c487e',
                    'dcf0b59678','eb49db316d','b2e669d72f','009f69f395',
                    'a7f1cf97e1','ad9467688a','18885c319d','c9d92d1d2a','8fc7b9d9af',
                    'edcced0626','8678f1d459']
    
    data['driving_time']=next(read_result)
    
    if data['driving_time'] == ['0','3060','480','540','1560','420','240','420','4020','2460','1740',
            '1800','1560','1680','180','4380','2160','240','960','1680']:
        result_data.seek(0)
        
   # fatigue drivers
    data['driver_id_fatigue']=next(read_fatigue)
   # print (data['driver_id_fatigue'])
    data['driving_time_fatigue']=next(read_fatigue)
   # print (data['driving_time_fatigue'])

    if data['driver_id_fatigue'] == ['be2af1b95b', '8a124d2c97', '6768c7ebfd', '6d483b193a', 'c201a15920', 
            'b9b265c465', '44e35d9801', '00c152d495', 'ac39a2b21a', '028625a515', 'aa2d1be97b', 
            '7c59589709', 'bfec2c659f', '5f688171bb', '93c7ea88e8', 'bd311c6da5', '688e888ea8', 'a3efed94df', 
            '1d9f1ab92f', '070518ef3f']:
        fatigue_data.seek(0)
        
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
        'type': 'bar'
    }, 1, 1)
    fig.append_trace({
        'x': data['driver_id'],
        'y': data['driving_time'],
        'name': 'driving time vs driver id',
        'type': 'bar',
        'marker_color':'rgb(102,255,178)',
        'width':0.4
    }, 2, 1)
    fig.append_trace({
        'x': data['driver_id_fatigue'],
        'y': data['driving_time_fatigue'],
        'name': 'fatigue drivers',
        'type': 'bar',
        'marker_color':'rgb(255,102,102)',
        'width':0.4,
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
