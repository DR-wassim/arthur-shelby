import pymongo

# myclient = pymongo.MongoClient("mongodb+srv://wassim_boss:A2J81EAAB6@cluster0.dj7u9.mongodb.net/Cluster0?retryWrites=true&w=majority")


myclient = pymongo.MongoClient("mongodb+srv://wassim_boss:A2J81EAAB6@cluster0.dj7u9.mongodb.net/sample_airbnb?retryWrites=true&w=majority")



mydb = myclient["mydatabase"]

mycol = mydb["customers"]

print(mycol)
print(mydb.list_collection_names())