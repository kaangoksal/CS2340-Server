import sys
import json
import MySQLdb
from pprint import pprint

class WaterAppApi():
    
    @staticmethod
    def mysql_connection():
       MySQLhost = "localhost"
       MySQLusername = "python_backend"
       MySQLpassword = "Secur1ty_1s_sexy"
       database = "waterapp"
       return MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

    @staticmethod
    def handleLogin(Headers, datain):
        try:
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)
            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("SELECT password FROM users where email = \"%s\" " % Email)
            DBpassword = cursor.fetchone()

            if DBpassword != None:
                (DBpassword,) = DBpassword
                if DBpassword == Password:
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>Successful</h1></body></html>")
                else:
                    datain._set_headers()
                    datain.wfile.write("<html><body><h1>Login Failed, Wrong Password</h1></body></html>")
            else:
                datain._set_headers()
                datain.wfile.write("<html><body><h1>Login Failed not registered</h1></body></html>")
            DataBase.close()
        except(KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- handleLogin: Login failed"
            print sys.exc_info()[0]
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Login Failed Exception</h1></body></html>")


    @staticmethod
    def registerAccount(Headers, datain):
        try:
            #print "[DEBUG] - registerAccount:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            Email = parsedJson["email"]
            Username = parsedJson["username"]
            Password = parsedJson["password"]
            Token    = parsedJson["token"]

            DataBase = WaterAppApi.mysql_connection()
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
    @staticmethod
    def addWaterReport(Headers, datain):
        try:
            #print "[DEBUG] - registerAccount:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            datetime = parsedJson["date"]
            report_number = parsedJson["report_number"]
            reporter = parsedJson["reporter"]
            location = parsedJson["location"]
            data = parsedJson["data"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("insert into reports (date, report_number,"
                           " reporter, location, data) VALUES ( '%s', '%s', '%s', '%s')"% (datetime, report_number,reporter, location, data))
            DataBase.commit()

            print "[DEBUG] - addWaterReport: Adding Water Report"
            print "date " + parsedJson["date"]
            print "report_number " + parsedJson["report_number"]
            print bcolors.OKBLUE +"reporter " + parsedJson["reporter"] + bcolors.ENDC
            print "location " + parsedJson["location"]

            datain._set_headers()
            datain.wfile.write("<html><body><h1>Report Added Successfully</h1></body></html>")
            print "[DEBUG] - AddWaterReport:Success "


        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- AddWaterReport: Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>AddWaterReport Failed</h1></body></html>")

    @staticmethod
    def getWaterRepots(Headers, datain):
        try:
            print "[DEBUG] - getWaterReports:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            # datetime = parsedJson["date"]
            # report_number = parsedJson["report_number"]
            # reporter = parsedJson["reporter"]
            # location = parsedJson["location"]
            # data = parsedJson["data"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("SELECT date, report_number, reporter, location, data from reports")
            dataget = cursor.fetchone()
            DataBase.commit()

            #convert info to json and pass bietch


            datain._set_headers()
            datain.wfile.write("<html><body><h1>Here are the reports</h1></body></html>")
            print "[DEBUG] - getWaterReport: SUccessful "


        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- getWaterReport: Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")

    @staticmethod
    def deleteWaterReport(Headers, datain):
        try:
            print "[DEBUG] - deleteWaterReport:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            report_number = parsedJson["report_number"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("SELECT date, report_number, reporter, location, data from reports")
            dataget = cursor.fetchone()
            DataBase.commit()



            print dataget

            # convert info to json and pass bietch


            datain._set_headers()
            datain.wfile.write("<html><body><h1>Here are the reports</h1></body></html>")
            print "[DEBUG] - deleteWaterReport: water report deleted "


        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- deleteWaterReport: Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1> delete water report failed</h1></body></html>")

    @staticmethod
    def editWaterReport(Headers, datain):
        try:
            print "[DEBUG] - editWaterReport:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            datetime = parsedJson["date"]
            report_number = parsedJson["report_number"]
            reporter = parsedJson["reporter"]
            location = parsedJson["location"]
            data = parsedJson["data"]


            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("UPDATE reports set date= %s, reporter = %s, location = %s, data= %s where report_number = %s" % (datetime,reporter, location, data, report_number))
            DataBase.commit()

            # convert info to json and pass bietch return the updated report

            datain._set_headers()
            datain.wfile.write("<html><body><h1>Here are the reports</h1></body></html>")
            print "[DEBUG] - editWaterReport: report edited "


        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editWaterReport: Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Fetch waterreports Failed</h1></body></html>")
    @staticmethod
    def editUser(Headers, datain):
        try:
            print "[DEBUG] - editUser:"
            content_length = int(datain.headers['Content-Length'])
            post_data = datain.rfile.read(content_length)
            parsedJson = json.loads(post_data)

            username = parsedJson["username"]
            password = parsedJson["password"]
            email = parsedJson["email"]

            DataBase = WaterAppApi.mysql_connection()
            cursor = DataBase.cursor()

            cursor.execute("UPDATE users set username= \"%s\", password = \"%s\" where email = \"%s\"" % (username,password, email))
            DataBase.commit()

            # convert info to json and pass bietch return the updated report

            datain._set_headers()
            datain.wfile.write("<html><body><h1>Successful</h1></body></html>")
            print "[DEBUG] - editUser: user edited "


        except (KeyError):
            print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- editUser: Failed"
            datain._set_headers()
            datain.wfile.write("<html><body><h1>Failed/h1></body></html>")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
