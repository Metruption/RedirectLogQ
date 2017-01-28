#!/usr/bin/env python3
'''
    A simple URL redirection backend that logs the time of each redirection.
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
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/redirect.php?token=<token>')
def redirect(token):
	'''
	Redirects the user
	@todo(aaron):
		1) learn how to have a database
		2) learn how to generate lots of different URLs
		3) make sure the database is setup right
		4) write code so that the databse has logs of all the stuff
		5) you win!
	'''
	return render_template('redirect.html',url=token)

app.run()