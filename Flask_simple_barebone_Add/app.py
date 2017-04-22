from flask import Flask, make_response, jsonify, request
import os

DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
	return make_response(open(os.path.join(DIR, 'index.html')).read())


@app.route('/result', methods=['POST'])
def result():
	a = request.args.get('a',0, type=int)
	b = request.args.get('b',0, type=int)
	return jsonify(result= a + b)

if __name__ == '__main__':
	app.run(debug=True)
