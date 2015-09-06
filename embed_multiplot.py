from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components
from jinja2 import Template
import webbrowser
import os
import six

# create some data
x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]


# select the tools we want
TOOLS="pan,wheel_zoom,box_zoom,reset,save"

# the red and blue graphs will share this data range
xr1 = Range1d(start=0, end=30)
yr1 = Range1d(start=0, end=30)



# build our figures
p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
p1.scatter(x1, y1, size=12, color="red", alpha=0.5)



# plots can be a single PlotObject, a list/tuple, or even a dictionary
plots = {'Red': p1}

script, div = components(plots)

template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Bokeh Scatter Plots</title>
        <style> div{float: left;} </style>
        <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css" type="text/css" />
        <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js"></script>
        {{ script }}
    </head>
    <body>
    {% for key in div.keys() %}
        {{ div[key] }}
    {% endfor %}
    </body>
</html>
''')

html_file = 'embed_multiple.html'
with open(html_file, 'w') as textfile:
    textfile.write(template.render(script=script, div=div))
url = 'file:{}'.format(six.moves.urllib.request.pathname2url(os.path.abspath(html_file)))
webbrowser.open(url)
