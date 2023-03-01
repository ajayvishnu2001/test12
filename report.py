from flask import Blueprint
from pymongo import MongoClient
import pandas as pd
from ydata_profiling import ProfileReport

pand_rep = Blueprint('report', __name__)

client = MongoClient('mongodb+srv://ajay:ajaymongo@cluster0.ntpzikj.mongodb.net/?retryWrites=true&w=majority')
db = client['salesdata']
collection = db['test5']


class st_class:
    stc_html = ""


@pand_rep.route("/")
def ind14():
    return "Home page"

@pand_rep.route("/report_disp")
def ind11():
    try:
        print("Report Generation")
        cursor = collection.find({})
        records = list(cursor)
        print("Report Generation")
        df = pd.DataFrame(records)
        df.drop(['_id'], axis=1, inplace=True)
        profile = ProfileReport(df, explorative=True)
        html = profile.to_html()
        st_class.stc_html = html
        return html


    except Exception as error:
        print("Some Error Occurred", error)
        return "Error Occurred"


