from pymongo import *
from flask import Blueprint, request, send_file
import pandas as pd
import json

mongo2 = Blueprint('mongodb2', __name__)

client = MongoClient('mongodb+srv://ajay:ajaymongo@cluster0.ntpzikj.mongodb.net/?retryWrites=true&w=majority')
db = client['salesdata']
collection = db['test5']


@mongo2.route("/mongodb2", methods=['GET', 'POST'])
def index():
    try:
        print("MongoDB upload")
        collection.drop()
        if 'files' not in request.files:
            print("No File in Request")
            return "No file has been sent"
        file = request.files['files']
        if file.filename == "":
            print("File not Attached")
            return "Please Attach a file"
        if file:
            df = pd.read_csv(file)
            records = df.to_dict("records")
            collection.insert_many(records)
            return "DataFrame uploaded successfully!"
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print("Please Update IP in MongoDB")
    except:
        print("Some Error Occurred")
        return "Error Occurred"

@mongo2.route("/mongodbget", methods=['GET', 'POST'])
def index22():
    cursor = collection.find({})
    records = list(cursor)
    df = pd.DataFrame(records)
    df.drop(['_id'], axis=1, inplace=True)
    return df.to_html()
