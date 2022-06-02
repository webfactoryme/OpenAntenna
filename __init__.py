from flask import Flask, session, request, redirect, url_for, render_template
import MySQLdb

app = Flask(__name__)

# Database Connection
db = MySQLdb.connect(host="host",user="user",passwd="password",db="openantenna",port=3306)

@app.route("/")
def home():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    # Get posts data
    cursor = db.cursor()
    sql = "SELECT * FROM posts WHERE status = 'published';"
    cursor.execute(sql)
    posts_data = cursor.fetchall()    
    # Get donations data
    cursor = db.cursor()
    sql = "SELECT * FROM donation_methods WHERE active = 1;"
    cursor.execute(sql)
    donation_methods_data = cursor.fetchall()       
    return(render_template('index.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/posts/")
def posts():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    # Get posts data
    cursor = db.cursor()
    sql = "SELECT * FROM posts WHERE status = 'published';"
    cursor.execute(sql)
    posts_data = cursor.fetchall()    
    # Get donations data
    cursor = db.cursor()
    sql = "SELECT * FROM donation_methods WHERE active = 1;"
    cursor.execute(sql)
    donation_methods_data = cursor.fetchall()            
    return(render_template('posts-listing.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/post/<post_slug>")
def single_post_page(post_slug):
    # Get individual post data
    cursor = db.cursor()
    sql = "SELECT * FROM posts WHERE status = 'published' and title_slug = '{}' ORDER BY id DESC;".format(str(post_slug))
    cursor.execute(sql)
    post_data = cursor.fetchone()
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    # Get posts data
    cursor = db.cursor()
    sql = "SELECT * FROM posts WHERE status = 'published';"
    cursor.execute(sql)
    posts_data = cursor.fetchall()    
    # Get donations data
    cursor = db.cursor()
    sql = "SELECT * FROM donation_methods WHERE active = 1;"
    cursor.execute(sql)
    donation_methods_data = cursor.fetchall()
    return(render_template("post-page.html", settings_data=settings_data, posts_data=posts_data, post_data=post_data, donation_methods_data=donation_methods_data))

@app.route("/donate")
def donate():
    # Get donate status and description
    cursor = db.cursor()
    sql = "SELECT * FROM settings LIMIT 1;"
    cursor.execute(sql)
    show_data = cursor.fetchone()
    if show_data[7] == 1:
        # Get settings data
        cursor = db.cursor()
        sql = "SELECT * FROM settings;"
        cursor.execute(sql)
        settings_data = cursor.fetchone()
        # Get posts data
        cursor = db.cursor()
        sql = "SELECT * FROM posts WHERE status = 'published';"
        cursor.execute(sql)
        posts_data = cursor.fetchall()    
        # Get donations data
        cursor = db.cursor()
        sql = "SELECT * FROM donation_methods WHERE active = 1;"
        cursor.execute(sql)
        donation_methods_data = cursor.fetchall()      
        return render_template('donate.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data)
    else:
        return(redirect(url_for('home')))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    # Get posts data
    cursor = db.cursor()
    sql = "SELECT * FROM posts WHERE status = 'published';"
    cursor.execute(sql)
    posts_data = cursor.fetchall()    
    # Get donations data
    cursor = db.cursor()
    sql = "SELECT * FROM donation_methods WHERE active = 1;"
    cursor.execute(sql)
    donation_methods_data = cursor.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(name, email, message)   
        return redirect(url_for('home'))
    return(render_template('contact.html', settings_data=settings_data, posts_data=posts_data, donation_methods_data=donation_methods_data))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    if 'username' in session:
        # Get post data
        cursor = db.cursor()
        sql = "SELECT * FROM posts ORDER BY id DESC;"
        cursor.execute(sql)
        post_data = cursor.fetchall()    
        # Automatically create length and title_slug for db
        return(render_template('admin.html', settings_data=settings_data,post_data=post_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/edit-upload")
def admin_edit_upload():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    if 'username' in session: 
        # Automatically create length and title_slug for db
        return(render_template('admin-edit-upload.html', settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/analytics")
def admin_analytics():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()    
    if 'username' in session:
        # Get analytics data
        cursor = db.cursor()
        sql = "SELECT * FROM analytics ORDER BY id DESC LIMIT 1000;"
        cursor.execute(sql)
        analytics_data = cursor.fetchall()    
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
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    if 'username' in session: 
        # Get user data
        cursor = db.cursor()
        sql = "SELECT * FROM users ORDER BY id DESC;"
        cursor.execute(sql)
        user_data = cursor.fetchall()    
        return(render_template('admin-users.html',settings_data=settings_data,user_data=user_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route("/admin/settings")
def admin_settings():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    if 'username' in session: 
        # Automatically create length and title_slug for db
        return(render_template('admin-settings.html',settings_data=settings_data))
    return("Please <a href='/login'>Log In</a> For Access")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get settings data
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    if request.method == 'POST':
        # # Get potential user data
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE email = '{}' AND password = '{}';".format(email,password)
        cursor.execute(sql)
        user_data = cursor.fetchone() 
        if user_data == None:
            return(redirect(url_for('login')))
        else:
            session['username'] = user_data[1]
            session['email'] = user_data[3]
            return(redirect(url_for('admin')))
        return()

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
    cursor = db.cursor()
    sql = "SELECT * FROM settings;"
    cursor.execute(sql)
    settings_data = cursor.fetchone()
    return('coming soon')

if __name__ == "__main__":
    app.run(debug = True)
