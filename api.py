import flask
from flask import redirect, render_template, url_for
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, emit

# Flask Configuration

app = flask.Flask(__name__)
api = Api(app)
socketio = SocketIO(app)

# Config Vals

# The maximum number of equations to display at once.
MAX_EQNS = 10

# App route configuration

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return redirect(url_for("home"))

@app.route('/home', methods=['GET'])
def home():
    # eqns is the list of dictionary equations, and pretty_eqn is the function to pretty-ify an idividual eqn dict.
    return render_template('home.html', eqns = eqns, pretty_eqn = pretty_eqn)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_not_found.html'),404

@app.errorhandler(500)
def internal_error(e):
    print("----- INTERNAL ERROR -----")

# Classes

class Eqn:
    def __init__(self, a, op, b):
        """Assign the Eqn object's vals, including the result"""
        self.a = float(a)
        self.op = op
        self.b = float(b)
        self.result = self.calc(self.a, self.op, self.b)

    def calc(self, a, op, b):
        """Calculate the result of the equation using the input numbers and their infix operator"""
        if op == "a":
            return a + b
        elif op == "s":
            return a - b
        elif op == "d":
            if b == 0:
                return "Undefined"
            return a / b
        elif op == "m":
            return a * b

    def to_dict(self):
        """General-use function to turn the Eqn's values, including result, into a dict object"""
        return {"a":self.a, "op":self.op, "b":self.b, "result":self.result}

class EqnRESTer(Resource):
    def get(self):
        """Return the current list of equations"""
        return eqns, 200

    def post(self):
        """Add a new equation to the existing list of equations"""
        parser = reqparse.RequestParser()
        parser.add_argument("a")
        parser.add_argument("op")
        parser.add_argument("b")
        args = parser.parse_args()

        latest_eqn = Eqn(args["a"],args["op"],args["b"]).to_dict()

        if validate_eqn(latest_eqn) == None:
            return None, 500

        if(len(eqns) >= MAX_EQNS):
            eqns.pop(0)
        eqns.append(latest_eqn)

        # Send the list in reverse order
        socketio.emit('eqn_update', {"eqn_list": list(map(pretty_eqn, eqns))[::-1]}, namespace='/eqnio')

        return latest_eqn, 201

    def put(self):
        """Replace the most recent equation in the list of equations with the input, or add a new equation if the list of equations is empty"""
        parser = reqparse.RequestParser()
        parser.add_argument("a")
        parser.add_argument("op")
        parser.add_argument("b")
        args = parser.parse_args()

        latest_eqn = Eqn(args["a"],args["op"],args["b"]).to_dict()

        if validate_eqn(latest_eqn) == None:
            return None, 500

        if len(eqns) > 0:
            eqns[-1] = latest_eqn
        else:
            eqns.append(latest_eqn)
        
        # Send the list in reverse order
        socketio.emit('eqn_update', {"eqn_list": list(map(pretty_eqn, eqns))[::-1]}, namespace='/eqnio')

        return latest_eqn, 201

    def delete(self):
        """Delete the contents of the list of equations"""
        # Use eqns in the global context to empty it
        global eqns
        eqns = []
        socketio.emit('eqn_update', {"eqn_list": list(map(pretty_eqn, eqns))[::-1]}, namespace='/eqnio')
        return "Equations list emptied", 200

# Global Vars

eqns = []

# Helper Funcs

def pretty_eqn(eqn):
    """Convert a dict representation of an equation into a pretty string"""
    #The lack of validation in this function is due to it being used in validate_eqn() as well.
    pretty_a = pretty_num(eqn['a'])
    pretty_b = pretty_num(eqn['b'])
    pretty_r = pretty_num(eqn['result'])
    op = eqn['op']

    if op == "a":
        pretty_op = "+"
    elif op == "s":
        pretty_op = "-"
    elif op == "d":
        pretty_op = "÷"
    elif op == "m":
        pretty_op = "×"
    return "{} {} {} = {}".format(pretty_a,pretty_op,pretty_b,pretty_r)

def pretty_num(num):
    """Turn a potentially UGLY number into a generally-formatted number, for viewers' eyes"""
    if type(num) == int or type(num) == float:
        #Format with the general numerical format to allow for better display with very small (<1) and very large numbers, as well as to trim unnecesary decimals.
        return '{0:g}'.format(num)
    else:
        return num

def validate_eqn(eqn):
    """Utilize the pretty_eqn function in order to check if a given eqn object isn't up to pretty equation standards"""
    try:
        return pretty_eqn(eqn)
    except:
        return None

# Launch

api.add_resource(EqnRESTer, "/api/eqn")
socketio.run(app)
