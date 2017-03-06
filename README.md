# CS2340-Server
This is the server that we are going to use for CS2340

**Requirements**  
`sudo apt-get install python-minimal`  
`sudo apt-get install python-mysqldb`  
`sudo mysql_secure_installation`  


**MySQL installation**  
`sudo apt-get update
sudo apt-get install mysql-server`

Login to MySQL and then type the password  
`mysql -u root -p`


**References:**
https://gist.github.com/bradmontgomery/2219997  
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04  


**Troubleshooting**

Man, mysql gives me this when I try to login or try to check status 

ERROR:  
root@68b3e40cb624:/# mysql status  
2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)  

SOLUTION:  
`service mysql start`  


