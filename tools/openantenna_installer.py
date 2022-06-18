sudo apt update &&
sudo apt -y upgrade &&

# Install required linux dependencies
sudo apt install git apache2 mysql-server libmysqlclient-dev python3-pip certbot &&

# Install required Python packages
sudo pip3 install flask flask_sqlalchemy mysqlclient &&

cd /var/www/ &&

rm -rf OpenAntenna/ ||: &&
# Clone OpenAntenna into /var/www/ folder
git clone https://github.com/webfactoryme/OpenAntenna.git &&

# Add configurations for Apache 

# Create OpenAntenna Database in MySQL
mysql -e "CREATE DATABASE IF NOT EXISTS openantenna;" || true &&

# Run OpenAntenna Server for first time to generate DB tables
timeout 2 python3 /var/www/OpenAntenna/__init__.py &&

# Create User in OpenAntenna
mysql openantenna << EOF 
INSERT INTO users (id,name,picture,email,phone,password,date_registered,last_login,user_type,status) VALUES (NULL, 'User', 'https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png', 'emailme@email.com', '9999999999', 'password', '2022-06-18 13:50:39', '2022-06-18 13:50:39', 'admin', 'active'); 
EOF

echo "You can now run 'python3 /var/www/OpenAntenna/__init__.py' to start the server"