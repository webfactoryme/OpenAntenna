import MySQLdb
from datetime import datetime
import requests
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text

app = Flask(__name__)

# Create connection to the database
engine = create_engine("mysql://openantenna:password@localhost:3306/openantenna") 
meta = MetaData(bind=engine)
MetaData.reflect(meta)
db = SQLAlchemy(app)

# Identify the log location
log_location = '/var/log/apache2/openantenna-access.log'

with open(log_location) as fp:  
    for line in fp:
        ip_address = line.split(' ')[0]
        time = line.split('[')[1].split(']')[0].split(' +')[0]
        method = line.split('"')[1].split('"')[0].split(' ')[0]
        request = line.split('"')[1].split('"')[0].split(' ')[1]
        referral = line.split('"')[3].split('"')[0]
        client = line.split('"')[5].split('"')[0]
        response = line.split('"')[2].split('"')[0].split(' ')[1].replace(' ','')
        # Check to see if data is already in database
        sql = text("SELECT * FROM openantenna.analytics WHERE ip ='{}' AND time ='{}' AND request ='{}';".format(ip_address,time,request))
        data = engine.execute(sql)
        # If not, insert into the database
        if len(data) == 0:            
            # Try to scrape location data for the IP address
            try:
                location_data = requests.get("https://geolocation-db.com/json/{}&position=true".format(ip_address)).json()
                country = location_data['country_code']
                city = location_data['city']
                postal = location_data['postal']
                latitude = location_data['latitude']
                longitude = location_data['longitude']
                state = location_data['state']

                sql = text("INSERT INTO openantenna.analytics VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}',now(),'{}','{}','{}','{}','{}','{}')".format(ip_address,time,method,request,referral,client,response,country,city,state,latitude,longitude,postal,))
                data = engine.execute(sql)
                db.commit()
                print('Added new line of data with location information:')
                print(line + '\n')
            # If problem with scraping location data, insert with NULL values    
            except: 
                sql = text("INSERT INTO openantenna.analytics VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}',now(),NULL,NULL,NULL,NULL,NULL,NULL)".format(ip_address,time,method,request,referral,client,response))
                data = engine.execute(sql)
                db.commit()
                print('Added new line of data WITHOUT location information:')
                print(line + '\n')
        else:
            pass
