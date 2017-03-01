
import json
import MySQLdb
from pprint import pprint

class WaterAppApi():

    @staticmethod
    def handleLogin(Headers, self):
        Auth = "123"
        try:
            if Headers["authorization"] == Auth:
                self._set_headers()
                self.wfile.write("<html><body><h1>Authorized</h1></body></html>")
            else:
                self._set_headers()
                self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")
        except (KeyError):
            self._set_headers()
            self.wfile.write("<html><body><h1>Authorization failed</h1></body></html>")

    @staticmethod
    def registerAccount(Headers, datain):

        MySQLhost = "localhost"
        MySQLusername = "yok oyle kolay patates"
        MySQLpassword = "hadi bakim baska kapiya"
        database = "waterapp"


        try:
            print "[DEBUG] - registerAccount:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]
            Token    = parsedJson["token"]



            DataBase = MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

            cursor = DataBase.cursor()

            cursor.execute("SELECT email FROM users where email = \"%s\" " % Email )
            EmailDBResult = cursor.fetchone()
            cursor.execute("SELECT username FROM users where username = \"%s\" " % Username)
            UsernameDBResult = cursor.fetchone()


            if EmailDBResult == None and UsernameDBResult == None:
                print "[DEBUG] Registering User"
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
                    print "Error"
                DataBase.close()
            else:
                print "[ERROR] - registerAccount: Registeration failed " + EmailDBResult + " " + UsernameDBResult
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
            print "[ERROR] - registerAccount: Registeration failed"
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