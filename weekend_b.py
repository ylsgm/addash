[ ] to be merged into chsh

# [ ]to io excel:
########################################
df_rename = pd.read_excel(pwd / '__colrename.xlsx', sheet_name='AllJobData', index_col=None, na_values="NULL")

# must use float number, or 
kdf.sht.api.Columns('H:K').ColumnWidth = 55.0
kdf.sht.api.Columns(1).RowHeight = 55.0 # [!!!] MUST BE A FLOAT NUMBER
kdf.sht.api.Columns('A:N').WrapText = True
kdf.sht.api.Columns('A:N').VerticalAlignment = -4160 # VeralineTOp


#to apply, agg
########################################
# [!] careful where foo is declared and used. multiple agg() or apply() with different foo()s may
# cause applying the wrong foo()

# groupby multiple columns; rename;
gp = df.groupby('JobTrac ID', 'Team Member Name')
sr = gp.agg(
        mhrs = pd.NamedAgg('memberhours', pd.unique)
        )
sr0.index.names = ['id', 'who']
df = sr.to_frame().reset_index().rename(columns={'mhrs': 'hours'})
    # both multi indexes will be set to columns by sr.to_frame()

# to be sorted
########################################
# normal import when testing lib files inside the lib dir
# vs.
# relative import when lib is used from outside
if __package__ is None or __package__ == '':
    from fileInSameFolderAsThisFile import myfoo
else:
    from .fileInSameFolderAsThisFile import myfoo

nan is not None
if pd.notnull(row['valid']): #[!] nan is NOT NONE, if nan returns true
    also, expand on df.empty; if df usage and all

##################################

########################################################################################
# plotly stuff
########################################################################################


l_xvals = df.index.to_timestamp()
    #[!] df.index at the moment is time period, which doens't work well with plotly 
   #  "Object of type Period is not JSON serializable"

df_meta = pd.merge(left=preplot, right=ref, how='left', on='id')
df_meta['start'], df_meta['end'] = df_meta['start'].dt.strftime('%Y-%b'), df_meta['end'].dt.strftime('%Y-%b')


fig= go.Figure()

for coln in df.columns:

    meta = df_meta.loc[df_meta['id']==coln, :].to_dict('records')[0]
    fillcolor, linecolor, linewidth = 0,0,1

    if len(meta['problem']) > 0:
        fillcolor = 'rgba(0, 0, 0, 0)'
        linecolor = '#cc11cc'
        linewidth = 0.1
    elif not "In-Progress" in meta['status']:
        fillcolor = 'rgba(99, 99, 99, .1)'
        linecolor = '#666'
        linewidth = 0.5  
    else:
        fillcolor = getcolor(meta['priority'])
        linecolor = None
        linewidth = 1   
        
    fig = fig.add_trace(go.Bar(
        name=coln, x=l_xvals, y=df[coln],  
        
        customdata = [meta]*len(df.index),
        
        hovertemplate =
        '<b>[%{customdata.id}]  %{customdata.problem}</b>   <i>%{customdata.status}</i>' + '<br>'
        '<b>%{customdata.title}</b>' +'<br>'
        '<i>PRIORITY</i>: %{customdata.priority} | ' + '<i>monthlyHrs</i>: %{y} | '
        '%{customdata.percent}% of %{customdata.hours} <i>hrs total</i> <br>'
        '%{customdata.start} ~ %{customdata.end} <br>'
        '? %{customdata.sact}' +'<br>'
        '? %{customdata.scmt0}' +'<br>'
        '%{customdata.scmt1}' +'<br>'           
        '<extra></extra>',

        texttemplate = '%{customdata.id}',            
        textposition="auto",
        
        textfont=dict(
            color=linecolor,
        ),
        
        marker=dict(
            color = fillcolor,
            line=dict(
                color=linecolor,
                width=linewidth,
            ),
        ),
        
    ))

fig = fig.add_shape(type="line",
    x0=l_xvals[0], y0=125, x1=l_xvals[-1], y1=125,
    line=dict(
        color="rgba(255, 22, 99, 0.4)",
        width=3,
        dash="dot",
    )
)
fig = fig.update_layout(barmode='stack')
fig = fig.update_layout(
    title= meta['who'],
    
    hoverlabel=dict(
        font_size=16,
        font_family="monospace"
    ),
    xaxis=dict( #[!!!!!!]
        title="time",
        
        tickformat="%Y-%b",
#         nticks=12,
        tick0 = l_xvals[0],

        dtick = "M1",
        
        type="date",
        # type="category",
        range=[l_xvals[0] , l_xvals[13] if len(l_xvals)>13 else l_xvals[-1]
              ],
#         rangeslider=dict( # terrible performance
#             autorange=False,
#             visible=True,
#         ),
    ),    
)
pio.show(fig)


