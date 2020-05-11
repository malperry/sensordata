import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.graph_objs as go
import dash
import pandas as pd

tailnumber = 50

tests = ['http', 'dns', 'ping', 'iperf']

# Step 1 Launch app
app = dash.Dash('__name__')

# Step 2 Import data from logs
# http page load logs
http_df = pd.read_csv('/root/project/data/pi/httploadtime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
http_df['Time'] = pd.to_datetime(http_df.Time)
http_df.set_index('Time')

# dns lookup time logs
dns_df = pd.read_csv('/root/project/data/pi/dnslookuptime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
dns_df['Time'] = pd.to_datetime(dns_df.Time)
dns_df.set_index('Time')

# wifi signal strength logs
wifisignal_df = pd.read_csv('/root/project/data/pi/wifidb.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
wifisignal_df['Time'] = pd.to_datetime(wifisignal_df.Time)
wifisignal_df.set_index('Time')

# Step 3 create plotly figure for HTTP load times
# make a new dataframe using the last 'tailnumber' of line from df
# http figure
tail_http_df = http_df.tail(tailnumber)
http_trace = go.Scatter(x=tail_http_df['Time'], y=tail_http_df['Resp'],
                        name='HTTP Response',
                        line=dict(width=2,
                                  color='rgb(229, 151, 50)')
                        )
http_layout = go.Layout(title='HTTP load times',
                        hovermode='closest')
http_fig = go.Figure(data=[http_trace], layout=http_layout)

# dns figure
tail_dns_df = dns_df.tail(tailnumber)
dns_trace = go.Scatter(x=tail_dns_df['Time'], y=tail_dns_df['Resp'],
                       name='DNS Lookup Response',
                       line=dict(width=2,
                                 color='rgb(229, 151, 50)')
                       )
dns_layout = go.Layout(title='DNS Lookup times',
                       hovermode='closest')
dns_fig = go.Figure(data=[dns_trace], layout=dns_layout)

# wifi signal figure
tail_wifisignal_df = wifisignal_df.tail(tailnumber)
wifisignal_trace = go.Scatter(x=tail_wifisignal_df['Time'], y=tail_wifisignal_df['Resp'],
                              name='Wi-Fi signal strength in dB',
                              line=dict(width=2,
                                        color='rgb(229, 151, 50)')
                              )
wifisignal_layout = go.Layout(title='Wi-Fi signal strength in dB',
                              hovermode='closest')
wifisignal_fig = go.Figure(data=[wifisignal_trace], layout=wifisignal_layout)

# Step 4 Create dash layout
app.layout = html.Div([
    # adding a header and paragraph
    html.Div([
        html.H1('Network Metric Dashboard'),
        html.P('Live Graphs showing the last ' + str(tailnumber) + ' minutes')
    ],
        style={'padding': '10px',
               'backgroundColor': '3aaab2'}),

    dcc.Graph(id='plot', figure=http_fig),
    dcc.Interval(
        id='interval-component',
        interval=1 * 5000,
        n_intervals=0
    ),
    dcc.Graph(id='dnsplot', figure=dns_fig),
    dcc.Interval(
        id='dns-interval-component',
        interval=1 * 5000,
        n_intervals=0),
    dcc.Graph(id='wifiplot', figure=wifisignal_fig),
    dcc.Interval(
        id='wifi-interval-component',
        interval=1 * 5000,
        n_intervals=0)
])


# Step 5 Add callback functions
@app.callback(Output('plot', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    refresh_http_df = pd.read_csv('/root/project/data/pi/httploadtime.txt', header=None, usecols=[0, 1],
                                  names=['Time', 'Resp'])
    tail_refreshed_http = refresh_http_df.tail(50)
    http_trace_2 = go.Scatter(x=tail_refreshed_http['Time'], y=tail_refreshed_http['Resp'],
                              name='HTTP Response',
                              line=dict(width=2,
                                        color='rgb(229, 151, 50)')
                              )
    http_layout2 = go.Layout(title='HTTP load times in ms',
                             hovermode='closest')
    http_fig2 = go.Figure(data=[http_trace_2], layout=http_layout2)
    return http_fig2


@app.callback(Output('dnsplot', 'figure'),
              [Input('dns-interval-component', 'n_intervals')])
def update_dnsgraph(graphs):
    refresh_dns_df = pd.read_csv('/root/project/data/pi/dnslookuptime.txt', header=None, usecols=[0, 1],
                                 names=['Time', 'Resp'])
    tail_refreshed_dns = refresh_dns_df.tail(50)
    dns_trace_2 = go.Scatter(x=tail_refreshed_dns['Time'], y=tail_refreshed_dns['Resp'],
                             name='DNS Lookup Response',
                             line=dict(width=2,
                                       color='rgb(229, 151, 50)')
                             )
    dns_layout2 = go.Layout(title='DNS Lookup times in ms',
                            hovermode='closest')
    dns_fig2 = go.Figure(data=[dns_trace_2], layout=dns_layout2)
    return dns_fig2


@app.callback(Output('wifiplot', 'figure'),
              [Input('wifi-interval-component', 'n_intervals')])
def update_wifigraph(graphs):
    refresh_wifi_df = pd.read_csv('/root/project/data/pi/wifidb.txt', header=None, usecols=[0, 1],
                                  names=['Time', 'Resp'])
    tail_refreshed_wifi = refresh_wifi_df.tail(50)
    wifi_trace_2 = go.Scatter(x=tail_refreshed_wifi['Time'], y=tail_refreshed_wifi['Resp'],
                              name='wifi signal strength',
                              line=dict(width=2,
                                        color='rgb(229, 151, 50)')
                              )
    wifi_layout2 = go.Layout(title='WiFi signal strength in dB',
                             hovermode='closest')
    wifi_fig2 = go.Figure(data=[wifi_trace_2], layout=wifi_layout2)
    return wifi_fig2


# Step 6 Add server
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
