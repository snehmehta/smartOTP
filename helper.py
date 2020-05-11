from random import randint


def savetotp(topt):
    print('Tracker otp is saved')


def generatorOTP():
    otp = ''
    for i in range(6):
        i = randint(0, 9)
        otp += str(i)

    return otp



def isnOTP(otp):
    return True


def istOTP(otp):
    return False
