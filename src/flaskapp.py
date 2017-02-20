#!/usr/bin/env python3
'''
    RedirectLogQ: A simple URL redirection backend that logs the time of each redirection.
    Copyright (C) 2017  Aaron Thomas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from datetime import datetime, timezone
import flask
from flask import Flask, make_response, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()  # Connect to mongodb
db = client.RedirectLogQ_db  # Establish a database
hit_coll = db.hit_coll  # Establish a collection for hits
redirect_coll = db.redirect_coll  # Establish a collection for redirects 
locations_coll = db.locations_coll # Establish a collection for physical locations

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/redirect', methods=['GET'])  # I could have chosen any name as long as it contained <token>
def redirect():
    '''
    Redirects the user
    @todo(aaron):
        1) learn how to have a database
        2) learn how to generate lots of different URLs
        3) make sure the database is setup right
        4) write code so that the databse has logs of all the stuff
        5) you win!
    '''
    locationID = request.args.get('locationID')
    token = request.args.get('token')
    now = str(datetime.now(timezone.utc))

    # redirect_url = db.locations_coll.find({"token":token})  # Find the token from mongo
    redirect_url = 'http://www.google.com'  # Just kidding; nothing's in mongo yet
    redirect_obj = flask.redirect(redirect_url, code=303)
    response = make_response(redirect_obj)
    response.set_cookie('cookie_name', value='values')
    hit = {
        "time": now,
        "token": token,
        "cookie": "the cookie that we found/added"
    }
    result = db.hit_coll.insert_one(hit)
    print(locationID, token)
    return response

    # return render_template('redirect.html',url=token)


@app.route('/generate_url_token')
def generate_url_token():
    return 'Hello World'

app.run()