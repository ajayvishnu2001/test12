from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from pycaret.regression import *
import pandas as pd
import numpy as np
# import mysql.connector
# from sqlalchemy import create_engine

pycaret = Blueprint('forecast', __name__)

# MongoDB Database Authentication and database registration
client = MongoClient('mongodb+srv://ajay:ajaymongo@cluster0.ntpzikj.mongodb.net/?retryWrites=true&w=majority')
db = client['salesdata']
collection = db['test5']

# MySQL database Authentication to MySQL workspace
# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     port=3307,
#     user="root",
#     password="",
#     database="test"
# )
#to use tosql()
#engine = create_engine('mysql+pymysql://root:@localhost:3307/test')

# declaring Cursor for SQL
#mycur = mydb.cursor()


# class to store static variable
class st_class:
    stc_html = ""


@pycaret.route("/forecast", methods=['GET', 'POST'])
def index23():
    try:
        print("Forecasting")
        if 'freq' not in request.form or 'period' not in request.form:
            print("Please send Values for Prediction")
            return "Please send Values for Prediction"
        frequency = request.form['freq']
        period = request.form['period']
        if frequency == "" or period == "":
            print("Please enter values")
            return "Please enter values"
        period = int(period)
        cursor = collection.find({})
        records = list(cursor)
        ed = pd.DataFrame(records)
        ed.drop(['_id'], axis=1, inplace=True)
        ed.dropna(how='all', inplace=True)
        ed = ed.loc[:, ['Date', ed.columns[-1]]]

        ed['Date'] = pd.to_datetime(ed['Date'])
        ed['Series'] = np.arange(1, len(ed) + 1)
        ed['Month'] = [i.month for i in ed['Date']]
        ed['Year'] = [i.year for i in ed['Date']]
        ed['Day'] = [i.day for i in ed['Date']]
        st_date = ed['Date'].iloc[-1]

        ed.drop(['Date'], axis=1, inplace=True)
        cols = ed.columns.tolist()
        cols = cols[-4:] + cols[:-4]
        ed = ed[cols]
        ed = ed.rename(columns={ed.columns[-1]: "y_value"})
        length_df = len(ed)
        s = setup(data=ed, target='y_value', fold_strategy='timeseries', session_id=123, fold=5, silent=True)
        best = compare_models()
        final_best = finalize_model(best)

        future_dates = pd.date_range(start=st_date, periods=period, freq=frequency)

        future_df = pd.DataFrame()

        future_df['Month'] = [i.month for i in future_dates]
        future_df['Year'] = [i.year for i in future_dates]
        future_df['Day'] = [i.day for i in future_dates]

        future_df['Series'] = np.arange(length_df, (length_df + len(future_dates)))
        predictions_future = predict_model(final_best, data=future_df)
        predictions_future['Date'] = pd.to_datetime(predictions_future[['Year', 'Month', 'Day']])
        predictions_future.drop(['Month', 'Year', 'Day', 'Series'], axis=1, inplace=True)
        predictions_future.columns = ['Sales', 'Date']
        html = predictions_future.to_html()
        st_class.stc_html = html

        # SQL code to upload
        #predictions_future.to_sql('table2', engine, if_exists='replace')  #below code to one line

        # sql = "DROP TABLE table2"
        # mycur.execute(sql)
        # col1 = predictions_future.columns[0]
        # col2 = predictions_future.columns[1]
        # table_name = "table2"
        # sql = "CREATE TABLE " + table_name + " (id INT AUTO_INCREMENT PRIMARY KEY, " + col1 + " VARCHAR(255), " + col2 + " DATETIME)"
        # print(sql)
        # mycur.execute(sql)
        # predictions_future["Date"] = predictions_future["Date"].astype('string')
        # for i, row in predictions_future.iterrows():
        #     query = "INSERT INTO " + table_name + " (" + col1 + ", " + col2 + ") VALUES (%s, %s)"
        #     values = (row[col1], row[col2])
        #
        #     mycur.execute(query, values)
        #     mydb.commit()

        return jsonify({"Data": predictions_future.to_json(orient='records', lines=True)})

    except Exception as error:
        print("Some Error Occurred", error)
        return "Error Occurred"


@pycaret.route("/algo", methods=['GET', 'POST'])
def index24():
    try:
        print("Algorithm Analyse")
        cursor = collection.find({})
        records = list(cursor)
        ed = pd.DataFrame(records)
        ed.drop(['_id'], axis=1, inplace=True)
        ed.dropna(how='all', inplace=True)
        ed = ed.loc[:, ['Date', ed.columns[-1]]]

        ed['Date'] = pd.to_datetime(ed['Date'])
        ed['Series'] = np.arange(1, len(ed) + 1)
        ed['Month'] = [i.month for i in ed['Date']]
        ed['Year'] = [i.year for i in ed['Date']]
        ed['Day'] = [i.day for i in ed['Date']]
        st_date = ed['Date'].iloc[-1]

        ed.drop(['Date'], axis=1, inplace=True)
        cols = ed.columns.tolist()
        cols = cols[-4:] + cols[:-4]
        ed = ed[cols]
        ed = ed.rename(columns={ed.columns[-1]: "y_value"})
        s = setup(data=ed, target='y_value', fold_strategy='timeseries', session_id=123, fold=3, silent=True)
        best = compare_models()
        final_best = finalize_model(best)

        return {"Model": str(final_best)}

    except Exception as error:
        print("Some Error Occurred", error)
        return "Error Occurred"


@pycaret.route("/pre_values", methods=['GET'])
def ind56():
    return st_class.stc_html