from flask import Flask, request
# from flask_pymongo import PyMongo

import http.client
import json
import helper

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb+srv://unlikely:<coolperson>@cluster0-5cxq4.mongodb.net/test?retryWrites=true&w=majority"
# mongo = PyMongo(app)
# database = mongo.


@app.route('/')
def index():
    # collection = mongo.db.get_collection(name='otp')
    # print(collection)
    return 'hello ! Welcome to smart OTP '


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return json.dumps({'ip': request.remote_addr}), 200


@app.route('/verifyOTP', methods=['POST'])
def verifyOTP():

    otp = request.form['otp']

    notp = helper.isnOTP(otp)
    totp = helper.istOTP(otp)

    if notp:
        return 'verified'

    elif totp:
        return 'Tracked otp'

    return 'wrong otp'


@app.route('/sendOTP', methods=['POST'])
def sendsms():

    number = request.form['number']
    #  OTP GENERATION
    notp = helper.generatorOTP()
    topt = helper.generatorOTP()

    helper.savetotp(topt)

    message = f"Your otp is {notp} \n \n if you haven't asked for otp then send this otp to track spammer {topt}"

    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = json.dumps({
        'sender': 'SmtOTP',
        'route': '4',
        'country': '91',
        'sms': [
            {
                'message': message,
                'to': [
                    number
                ]
            }
        ]
    })

    headers = {
        'authkey': "286418A1HQ6wYO6q5e609da2P1",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


if __name__ == "__main__":
    app.run(debug=True)
