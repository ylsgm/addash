####################################################################################################################
# [+] how to insepct a fig object for debugging purpose
####################################################################################################################
fig.data==
(Bar({
     'alignmentgroup': 'True',
     'hovertemplate': 'x=%{x}<br>y=%{y}<extra></extra>',
     'legendgroup': '',
     'marker': {'color': '#636efa'},
     'name': '',
     'offsetgroup': '',
     'orientation': 'v',
     'showlegend': False,
     'textposition': 'auto',
     'x': array(['#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A',
                 '#B68100', '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1',
                 '#FC0080', '#B2828D', '#6C7C32', '#778AAE', '#862A16', '#A777F1',
                 '#620042', '#1616A7', '#DA60CA', '#6C4516', '#0D2A63', '#AF0038'],
                dtype=object),
     'xaxis': 'x',
     'y': array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
                 18, 19, 20, 21, 22, 23], dtype=int64),
     'yaxis': 'y'
 }),)

# to access the first Bar chart:
fig.data[0]
type(fig.data[0]) == plotly.graph_objs._bar.Bar

fig.data[0].name = 'a'

####################################################################################################################
# [+] when to use px
####################################################################################################################
import pandas as pd
import numpy as np
df = pd.DataFrame(columns=list('abcd'), data=np.random.randn(20, 4),
                  index=pd.date_range("2020-10-10", periods=20, freq="1min"))


# for something quick and dirty, px is great. 
# [1] It can interpret kwarg "y" very flexibly, gave it colname, or actual col, all good. 
# [2] px will also automatically assign coln to trace name, makes it easy to "selector" when fig.update_traces()
import plotly.express as px
fig = px.scatter(df, x=df.index, y=df.columns)
fig = px.scatter(df, x=df.index, y=['c', df['b']])

# with some fig.update_traces() that is common to 
fig = fig.update_traces(
    selector=dict(name="c"),
    marker=dict(color="rgba(0, 0, 0, .3)", size=22, symbol="201"),
    mode="lines+markers",
)


# [THE DRAWBACKs]
# [1] can NOT support multiaxis, can't specify during ploting, 
# [2] surprisingly px doesn't auto assign name, if there is only one trace [!!!]
fig = fig.add_trace(go.Scatter(
    x=df.index, y=df['a'], yaxis='y2'
))
fig = fig.update_layout(
    xaxis=dict(
        type="date",
        domain=[0, 1], # display    
        rangeslider=dict(
            autorange=True,
            visible=True,
        ),
    ),
    yaxis1=dict(
        anchor='free',
        #rangemode='tozero',
        linecolor='green', linewidth=2,
        showgrid=False, zeroline=False,
    ),
    yaxis2=dict(
        anchor="free",
        
        overlaying="y", 
            # [!] crucially important, otherwise stuff on y axis can not hover mode
        
        side="left",
        position=0.95,
        linecolor='red', linewidth=2,
        showgrid=False, zeroline=False,
    )
)
fig.show()

