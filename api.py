import flask
from flask import render_template

# Flask Configuration

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/api/v1/ops/add', methods=['POST'])
def op_add():
    pass

@app.route('/api/v1/ops/subtract', methods=['POST'])
def op_subtract():
    pass

@app.route('/api/v1/ops/multiply', methods=['POST'])
def op_multiply():
    pass

@app.route('/api/v1/ops/divide', methods=['POST'])
def op_divide():
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_not_found.html'),404

# Local Configuration

app.run()
