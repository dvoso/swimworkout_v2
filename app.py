# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from datetime import datetime
import model
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import bcrypt


# -- Initialization section --
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# load environment variables 
load_dotenv()
USER = os.getenv("MONGO_USERNAME")
PASS = os.getenv("MONGO_PASSWORD")

# name of database
app.config['MONGO_DBNAME'] = 'swimming'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@cluster0-7bt79.mongodb.net/swimming?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.now())

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        dist = int(request.form['dist'])
        practice = model.create_workout(dist)
        print(practice)
        if 'username' in session:
            practice['user'] = session['username']
            # connect to the database
            collection = mongo.db.practices
            # insert new data
            collection.insert(practice)

        return render_template('results.html', practice = practice, time = datetime.now())



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password': str(hashpass, 'utf-8')})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
            # return "success"
        else:
            message = "That username is already taken. Please try again"
            return render_template('signup.html', message=message)

    return render_template('signup.html', time=datetime.now())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
                # return "success"
        
        # if no successful match, display an error 
        message = "Unsuccessful username/password log in attempt"
        return render_template('login.html', message = message, time=datetime.now())
    else:
        return render_template('login.html', time=datetime.now())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/practices/<practiceId>', methods = ['GET', 'POST'])
def practice(practiceId):
    # connect to mongo
    collection = mongo.db.practices

    # if came via a post (updating the name or deleting), then rename or delete 
    if request.method == 'POST':
        if 'delete' in request.form:
            collection.remove({"_id": ObjectId(practiceId)})
            return redirect('/practices/mypractices')
        else:
            collection.update_one({"_id": ObjectId(practiceId)}, {"$set": {  "name" : request.form['name'] }})
    
    # find the desired practice
    practice = collection.find_one({"_id": ObjectId(practiceId)})
    
    return render_template('practice.html', practice = practice, time=datetime.now())


@app.route('/practices/mypractices')
def mypractices():
    collection = mongo.db.practices
    username = session['username']
    practices = collection.find({'user' : username})

    return render_template('mypractices.html', practices = practices, time=datetime.now())


# @app.route('/createpractice')
# def create_practice():
#     collection = mongo.db.practices
#     username = session['username']