import pymongo


client = pymongo.MongoClient("mongodb+srv://unlikely:<coolperson>@cluster0-5cxq4.mongodb.net/test?retryWrites=true&w=majority")


database = client.get_database('smartOTP')


database.client


database.current_op()



