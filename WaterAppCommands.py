
import json
import MySQLdb
from pprint import pprint

class WaterAppApi():
    MySQLhost = "localhost"
    MySQLusername = "na na na"
    MySQLpassword = "na na na"
    database = "waterapp"

    @staticmethod
    def handleLogin(Headers, datain):
        try:
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)
            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]

            global MySQLhost
            global MySQLusername
            global MySQLpassword
            global database
            DataBase = MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)
            cursor = DataBase.cursor()

            cursor.execute("SELECT password FROM users where email = \"%s\" " % Email)
            DBpassword = cursor.fetchone()

            if DBpassword != None:
                (DBpassword,) = DBpassword
                if DBpassword == Password:
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>Login Failed</h1></body></html>")
                else:
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>Login Failed</h1></body></html>")
            else:
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Login Failed</h1></body></html>")
            DataBase.close()
        except(Exception):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- handleLogin: Login failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Login Failed</h1></body></html>")


    @staticmethod
    def registerAccount(Headers, datain):
        global MySQLhost
        global MySQLusername
        global MySQLpassword
        global database
        try:
            #print "[DEBUG] - registerAccount:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]
            Token    = parsedJson["token"]

            DataBase = MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

            cursor = DataBase.cursor()

            cursor.execute("SELECT email FROM users where email = \"%s\" " % Email)
            EmailDBResult = cursor.fetchone()
            cursor.execute("SELECT username FROM users where username = \"%s\" " % Username)
            UsernameDBResult = cursor.fetchone()


            if EmailDBResult == None and UsernameDBResult == None:
                print "[DEBUG] - registerAccount: Registering User"
                print "email " + parsedJson["email"]
                print "username " + parsedJson["username"]
                print bcolors.OKBLUE +"password " + parsedJson["password"] + bcolors.ENDC
                print "token " + parsedJson["token"]
                try:
                    cursor.execute("INSERT INTO users(email, username, password, token) VALUES \
        ('%s', '%s', '%s', '%s')" % (Email, Username, Password, Token))
                    DataBase.commit()
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>User Account Registered</h1></body></html>")
                    print "[DEBUG] - registerAccount: Account registered for "
                except:
                    DataBase.rollback()
                    print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: MySQL Commit Failed"
                DataBase.close()
            else:
                if EmailDBResult != None:
                    (EmailDBResult,) = EmailDBResult
                else:
                    EmailDBResult = "None"
                if UsernameDBResult != None:
                    (UsernameDBResult,) = UsernameDBResult
                else:
                    UsernameDBResult = "None"

                print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: Registeration failed " + EmailDBResult  + " " + UsernameDBResult
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Registration Failed</h1></body></html>")
            # username
            # password
            # email
            # account
            # type
            # token(to
            # send
            # push
            # notification)
            # created_at



        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- registerAccount: Registeration failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Registration Failed</h1></body></html>")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
