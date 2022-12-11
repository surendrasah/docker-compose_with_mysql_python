#!/usr/bin/env python

import json
import mysql.connector
import pandas as pd
import yaml
from sqlquery import *


class ETLTEST():

    def __init__(self):
        self.params = self.get_yaml_param()
        self.mysql_connect = self.get_mysql_connection()
        

    def get_yaml_param(self):
        yaml_path=  './config.yml'
        with open(yaml_path) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            params = yaml.load(file, Loader=yaml.FullLoader)
        return params


    def get_mysql_connection(self):
        mysql_connector = mysql.connector.connect(
            host = self.params["mysql_connection"]["mysql_hostname"],
            user = self.params["mysql_connection"]["mysql_username"],
            db = self.params['mysql_connection']['mysql_database'],
            password = self.params["mysql_connection"]["mysql_password"],
            port = self.params["mysql_connection"]["mysql_port"],
            autocommit = True
        )
        return mysql_connector


    def save_json(self,sqlquery, filename):
        
        #open connection to fetch data
        with self.mysql_connect.cursor() as cursor:
            cursor.execute(sqlquery)
            data = cursor.fetchall()
            if "example" in filename: 
                rows = [{'id': row[0], 'name': row[1]} for row in data]
            elif "people" in filename:
                rows = [{'given_name': row[0], 'family_name': row[1], 'date_of_birth': row[2], 'place_of_birth': row[3]} for row in data]
            elif "place" in filename:
                rows = [{'city': row[0], 'county': row[1], 'country': row[2]} for row in data]
            elif "summary" in filename:
                rows = [{row[0]: row[1]} for row in data]
            else:
                print("wrong filename")

        
        #save json
        with open(filename +'.json', 'w', encoding='utf-8') as json_file:  
            json.dump(rows, json_file, separators=(',', ':'),default=str)



    def read_insert_examplestb(self):
    
        #read file:
        with open('/data/example.csv') as csv_file:
            example_df = pd.read_csv(csv_file, index_col=False, delimiter = ',')

        print("Record insertion started in examples table")

        #table creation and data insertion
        with self.mysql_connect.cursor() as cursor:
            cursor.execute(drop_examplestable())
            print('Creating table....example')                 
            cursor.execute(create_examplestable())
            print("Table is created....example")
            
            #loop through the data frame
            for i,row in example_df.iterrows():

                sql = insert_exampletable()
                cursor.execute(sql, tuple(row))
                self.mysql_connect.commit()
            
            print("Record inserted in examples table")
            
            #call save_json function
            filename = "/data/example_python"
            self.save_json(select_examplestable(),filename)
            print("examples table execution is over")

    def read_insert_peopletb(self):
    
        #read file:
        with open('/data/people.csv', encoding="utf-8") as csv_file:
            people_df = pd.read_csv(csv_file)

        #table creation and data insertion
        print("Record insertion started in people table")
        with self.mysql_connect.cursor() as cursor:
            #loop through the data frame
            for i,row in people_df.iterrows():
                sql = insert_peopletable()
                cursor.execute(sql, tuple(row))
                self.mysql_connect.commit()
            
            print("Record inserted in people table")
            
            #call save_json function
            filename = "/data/people_python"
            self.save_json(select_peopletable(),filename)
            print("people table execution is over")

    def read_insert_placestb(self):
    
        #read file:
        with open('/data/places.csv', encoding="utf-8") as csv_file:
            places_df = pd.read_csv(csv_file)

        print("Record insertion started in places table")
        #table creation and data insertion
        with self.mysql_connect.cursor() as cursor:
            #loop through the data frame
            for i,row in places_df.iterrows():
                sql = insert_placestable()
                cursor.execute(sql, tuple(row))
                self.mysql_connect.commit()
            
            print("Record inserted in places table")

            #call save_json function
            filename = "/data/places_python"
            self.save_json(select_placestable(),filename)
            print("places  table execution is over")
            
            
            
    def summary(self):
        with self.mysql_connect.cursor() as cursor:
            print("summary output is initiated")
            filename ="/data/summary_output"
            self.save_json(summary_query(),filename)
            print("summary output execution is over")



if __name__=='__main__':
    etltest = ETLTEST()
    etltest.read_insert_examplestb()
    etltest.read_insert_peopletb()
    etltest.read_insert_placestb()
    etltest.summary()
    
