from main import recommend, purchase, check_credential

RATIO = 0.5

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=["POST"])
def login():
    body = request.get_json(force=True)
    creds = {
        'userID': body['userID'],
        'password': body['password']
    }
    return jsonify({ 'Valid': check_credential(creds['userID'], creds['password']) });

@app.route('/home/<int:userID')
def home(userID):
    return recommend(userID=userID, ratio=RATIO)

@app.route('/purchase', methods=["POST"])
def do_purchase():
    body = request.get_json(force=True)
    purchase(body['userID'], body['productID'])