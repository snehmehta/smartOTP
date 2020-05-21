from flask import Flask, request, render_template, flash, redirect, url_for
from pymongo import MongoClient

import requests
import http.client
import json
import helper
import os 

app = Flask(__name__)

db_user = os.environ.get('db_user')
db_password = os.environ.get('db_pass')
msg91_authkey = os.environ.get('msg91_authkey')

client = MongoClient(f"mongodb+srv://unlikely:coolperson@cluster0-jvfen.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('smartOTP')
notp_colls = db.notp
totp_colls = db.totp
suspicious_colls = db.suspicious


@app.route('/')
def index():
    ip = request.remote_addr
    is_suspicious = helper.is_suspicious(suspicious_colls, ip)

    if is_suspicious:
        data = requests.get(
            f"http://api.ipstack.com/{ip}?access_key=7897b68ab057b85542c588eec25a6a24&format=1")
    #     data = requests.get(
    #         f"http://api.ipstack.com/123.201.227.38?access_key=7897b68ab057b85542c588eec25a6a24&format=1")
        
        return render_template('suspicious.html', data = data)

    return render_template('index.html')

@app.route('/home')
def home():

    return render_template('home.html')




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
    otp = otp.strip()
    notp = helper.isOTP(notp_colls, otp)
    totp = helper.isOTP(totp_colls, otp)

    data = helper.fake_data_generator()
    
    if notp:
        return render_template('bankPage.html', data=data)

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
        return render_template('suspicious.html', data = data)

    return json.dumps({"Message": "Wrong OTP"})


@app.route('/sendOTP', methods=['POST'])
def sendsms():
    
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
    flash(f"Your OTP is {notp} if you haven't asked for otp then send this otp to track spammer {topt}")
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


        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = 'hehehaha'
    app.run(debug=True)
