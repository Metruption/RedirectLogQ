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
redirect_coll = db.redirect_coll  # Establish a collection for redirects 
locations_coll = db.locations_coll # Establish a collection for physical locations

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/form')
def display_form():
    '''
    @todo(aaron): decide if it's worth your time making a comment for this
    '''
    return render_template('form.html') #@todo(aaron): make the form, also dont push until this is documented

@app.route('/form/url="<url>"+location_description="<location_description>"')
def display_completed_form(url, location_description):
    '''
    @todo(aaron): document this
    '''
    token = token_handler.generate_token(url)
    if token == None:
        message = "An error has occured. The url {} is not valid.".format(url)

    else:
        try:
            #@todo(sean): make a db entry
            message = "Successfully created a redirect to {} with the location description {}. Your token is {}".format(url, location_description, token)
        except:
            message = "An error has occured. It will probably occur again if you try doing that again, so please do not."
        finally:
            pass #@todo(someone): decide if we need any code here and if to keep it if there is no code

    return render_template('form.html', result=message)


@app.route('/redirect', methods=['GET'])  # I could have chosen any name as long as it contained <token>
def redirect_():
    '''
    Redirects the user
    '''

    #@todo(sean): add control flow so we don't make new cookies if they already have one

    token_data = tokenmanager.resolve_token(token)

    redirect_url = tokenmanager.resolve_token(token)
    if redirect_url == None:
        pass #@todo(someone) make it do an error, return 500

    newcookie = uuid.uuid4().hex
    token = request.args.get('token')
    now = str(datetime.now(timezone.utc))

    redirect_obj = flask.redirect(redirect_url, code=303)
    response = make_response(redirect_obj)
    response.set_cookie('RedirectLogQ_cookie', value=cookie_value)
    hit = {
        "time": now,
        "token": token,
        "cookie": newcookie
    }
    result = db.hit_coll.insert_one(hit)
    print(locationID, token)
    return response

    # return render_template('redirect.html',url=token)


app.run()