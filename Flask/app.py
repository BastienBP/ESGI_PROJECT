# -*- coding: utf-8 -*-

import pandas as pd


from flask import Flask
from flask import request
from flask import render_template
import json
import pyhs2
import ConfigParser
#import request

def dataset_twitter():
    df_twitter = pd.read_csv("./csv/twitter.csv")
    df_twitter = df_twitter[1:]
    df_twitter.columns = ['','id', 'value', 'time']
    df_twitter = df_twitter[['id', 'value', 'time']].copy()

    #Deleting the unwanted car
    return df_twitter



def dataset_indicator():
    df_indicator = pd.read_csv("./csv/indicator.csv")
    df_indicator = df_indicator[1:]

    df_indicator.columns = ['','year','week','indicator','inc','inc_low','inc_up','inc100','inc100_low','inc100_up','geo_insee','geo_name']
    df_indicator = df_indicator[['year','week','indicator','inc','inc_low','inc_up','inc100','inc100_low','inc100_up','geo_insee','geo_name']].copy()
    return df_indicator

#curr = connector()
#dataset_indicator(curr)

def graph_year_inc():
    df_ = pd.read_csv("./csv/indicator.csv")
    #Building the dataframe
    df_ = df_[1:]
    df_.columns = ['','year','week','indicator','inc','inc_low','inc_up','inc100','inc100_low','inc100_up','geo_insee','geo_name']
    print df_
    df_ = df_.groupby(["year"],as_index=False).sum()
    df_ = df_[['year', 'inc']].copy()
    df_.columns = ['x', 'y']

    list_year = ",".join(str(x) for x in (df_['x'].values.tolist()))
    list_inc = ",".join(str(x) for x in (df_['y'].values.tolist()))

    list_year.split(',')
    list_inc.split(',')

    return list_year, list_inc

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data",methods=['GET','POST'])
def get_var():
    var = request.form.get('table')

    if(var == "indicator"):
        df = dataset_indicator()
        return render_template('dataframe.html',title ="Dataset des Indicateurs ", table = df.to_html())

    elif(var == "twitter"):
        df = dataset_twitter()
        return render_template('dataframe.html',title ="Dataset des Tweets", table = df.to_html())

    else:
        return render_template('index.html')

@app.route("/graph_year_inc",methods=['GET','POST'])
def get_graph():
    #curr = connector()
    x,y = graph_year_inc()

    return render_template('graph_year_inc.html',x=x,y =y)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

