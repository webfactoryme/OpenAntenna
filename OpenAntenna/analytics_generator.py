import MySQLdb
from datetime import datetime
import requests

# Create connection to the database
db = MySQLdb.connect(host="host",user="user",passwd="password",db="openantenna",port=3306)

# Identify the log location
log_location = '/var/log/apache2/leadandcircus-access.log'

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
        cursor = db.cursor()
        cursor.execute("SELECT * FROM leadandcircus.analytics WHERE ip ='{}' AND time ='{}' AND request ='{}';".format(ip_address,time,request))
        data = cursor.fetchall()
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
                cursor = db.cursor()
                cursor.execute("INSERT INTO leadandcircus.analytics VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}',now(),'{}','{}','{}','{}','{}','{}')".format(ip_address,time,method,request,referral,client,response,country,city,state,latitude,longitude,postal,))
                db.commit()
                print('Added new line of data with location information:')
                print(line + '\n')
            # If problem with scraping location data, insert with NULL values    
            except: 
                cursor = db.cursor()
                cursor.execute("INSERT INTO leadandcircus.analytics VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}',now(),NULL,NULL,NULL,NULL,NULL,NULL)".format(ip_address,time,method,request,referral,client,response))
                db.commit()
                print('Added new line of data WITHOUT location information:')
                print(line + '\n')
        else:
            pass