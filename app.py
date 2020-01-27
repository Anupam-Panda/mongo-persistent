from flask import Flask, request, jsonify
import os
import pymongo
from bson.json_util import dumps
app = Flask(__name__)

class mongoInstance :
    def __init__(self):
        self.myclient = pymongo.MongoClient('mongodb://172.30.234.111:27017')
        self.mydb = self.myclient["sampledb"]
        self.mycol = self.mydb["persons"]

@app.route("/autobot", methods=['GET'])
def getAutobot():
    name = request.args['name']
    return dumps(getMongoData(name))

def getMongoData(name) :
    mongo_ref = mongoInstance()
    myquery = {"name": name}
    result = []
    myrecord = mongo_ref.mycol.find(myquery)
    print (myrecord)
    #return (list(myrecord))
    for entry in myrecord :
        result.append({'name': entry['name'], 'age': entry['age']})
    print (result)
    return (result)

@app.route("/autobot" , methods=['POST'])
def addAutobot () :
    mongo_ref = mongoInstance()
    data = request.get_json()
    entry = mongo_ref.mycol.insert_one(data)
    return dumps(mongo_ref.mycol.find_one({"_id": entry.inserted_id}))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
