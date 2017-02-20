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

from flask import Flask, abort, make_response, redirect, render_template, request
from pymongo import MongoClient

import token_handler
import config

mysecret = config.SECRET

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
def display_form():
	'''
	@todo(aaron): decide if it's worth your time making a comment for this
	'''
	secret_hidden = mysecret == None
	return render_template('form.html', secret_hidden=secret_hidden)


@app.route('/handle_form', methods=['POST'])
def handle_form():
	'''
	@preconditions:
		the post has the arguments 'url' and 'location_description'
			url is a valid url
			location_description is a string and should be meaningful to a human reader
	@postconditions:
		returns Success if the url is valid after a flier is added to the database
		returns Failure if something is awry (either user input or the db poops its pants)
	'''
	url = request.form['url']
	location_description = request.form['location_description']
	secret = request.form['secret']

	token = token_handler.generate_token(url)
	if mysecret != None and secret != mysecret:
		return "Failure"


	if token == None:
		print("An error has occured. The url {} is not valid.".format(url))
		return "Failure"
	else:
		flier = {
			"real_url": url,
			"token": token,
			"location_description": location_description
		}   
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
	token = request.args.get('token')

	redirect_url = token_handler.resolve_token(flier_coll, token)

	if redirect_url == None:
		abort(500)

	now = str(datetime.now(timezone.utc))

	redirect_obj = redirect(redirect_url, code=303)
	response = make_response(redirect_obj)

	has_cookie = False
	try:
		if 'RedirectLogQ_cookie' in request.cookies:
			has_cookie = True
			cookie_value = request.cookies['RedirectLogQ_cookie']
		else:
			cookie_value = uuid.uuid4().hex
			response.set_cookie('RedirectLogQ_cookie', value=cookie_value, max_age="315360000")
	except KeyError:
		cookie_value = uuid.uuid4().hex
		response.set_cookie('RedirectLogQ_cookie', value=cookie_value, max_age="315360000")

	hit = {
		"time": now,
		"token": token,
		"cookie": cookie_value
	}
	result = db.hit_coll.insert_one(hit)
	return response

app.run()