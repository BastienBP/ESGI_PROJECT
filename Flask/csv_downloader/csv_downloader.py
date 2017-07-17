# -*- coding: utf-8 -*-

import pandas as pd
import pyhs2
import ConfigParser
#import request

cfg = ConfigParser.ConfigParser()
cfg.read("cluster.cfg")
host_adress = cfg.get("CLUSTER","adress")
user = cfg.get("CLUSTER","user")
password = cfg.get("CLUSTER","password")

def connector():
    conn =  pyhs2.connect(host=host_adress,port=10000,authMechanism="PLAIN",user=user,password=password,database="default")
    cur = conn.cursor()
    print "connecting to hive...."
    return cur

#cur.fetchone()

def dataset_twitter(cur):
    cur.execute("select count(*)from kafka")
    total_row = cur.fetchone()
    cur.execute("select * from kafka")

    my_list_from_table = []
    for i in range(total_row[0]):
        my_list_from_table.append(cur.fetchone())

    #Building the dataframe:
    df_twitter = pd.DataFrame(my_list_from_table[1:])
    df_twitter.columns = ['id', 'value', 'time']
    #Deleting the unwanted car
    print "creating twitter csv"
    df_twitter.to_csv("/src/csv/twitter.csv")

def dataset_indicator(cur):
    cur.execute("select count(*)from indicator")
    total_row = cur.fetchone()

    cur.execute("select * from indicator")

    my_list_from_table = []
    for i in range(total_row[0]):
        my_list_from_table.append(cur.fetchone())

    #Building the dataframe:
    df_indicator = pd.DataFrame(my_list_from_table[1:])
    df_indicator.columns = ['year','week','indicator','inc','inc_low','inc_up','inc100','inc100_low','inc100_up','geo_insee','geo_name']
    print "creating indicator csv"
    df_indicator.to_csv("/src/csv/indicator.csv")

def graph_year_inc(cur):
    cur.execute("select count(*)from indicator")
    total_row = cur.fetchone()
    print total_row

    cur.execute("select * from indicator")

    my_list_from_table = []
    for i in range(total_row[0]):
        my_list_from_table.append(cur.fetchone())

    #Building the dataframe:
    df_ = pd.DataFrame(my_list_from_table[1:])
    df_.columns = ['year','week','indicator','inc','inc_low','inc_up','inc100','inc100_low','inc100_up','geo_insee','geo_name']
    df_ = df_.groupby(['year'],as_index=False).sum()
    print df_

    df_ = df_[['year', 'inc']].copy()
    df_.columns = ['x', 'y']

    list_year = ",".join(str(x) for x in (df_['x'].values.tolist()))
    list_inc = ",".join(str(x) for x in (df_['y'].values.tolist()))

    list_year.split(',')
    list_inc = list_inc.replace(',',' ')



print "beginning something..."
cur = connector()
dataset_indicator(cur)
dataset_twitter(cur)

