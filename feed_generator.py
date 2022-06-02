#!/usr/bin/env python

import MySQLdb
import os
from podgen import Podcast, Person, Media, Category, htmlencode
import datetime
import pytz
import time

# Database Connection
db = MySQLdb.connect(host="host",user="user",passwd="password",db="openantenna",port=3306)

# Get show data
cursor = db.cursor()
sql = "SELECT * FROM settings;"
cursor.execute(sql)
show_data = cursor.fetchone()

# Get episode data
cursor = db.cursor()
sql = "SELECT * FROM posts WHERE status = 'published' ORDER BY id DESC"
cursor.execute(sql)
episode_data = cursor.fetchall()

def make_feed():
    # Create feed
    p = Podcast()
    p.set_generator("Open Antenna Podcast Generator", (1,0,0))
    p.name = show_data[1]
    p.authors.append(Person('Lead and Circus (LeadandCircus.com)', 'contact@leadandcircus.com'))
    p.website = 'https://leadandcircus.com'
    p.copyright = 'Lead and Circus 2021'
    p.description = show_data[2]
    p.language = 'en'
    p.feed_url = 'https://leadandcircus.com/static/feed/podcast.xml'
    p.category = Category('News','Politics')
    p.image = show_data[3]
    p.explicit = False
    p.complete = False
    p.owner = Person('Lead and Circus', 'contact@leadandcircus.com')
    
    # Add episodes
    for item in episode_data:
        e1 = p.add_episode()
        e1.id = item[4]
        e1.title = item[1]
        e1.summary = htmlencode(item[2])
        e1.link = 'http://leadandcircus.com/episode/sdasd'
        hour_duration = int(item[6].split(':')[0])
        minute_duration = int(item[6].split(':')[1])
        second_duration =  int(item[6].split(':')[2])
        mysql_timestamp = str(item[9]) + "+00:00" # Add UTC data at end
        e1.publication_date = mysql_timestamp
        e1.media = Media(item[4], 17827000,duration=datetime.timedelta(hours=hour_duration, minutes=minute_duration, seconds=second_duration))

    # Write the feed to a file
    p.rss_file('/var/www/openantenna/flaskapp/static/podcast.xml')


make_feed()