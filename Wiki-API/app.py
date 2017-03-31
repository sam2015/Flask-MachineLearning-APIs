from flask import Flask, jsonify, render_template
from wiki_utils.Wiki_exc import wiki_content_extractor

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/wiki/<string:title>', methods=['GET'])
def extract(title):
	data = wiki_content_extractor(title=title)
	label = [data[i][0] for i in range(len(data))]
	freq = [data[i][1] for i in range(len(data))]
	return jsonify(label=label, freq=freq)


if __name__ == '__main__':
	app.run()
