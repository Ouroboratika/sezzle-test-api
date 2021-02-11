import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "Placeholder"

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

app.run()
