from bottle import route, run, template
from bottle import request
from bottle import redirect
from bottle import static_file
from src import web_script

@route('/')
def index():
	return template('web')

@route('/annotate', method=['GET'])
def submit():
	print(request)
	text = request.params.comments
	output = web_script.run_ner(text)
	return output

@route('/src/<filename:path>')
def fileget(filename):
	return static_file(filename, root='./src/')

run(host='localhost', port=8095)
