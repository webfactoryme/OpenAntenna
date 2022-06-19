sudo apt update &&
sudo apt -y upgrade &&

# Install required linux dependencies
sudo apt install git apache2 mariadb-server python3-pip certbot libmariadb-dev-compat libmariadb-dev libapache2-mod-wsgi-py3 &&

# Install required Python packages
sudo pip3 install flask flask_sqlalchemy mysqlclient &&

cd /var/www/ &&

rm -rf openantenna/ ||: &&

mkdir openantenna &&

cd /var/www/openantenna/ &&

cd /etc/apache2/sites-available/ &&

rm * &&

wget https://raw.githubusercontent.com/webfactoryme/OpenAntenna/main/configs/openantenna.conf &&

cd /var/www/openantenna/ &&

wget https://raw.githubusercontent.com/webfactoryme/OpenAntenna/main/configs/flaskapp.wsgi &&

# Clone OpenAntenna into /var/www/openantenna/ folder
git clone https://github.com/webfactoryme/OpenAntenna.git &&

a2ensite openantenna.conf &&

service apache2 restart &&

# Create OpenAntenna Database in MySQL
mysql -e "CREATE DATABASE IF NOT EXISTS openantenna;" || true &&

mysql <<MYSQL_SCRIPT
USE mysql;
CREATE USER 'openantenna'@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'openantenna'@localhost IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
MYSQL_SCRIPT &&

# Run OpenAntenna Server for first time to generate DB tables
timeout 2 python3 /var/www/openantenna/OpenAntenna/__init__.py &&

# Run OpenAntenna with Apache
sudo a2ensite openantenna.conf &&

# Create User in OpenAntenna
mysql openantenna << EOF 
INSERT INTO openantenna.users (id,name,picture,email,phone,password,date_registered,last_login,user_type,status) VALUES (NULL, 'User', 'h>
EOF

echo "You can now run 'python3 /var/www/openantenna/OpenAntenna/__init__.py' to start the server"
