"""
kwargs texttemplate and hovertemplate's %{var} syntax, in a go.plot()
Usually, for "var" to guarantee to work in %{var}, "var" better be an array the same size of x and y

[Summary]
"meta" is the most reliable, can be single value, can be array,
you can even use a single-ish array, and access throu "%{meta[0]}". or use a sinlge-ish dict and access
thru "%{meta.key}"

hovermode is very finiky, requires mostly array "var"s

"customdata" has to be an array, most notable use is customdata=df[othercols].to_dict("records")

"text" can be single str for texttemplate, but fails for hovermode

all other properties or kwargs like "name", "color", etc are not reliablely accessed by %{var}
"""

go.Figure(go.Bar(
    x= df.index
    y= df['col'],
    customdata= df[["col0", "col1"]].to_dict("records"), # per x,y pair
    meta = dict(key0='val0', key1='val1'), # per trace

    hovertemplate="%{customdata.col0}",
    texttemplate="%{meta.key0}",
    textposition="auto"
))
