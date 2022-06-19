sudo apt update &&
sudo apt -y upgrade &&

# Install required linux dependencies
sudo apt install git apache2 mariadb-server python3-pip certbot libmariadb-dev-compat libmariadb-dev libapache2-mod-wsgi &&

# Install required Python packages
sudo pip3 install flask flask_sqlalchemy mysqlclient &&

cd /var/www/ &&

rm -rf openantenna/ ||: &&

mkdir openantenna &&

cd /var/www/openantenna/ &&

wget https://raw.githubusercontent.com/webfactoryme/OpenAntenna/main/configs/openantenna.conf &&

cd /etc/apache2/sites-available/ &&

wget https://github.com/webfactoryme/OpenAntenna/blob/main/configs/openantenna.conf &&

# Clone OpenAntenna into /var/www/openantenna/ folder
git clone https://github.com/webfactoryme/OpenAntenna.git &&

# Add configurations for Apache 

# Create OpenAntenna Database in MySQL
mysql -e "CREATE DATABASE IF NOT EXISTS openantenna;" || true &&

# Run OpenAntenna Server for first time to generate DB tables
timeout 2 python3 /var/www/openantenna/OpenAntenna/__init__.py &&

# Run OpenAntenna with Apache
sudo a2ensite openantenna.conf &&

# Create User in OpenAntenna
mysql openantenna << EOF 
INSERT INTO openantenna.users (id,name,picture,email,phone,password,date_registered,last_login,user_type,status) VALUES (NULL, 'User', 'h>
EOF

echo "You can now run 'python3 /var/www/openantenna/OpenAntenna/__init__.py' to start the server"