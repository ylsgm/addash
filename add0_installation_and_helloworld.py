"""
INSTALLATIONS

in cmd:
$ conda install dash 
    # all packages will be installed by this simple command.
    # dash packages, flask, plotly, retry, all will be installed
$ conda install -c conda-forge jupyterlab-plotly-extension 
    # for jupyter plugin

$ jupyter lab build
    # enable the plug in.


# to veryfy:
import dash_core_components
print(dash_core_components.__version__) # >> 1.13.3
"""
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# pd stuff
import pandas as pd
import numpy as np
df = pd.DataFrame({"col0": [1, 2, 3], "SF": [4, 1, 2], "Montreal": [2, 4, 5]})
df.index.name = "index.name"
dt = pd.DataFrame(data=np.random.randint(5, size=(20, 6)), columns=list('asdfkj'))


## TABLE HANDLING ##
# impression is that, the thing is very hard coded, having difficulty to list index as a a column
# have to use df = df.reset_index() can turn index into a column instead.
def generate_table(dataframe, max_rows=100):
    """reusable table generator"""
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_dash_table(dfin):
    dfin = dfin.reset_index()
    import dash_table
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfin.columns],
        data=dfin.to_dict(orient='records'),
        # to_dict(): pd built in method, to turn df into a giant dictionary.
        )


#    The fonts in your application will look a little bit different than what is displayed here.
#    This application is using a custom CSS stylesheet to modify the default styles of the elements.
#    You can learn more in the css tutorial, but for now you can initialize your app with
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# [+] declare APP, [?] not sure what example app is, app itself can be ran as "server"?
#   maybe app is "flask".
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # later on, app.layout = an html

# [+] FIG is the plot, the key
# IMPRESSION IS THAT, DASH.EXPRESS IS PROBABLY NOT WHAT WE NEED. 
# NEED THE LOWER LAYER WAYS OF DOING PLOT, ONE COLUMN ADDED AT A TIME, SUBPLOT AS WELL.
# THE PIVOT TABLE BAR PLOT MAY USE THIS?
fig = px.bar(df, x=df.index, y=["col0", "SF", "Montreal"], barmode="group")
fig.update_layout(
        plot_bgcolor='#EEEEEE',
        paper_bgcolor='#CCCCCC',
        font_color='#111111',
        )

# import plotly.graph_obj as go
fig0 = px.line(
        dt,
        # x=dt.index, y='a', # this is to plot only one thing
        # hover_name='a',
        hover_name = 'value',
        )
    # if x and y kwargs not provided, all columns are plot, if x, y, provided one column ploted.
    # [!] 'value' and 'index' are built-in recognized, when you give 'value', dash knows it refers
    # to value of the df cell. Usually you pass a 'colname' to hover_name

# [+] LAYOUT, The layout is composed of a tree of "components" like html.Div and dcc.Graph.
#     HTML.DIV()
app.layout = html.Div(

#    The children property is special. By convention, it's always the first attribute which means
#    that you can omit it: html.H1(children='Hello Dash') is the same as html.H1('Hello Dash').
#    Also, it can contain a string, a number, a single component, or a list of components.
        children=[

#    The dash_html_components library has a component for every HTML tag. The
#    html.H1(children='Hello Dash') component generates a <h1>Hello Dash</h1> HTML element in your
#    application.
            html.H1(
                children='title name',
                style={
                    'textAlign': 'center',
                        # The keys in the style dictionary are camelCased, from HTML file 
                        # So, instead of text-align, it's textAlign
                        # So, instead of font-family, it's font-family
                    'color': '#002244',
                    'fontFamily':'Monospace',
                    'fontSize': '122px',
                },
            ),
            # "<h1>hello</h1>" <== this won't work
            # my impression is that, according to a 2017 post, Dash will not render raw HTML code

            # You can use the stackexchange mark down !!
            dcc.Markdown("""

            ## Dash supports [**stackexchange Markdown syntax**](http://commonmark.org/help).

            Markdown is a simple way to write and format text.
            It includes a syntax for things like:

            <double space>  for a new line  
            <2x "enter" key> for a new paragraph.

            \*\*bold text\*\* == **bold text**  
            \*italics\* == *italics*  

            [links](http://commonmark.org/help),

            \> for block quotes:

            > quote line 0  
            > quote line 1  

            inline `this is an inline code` inline snippets, lists, quotes, and more.

            ```
            this is a block
            of code
            NOTICE, it is not tripple quote, it is a 3x "~" key
            ```

            """),

#    Not all components are pure HTML. The dash_core_components describe higher-level components
#    that are interactive and are generated with JavaScript, HTML, and CSS through the React.js
#    library.
            dcc.Graph(
                id='express bar graph',
                figure=fig
            ),
            dcc.Graph(
                id='express scatter graph',
                figure=fig0
            ),

            html.Div(children='''
                another html.Div() ============
            '''),

            generate_table(dt),
            generate_dash_table(dt),

    ] # eof "children" list
) # eof root html.Div()

if __name__ == '__main__':
    app.run_server(debug=0)
    # exactly how server, threads, multiple pages is done?


