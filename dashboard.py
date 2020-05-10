import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.graph_objs as go
import dash
import pandas as pd

tailnumber = 50

# Step 1 Launch app
app = dash.Dash('__name__')

# Step 2 Import data
df = pd.read_csv('/root/project/data/pi/httploadtime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
df['Time'] = pd.to_datetime(df.Time)
df.set_index('Time')

dnsdf = pd.read_csv('/root/project/data/pi/dnslookuptime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
dnsdf['Time'] = pd.to_datetime(dnsdf.Time)
dnsdf.set_index('Time')

# Step 3 create plotly figure
latestdf = df.tail(tailnumber)
trace_1 = go.Scatter(x=latestdf['Time'], y=latestdf['Resp'],
                     name='HTTP Response',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)')
                     )
layout = go.Layout(title='HTTP load times',
                   hovermode='closest')
fig = go.Figure(data=[trace_1], layout=layout)

latestdnsdf = dnsdf.tail(tailnumber)
trace_2 = go.Scatter(x=latestdnsdf['Time'], y=latestdnsdf['Resp'],
                     name='DNS Lookup Response',
                     line=dict(width=2,
                               color='rgb(229, 151, 50)')
                     )
layout2 = go.Layout(title='DNS Lookup times',
                    hovermode='closest')
dns_fig = go.Figure(data=[trace_2], layout=layout2)

# Step 4 Create dash layout
app.layout = html.Div([
    # adding a header and paragraph
    html.Div([
        html.H1('Dashboard'),
        html.P('Live Graphs')
    ],
        style={'padding': '50px',
               'backgroundColor': '3aaab2'}),

    dcc.Graph(id='plot', figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=1 * 5000,
        n_intervals=0
    ),
    dcc.Graph(id='dnsplot', figure=dns_fig),
    dcc.Interval(
        id='dns-interval-component',
        interval=1 * 5000,
        n_intervals=0)
])


# Step 5 Add callback functions
@app.callback(Output('plot', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df2 = pd.read_csv('/root/project/data/pi/httploadtime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
    latestdf2 = df2.tail(50)
    trace_2 = go.Scatter(x=latestdf2['Time'], y=latestdf2['Resp'],
                         name='HTTP Response',
                         line=dict(width=2,
                                   color='rgb(229, 151, 50)')
                         )
    layout2 = go.Layout(title='HTTP load times',
                        hovermode='closest')
    fig2 = go.Figure(data=[trace_2], layout=layout2)
    return fig2


@app.callback(Output('dnsplot', 'figure'),
              [Input('dns-interval-component', 'n_intervals')])
def update_dnsgraph(n):
    dnsdf2 = pd.read_csv('/root/project/data/pi/dnslookuptime.txt', header=None, usecols=[0, 1], names=['Time', 'Resp'])
    latestdnsdf2 = dnsdf2.tail(50)
    dnstrace_2 = go.Scatter(x=latestdnsdf2['Time'], y=latestdnsdf2['Resp'],
                            name='DNS Lookup Response',
                            line=dict(width=2,
                                      color='rgb(229, 151, 50)')
                            )
    dnslayout2 = go.Layout(title='DNS Lookup times',
                           hovermode='closest')
    fig3 = go.Figure(data=[dnstrace_2], layout=dnslayout2)
    return fig3


# Step 6 Add server
if __name__ == '__main__':
    app.run_server(debug=True)
