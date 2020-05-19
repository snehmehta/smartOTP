from random import randint
from datetime import datetime


def saveotp(n_colls, t_colls, notp, totp):
    n_colls.insert_one({'otp': notp})
    t_colls.insert_one({'otp': totp})
    print('otps is saved')


def generatorOTP():
    otp = ''
    for i in range(6):
        i = randint(0, 9)
        otp += str(i)

    return otp


def isOTP(collection_ins, otp):
    records = collection_ins.find_one({'otp': otp})
    if records:
        return True
    return False


def suspicious(collection_ins, ip):
    collection_ins.insert_one({'ip': ip, 'tracked_at': datetime.now()})

def is_suspicious(collection_ins, ip):

    records = collection_ins.find_one({'ip' : ip})

    if records and len(list(records)) > 0:

        return True
    
    return False
        