from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://unlikely:coolperson@cluster0-jvfen.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('smartOTP')

normal_otp = db.notp

# print(normal_otp.count_documents({}))

# normal_otp.insert_one({
#     'otp': '480231'
# })
# print(normal_otp.count_documents({}))
search = normal_otp.find({'otp': '480231'})
print(list(search))
otps = list(normal_otp.find())

print(otps)