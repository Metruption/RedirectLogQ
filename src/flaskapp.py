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
import uuid

from flask import Flask, make_response, render_template, request
from pymongo import MongoClient

import token_handler


app = Flask(__name__)

client = MongoClient()  # Connect to mongodb
db = client.RedirectLogQ_db  # Establish a database
hit_coll = db.hit_coll  # Establish a collection for hits
flier_coll = db.flier_coll  # Establish a collection for fliers 


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/form')
def display_empty_form():
    '''
    @todo(aaron): decide if it's worth your time making a comment for this
    '''
    return render_template('form.html', result="") #@todo(aaron): make the form, also dont push until this is documented


@app.route('/handle_tokens')
def handle_tokens(url, location_description):
    '''
    @todo(aaron): document this
    '''
    url = request.args.post('url')
    location_description = request.args.post('location_description')

    token = token_handler.generate_token(url)

    flier = {
        "real_url": url,
        "token": token,
        "location_description": location_description
    }

    if token == None:
        print("An error has occured. The url {} is not valid.".format(url))
        return "Failure"
    else:
        try:
            db.flier_coll.insert_one(flier)
            return "Success"
        except Exception as e:
            print(e)
            return "Failure"


@app.route('/redirect', methods=['GET'])  # I could have chosen any name as long as it contained <token>
def redirect_():
    '''
    Redirects the user
    '''
    redirect_url = tokenmanager.resolve_token(token)
    if redirect_url == None:
        pass #@todo(someone) make it do an error, return 500

    
    token = request.args.get('token')
    now = str(datetime.now(timezone.utc))

    redirect_obj = flask.redirect(redirect_url, code=303)
    response = make_response(redirect_obj)

    if 'RedirectLogQ_cookie' in request.cookies:
        cookie_value = uuid.uuid4().hex
        response.set_cookie('RedirectLogQ_cookie', value=cookie_value)
    else:
        cookie_value = request.cookies['RedirectLogQ_cookie']
    hit = {
        "time": now,
        "token": token,
        "cookie": cookie_value
    }
    result = db.hit_coll.insert_one(hit)
    return response

app.run()