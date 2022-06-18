#!/usr/bin/env python

import MySQLdb
import os
from podgen import Podcast, Person, Media, Category, htmlencode
import datetime
import pytz
import time
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text


app = Flask(__name__)

# Database Connection

engine = create_engine(
    "mysql://user:1234@localhost:3306/openantenna")        # substitue the 'user:1234@localhost:3306/openantenna' with <username>:<password>@<host>:<port>/<DB_name>

meta = MetaData(bind=engine)
MetaData.reflect(meta)

db = SQLAlchemy(app)

# Get show data
 
sql = text("SELECT * FROM settings;")
show_data=engine.execute(sql).fetchone()
 

# Get episode data
 
sql = text("SELECT * FROM posts WHERE status = 'published' ORDER BY id DESC")
episode_data= engine.execute(sql).fetchall()
 

def make_feed():
    # Create feed
    p = Podcast()
    p.set_generator("Open Antenna Podcast Generator", (1,0,0))
    p.name = show_data[1]
    p.authors.append(Person('Open Antenna (OpenAntenna.org)', 'contact@openantenna.org'))
    p.website = 'https://openantenna.org'
    p.copyright = 'Open Antenna 2022'
    p.description = show_data[2]
    p.language = 'en'
    p.feed_url = 'https://openantenna.org/static/feed/podcast.xml'
    p.category = Category('News','Politics')
    p.image = show_data[3]
    p.explicit = False
    p.complete = False
    p.owner = Person('Open Antenna', 'contact@openantenna.org')
    
    # Add episodes
    for item in episode_data:
        e1 = p.add_episode()
        e1.id = item[4]
        e1.title = item[1]
        e1.summary = htmlencode(item[2])
        e1.link = 'http://openantenna.org/episode/sdasd'
        hour_duration = int(item[6].split(':')[0])
        minute_duration = int(item[6].split(':')[1])
        second_duration =  int(item[6].split(':')[2])
        mysql_timestamp = str(item[9]) + "+00:00" # Add UTC data at end
        e1.publication_date = mysql_timestamp
        e1.media = Media(item[4], 17827000,duration=datetime.timedelta(hours=hour_duration, minutes=minute_duration, seconds=second_duration))

    # Write the feed to a file
    p.rss_file('/var/www/openantenna/flaskapp/static/podcast.xml')


make_feed()
