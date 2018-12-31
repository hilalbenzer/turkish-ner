from bottle import route, run, template
from bottle import request
from bottle import redirect
import find_named_entities

@route('/')
def index():
	return template('web')

@route('/annotate', method=['GET'])
def submit():
	print(request)
	text = request.params.comments
	# package = str(request.GET.get('comments'))
	output = find_named_entities.run_ner(text)
	return output

run(host='localhost', port=8075)
