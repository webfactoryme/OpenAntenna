from flask import Flask, session, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import result
from sqlalchemy import text, Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()
app = Flask(__name__)

# Database Connection
engine = create_engine("mysql://root:password@localhost:3306/openantenna")    

# Initialize Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)

db = SQLAlchemy(app)

### Create Database Tables
class analytics(Base):
    __tablename__="analytics"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    ip = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(10),nullable=False)
    request = db.Column(db.String(300),nullable=False)
    referral = db.Column(db.String(300),nullable=False)
    client = db.Column(db.String(300),nullable=False)
    response = db.Column(db.String(10),nullable=False)
    databased_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    country = db.Column(db.String(30),nullable=False)
    city = db.Column(db.String(30),nullable=False)
    state = db.Column(db.String(30),nullable=False)
    latitude = db.Column(db.String(10),nullable=False)
    longitude = db.Column(db.String(10),nullable=False)
    postal = db.Column(db.String(100),nullable=True)
    def __str__(self):
        return f'<analytics {self.id}>'

class donation_methods(Base):
    __tablename__="donation_methods"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    service = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(300),nullable=False)
    active = db.Column(db.Integer,autoincrement=False)
    def __str__(self):
        return f'<donation_methods {self.id}>'

class posts(Base):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(750), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(300),nullable=False)
    length = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    submission_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    publish_time = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    requests = db.Column(db.Integer, nullable=False)
    title_slug = db.Column(db.String(750),nullable=False)
    def __str__(self):
        return f'<posts {self.id}>'

class relays(Base):
    __tablename__="relays"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(500),nullable=False)
    type = db.Column(db.String(100),nullable=False)
    def __str__(self):
        return f'<relays {self.id}>'

class settings(Base):
    __tablename__="settings"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(750), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(300),nullable=False)
    podcast_category = db.Column(db.String(300),nullable=False)
    email = db.Column(db.String(300),nullable=False)
    explicit = db.Column(db.String(20),nullable=False)
    donations_active = db.Column(db.Integer, nullable=False)
    donate_description = db.Column(db.String(1000),nullable=False)
    shortened_name = db.Column(db.String(100),nullable=False)     
    def __str__(self):
        return f'<settings {self.id}>'

class social(Base):
    __tablename__="social"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(300),nullable=False)
    image = db.Column(db.String(300),nullable=False)
    def __str__(self):
        return f'<social {self.id}>'

class GuestUser(Base):
    __tablename__="guest_user"
    id = Column(db.Integer, primary_key=True,autoincrement=True)
    name = Column(db.String(100), nullable=False)
    email = Column(db.String(50),nullable=False)
    message = Column(db.String(1000), nullable=False)

class users(Base):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1000),nullable=False)
    phone = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    date_registered =  db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    last_login = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),nullable=False)
    user_type = db.Column(db.String(10),nullable=False)
    status = db.Column(db.String(10),nullable=False)
    def __str__(self):
        return f'<users {self.id}>'

Base.metadata.create_all(engine)

@app.route("/")
def home():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall()
    return(render_template('index.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/posts/")
def posts():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()   
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")    
    donation_methods_data=engine.execute(sql).fetchall()          
    return(render_template('posts-listing.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/post/<post_slug>")
def single_post_page(post_slug):
    # Get individual post data
    sql = text("SELECT * FROM posts WHERE status = 'published' and title_slug = '{}' ORDER BY id DESC;".format(str(post_slug)))
    post_data=engine.execute(sql).fetchone()
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")   
    posts_data=engine.execute(sql).fetchall() 
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall()  
    return(render_template("post-page.html", settings_data=settings_data, posts_data=posts_data, post_data=post_data, donation_methods_data=donation_methods_data))

@app.route("/donate")
def donate():
    # Get donate status and description
    sql = text("SELECT * FROM settings LIMIT 1;")
    show_data=engine.execute(sql).fetchone()
    if show_data:
        if show_data[7] == 1:
            # Get settings data
            sql = text("SELECT * FROM settings;")
            settings_data=engine.execute(sql).fetchone()
            # Get posts data
            sql = text("SELECT * FROM posts WHERE status = 'published';")
            posts_data=engine.execute(sql).fetchall()    
            # Get donations data
            sql = text("SELECT * FROM donation_methods WHERE active = 1;")
            donation_methods_data=engine.execute(sql).fetchall()        
            return render_template('donate.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data)
        else:
            return(redirect(url_for('home')))
    else:
        return(redirect(url_for('home')))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    # Get posts data
    sql = text("SELECT * FROM posts WHERE status = 'published';")
    posts_data=engine.execute(sql).fetchall()    
    # Get donations data
    sql = text("SELECT * FROM donation_methods WHERE active = 1;")
    donation_methods_data=engine.execute(sql).fetchall() 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        data = ( { "name": name,
          "email": email,
          "message": message},
          )
        statement = text("""INSERT INTO guest_user (name, email,
        message) VALUES(:name, :email,
        :message)""")
        for line in data:
            engine.execute(statement, **line)
        return redirect(url_for('home'))
    return(render_template('contact.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()
    if 'username' in session:
        # Get post data
        sql = text("SELECT * FROM posts ORDER BY id DESC;")
        post_data=engine.execute(sql).fetchall()   
        # Automatically create length and title_slug for db
        return(render_template('admin.html', settings_data=settings_data,post_data=post_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/edit-upload")
def admin_edit_upload():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()  
    if 'username' in session: 
        # Automatically create length and title_slug for db
        return(render_template('admin-edit-upload.html', settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/analytics")
def admin_analytics():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone()     
    if 'username' in session:
        # Get analytics data
        sql = text("SELECT * FROM analytics ORDER BY id DESC LIMIT 1000;") 
        analytics_data=engine.execute(sql).fetchall()  
        # Automatically create length and title_slug for db
        return(render_template('admin-analytics.html',settings_data=settings_data, analytics_data=analytics_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/analytics/ip/<ip_id>")
def admin_analytics_ip(ip_id):
    ip_address = ip_id.replace('-','.')
    return(ip_address)

@app.route("/admin/users")
def admin_users():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    if 'username' in session: 
        # Get user data
        sql = text("SELECT * FROM users ORDER BY id DESC;")  
        user_data=engine.execute(sql).fetchall() 
        return(render_template('admin-users.html',settings_data=settings_data,user_data=user_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/settings")
def admin_settings():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    if 'username' in session: 
        # Automatically create length and title_slug for db
        return(render_template('admin-settings.html',settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    if request.method == 'POST':
        # # Get potential user data
        email = request.form['email']
        password = request.form['password']
        sql = text("SELECT * FROM users WHERE email = '{}' AND password = '{}';".format(email,password))
        user_data=engine.execute(sql).fetchone() 
        if user_data == None:
            return(redirect(url_for('login')))
        else:
            session['username'] = user_data[1]
            session['email'] = user_data[3]
            return(redirect(url_for('admin')))
    return('''
        <form method="post">
            <p><input type=text name=email>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get settings data
    sql = text("SELECT * FROM settings;")
    settings_data=engine.execute(sql).fetchone() 
    return('coming soon')

if __name__ == "__main__":   
    app.run(host="0.0.0.0",debug = True)