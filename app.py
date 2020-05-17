from flask import Flask, request, render_template
from pymongo import MongoClient

import requests
import http.client
import json
import helper

app = Flask(__name__)


client = MongoClient(
    "mongodb+srv://unlikely:coolperson@cluster0-jvfen.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('smartOTP')
notp_colls = db.notp
totp_colls = db.totp
suspicious_colls = db.suspicious


@app.route('/')
def index():

    return render_template('index.html')


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    try:
        real_ip = request.headers['X-Forwarded-For']

        return json.dumps({'real_ip': real_ip, 'redirect_ip': request.remote_addr}), 200
    except:
        return json.dumps({'redirect_ip': request.remote_addr}), 200


@app.route('/verifyOTP', methods=['POST'])
def verifyOTP():

    otp = request.form['otp']

    notp = helper.isOTP(notp_colls, otp)
    totp = helper.isOTP(totp_colls, otp)

    if notp:
        return json.dumps({"Message": "Hello Legit USER"})

    elif totp:
        try:
            ip = request.headers['X-Forwarded-For']

        except:
            ip = request.remote_addr

        helper.suspicious(suspicious_colls, ip)

        data = requests.get(
            f"http://api.ipstack.com/{ip}?access_key=7897b68ab057b85542c588eec25a6a24&format=1")
        data = json.loads(data.text)

        data['INFO'] = "We suspect you as scammer"
        data['Scammer Details'] = " Following Are your Potential Details"
        return data

    return json.dumps({"Message": "Wrong OTP"})


@app.route('/sendOTP', methods=['POST'])
def sendsms():
    # print(request.form)
    number = request.form['number']
    try:
        send_to_mobile = request.form['mobile']

    except:
        send_to_mobile = False

    #  OTP GENERATION
    notp = helper.generatorOTP()
    topt = helper.generatorOTP()

    helper.saveotp(notp_colls, totp_colls, notp, topt)

    message = f"Your otp is {notp} \n \n if you haven't asked for otp then send this otp to track spammer {topt}"
    if send_to_mobile:
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
    else:
        return json.dumps({"Message": message})


if __name__ == "__main__":
    app.run(debug=True)
