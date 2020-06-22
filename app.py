# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import model


# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.now())

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        dist = int(request.form['dist'])
        workout = model.create_workout(dist)
        total_dist = 0
        for eachset in workout:
            total_dist += eachset.set_dist
        return render_template('results.html', workout=workout, total_dist=total_dist, time=datetime.now())