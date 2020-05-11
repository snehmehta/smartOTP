# from random import randint


# def generatorOTP():
#     otp = ''
#     for i in range(6):
#         i = randint(0, 9)
#         otp += str(i)

#     return otp
# # print(generator())

# def savetotp(topt):
#     print('Tracker otp is saved')


# def sendotp():

#     notp = generatorOTP()

#     topt = generatorOTP()

#     savetotp(topt)

#     message = f"Your otp is : {notp} \n \nif you haven't asked for otp then send this otp to track spammer : {topt}"

#     print(message)

# sendotp()
import pyotp 

totp = pyotp.TOTP('base32secret3232')

print(totp.now())

totp.verify("171048")


