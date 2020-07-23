import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import numpy as np
np.random.seed(0)

## setting up the dfs
num_of_rows=10
df0 = pd.DataFrame(
        data=np.random.randint(-2, 5, (num_of_rows, 2)),
        columns=list('ab'),
        index=pd.date_range('2020-01-01', periods=num_of_rows, freq='1h')
        )
df0['a'] = df0['a'] * 123.4
print(df0)


num_of_rows=15
df1 = pd.DataFrame(
        data=np.random.randint(3, 5, (num_of_rows, 1)),
        columns=['c'],
        index=pd.date_range('2020-01-01 06:10:00', periods=num_of_rows,  freq='5min'),
        )
df1.iloc[[1, 3, 5], :] = np.nan
print(df1)

df2 = pd.DataFrame(
        data=['foo happens', 'bar happens', 'baz happens'],
        columns=['events'],
        index=pd.date_range('2020-01-01 03:00:00', periods=3, freq = '111min'),
        )
print(df2)

## setting up dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    children=[
        dcc.Graph(
            id='number + text time series plot',
            figure=fig
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=0)




