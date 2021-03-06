from flask import Flask, render_template, request, redirect
import requests
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from jinja2 import Template
import pandas as pd
import numpy as np

# create some data
x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]


# select the tools we want
TOOLS="pan,wheel_zoom,box_zoom,reset,save"

# the red and blue graphs will share this data range
#xr1 = Range1d(start=0, end=30)
#yr1 = Range1d(start=0, end=30)







app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
         return render_template('index.html')
    else:
         app_lulu.vars['name'] = request.form['name_lulu']
         #app_lulu.vars['choose'] = request.form.getlist['features']
         return render_template('index.html')

@app.route('/next_lulu',methods=['GET','POST'])
def next_lulu():
    payload = { 'order':'asc','start_date':'2010-05-01'}
    wiki_name = 'https://www.quandl.com/api/v3/datasets/WIKI/'+request.form['name_lulu']+'.json'
    r = requests.get(wiki_name, params=payload)
    

    ddate = r.json()
    if ddate.has_key('quandl_error'):
	return render_template('end_lulu.html')
    
    s = pd.DataFrame(ddate['dataset']['data'])
    s[0] = pd.to_datetime(s[0])

    # build our figures
    p1 = figure(tools=TOOLS,x_axis_type = "datetime",title = "Data from Quandle WIKI set")
    p1.xaxis.axis_label = 'Date'
    

    


    if request.form.get('features1'):
	p1.line(s[0], s[4], color="red", legend="Closing price")
    
    if request.form.get('features2'):
        p1.line(s[0], s[11] , color="blue",legend="Adjusted closing price")
    
    if request.form.get('features3'):
        p1.line(s[0], s[5] , color="yellow",legend="Volume")
    

    



    # plots can be a single PlotObject, a list/tuple, or even a dictionary
    plots = {'Red': p1}

    script, div = components(plots)
    print div

    template = Template('''<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Bokeh Scatter Plots</title>
        <style> div{float: left;} </style>
        <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.css" type="text/css" />
        <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.js"></script>
        {{ script }}
    </head>
    <body>
                        <h1>Generated graph for  {{ name }}</h1>
                        <h4>
                        <form id='return' method='GET' action='index' > 
                          <p>
                            <input type='submit' value='BACK' /> 
                          </p>
                        </form>
                        </h4>
    {% for key in div.keys() %}
        {{ div[key] }}
    {% endfor %}
    </body>
    </html>
    ''')

    return encode_utf8(template.render(name=request.form['name_lulu'], script=script, div=div))


if __name__ == '__main__':
  app.run(port=33507)
