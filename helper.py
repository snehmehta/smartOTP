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

    records = collection_ins.find_one({'ip': ip})

    if records and len(list(records)) > 0:

        return True

    return False


def fake_data_generator():
    import random 
    from faker import Faker

    fake = Faker('en_IN')
    Faker.seed(4521)

    data = []
    for _ in range(10):

        temp = []

        temp.append(fake.name())
        temp.append(fake.sentence())
        temp.append(round(random.randint(90000,120000)/1000)*1000)
        temp.append(fake.date())
        temp.append(fake.time_object())

        data.append(temp)

    return data