'''
This file contains functions that deal with the tokens of URLs.
'''
import base62
import requests
import uuid

def generate_token(url):
	'''
	Generates a token for a given URL. Makes sure tokens are never repeated, even if same URL is given twice.

	@params:
		url is a string hopefully containing a valid url

	@preconditions:
		url is a valid url and any requests to it will return a 200

	@postconditions:
		returns a tokenized URL if the preconditons are met
		otherwise returns None
	'''
	headers = {'user-agent': 'RedirectLogQ'}
	r = requests.get(url, headers=headers)
	if r.status_code != 200:
		return None

	token = uuid.uuid4().int
	token = base62.encode(token)

	return token

def resolve_token(flier_coll, token):
	'''
	@params:
		token is a string hopefully containing a valid token
	
	@preconditions:
		there is an entry in the redirects collection of the db that has the token associated with a url

	@postconditions:
		returns the URL associated with the token if the precondtions are met
		otherwise returns None
	'''
	cursor = flier_coll.find_one({"token": token})
	url = cursor['real_url']
	return url