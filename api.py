import flask
from flask import redirect, render_template, url_for
from flask_restful import Api, Resource, reqparse

# Flask Configuration

app = flask.Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

# Config Vals

MAX_EQNS = 10

# App route configuration

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return redirect(url_for("home"))

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', eqns = eqns, pretty_eqn = pretty_eqn)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_not_found.html'),404

# Classes

class Eqn:
    def __init__(self, a, op, b):
        self.a = int(a)
        self.op = op
        self.b = int(b)
        self.result = self.calc(self.a, self.op, self.b)

    def calc(self, a, op, b):
        if op == "a":
            return a + b
        elif op == "s":
            return a - b
        elif op == "d":
            return a / b
        elif op == "m":
            return a * b

    def to_dict(self):
        return {"a":self.a, "op":self.op, "b":self.b, "result":self.result}

class EqnRESTer(Resource):
    def get(self):
        return eqns, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("a")
        parser.add_argument("op")
        parser.add_argument("b")
        args = parser.parse_args()

        latest_eqn = Eqn(args["a"],args["op"],args["b"]).to_dict()

        if(len(eqns) >= MAX_EQNS):
            eqns.pop(0)
        eqns.append(latest_eqn)

        return latest_eqn, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("a")
        parser.add_argument("op")
        parser.add_argument("b")
        args = parser.parse_args()

        latest_eqn = Eqn(args["a"],args["op"],args["b"]).to_dict()

        if len(eqns) > 0:
            eqns[-1] = latest_eqn
        else:
            eqns.append(latest_eqn)
        
        return latest_eqn, 201

    def delete(self):
        global eqns
        eqns = []
        return "Equations list emptied", 200

# Global Vars

eqns = []

# Helper Funcs

def pretty_eqn(eqn):
    op = eqn["op"]
    if op == "a":
        pretty_op = "+"
    elif op == "s":
        pretty_op = "-"
    elif op == "d":
        pretty_op = "÷"
    elif op == "m":
        pretty_op = "×"
    return "{} {} {} = {}".format(eqn["a"],pretty_op,eqn["b"],eqn["result"])

# Launch

api.add_resource(EqnRESTer, "/eqn")
app.run()
