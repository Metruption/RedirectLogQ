'''
This file contains functions that deal with the tokens of URLs.
'''
import base62
import requests

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

	@hopefully_helpful:

	Takes a given URL and generates a token for it that no other url in the database has.

	We take the given URL and then modify it so that the the result is a token that won't be shared between two db entries:

	If there are five entries in the db...
	"www.example.com" becomes "www5.5example5.5com"

	Then we encode it in base62 [A-Za-z0-9]
	'''
	#@todo(aaron) have it request the URL to make sure it's ok
	r = requests.get(url)
	if r.status_code != 200:
		return None

	db_size = None #@todo(aaron) find out how many dictionaries are in the collection
	replace_string = "{}.{}".format(db_size,db_size)
	url = url.replace(".",replace_string)

	token = base62.encode(url)

	return token

def resolve_token(token):
	'''
	@params:
		token is a string hopefully containing a valid token
	
	@preconditions:
		there is an entry in the redirects collection of the db that has the token associated with a url

	@postconditions:
		returns the URL associated with the token if the precondtions are met
		otherwise returns None
	'''
	pass #@todo(aaron) code this